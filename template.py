from argparse import ArgumentParser
import yaml
from jinja2 import Environment, FileSystemLoader
import os


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'travis-template')


def main():
    p = ArgumentParser()
    p.add_argument(
        "-tc", "--travis-config",
        help="The yaml file specifying the configuration details for the travis yaml file",
        nargs="?",
    )
    p.add_argument(
        "-o", "--output-dir",
        help="The location to output the completed .travis.yml file. Will be output to \"output-dir/.travis.yml\"",
        nargs="?",
        default="."
    )
    p.set_defaults(func=execute)
    args = p.parse_args()
    execute(args, p)


def execute(args, p):
    output_dir = args.output_dir
    input_config_yaml = args.travis_config
    execute_programmatically(input_config_yaml, output_dir)


def nest_all_the_loops(iterable, matrix=None, matrices=None):
    if matrix is None:
        matrix = {}
    if matrices is None:
        matrices = []
    local_iterable = iterable.copy()
    try:
        lib, versions = local_iterable.pop(0)
    except IndexError:
        matrices.append(matrix.copy())
        return
    for version in versions:
        matrix[lib] = version
        nest_all_the_loops(local_iterable, matrix, matrices)
    return matrices


def execute_programmatically(input_config_yaml, output_dir):
    print("input_config_yaml = %s" % input_config_yaml)
    print("output_directory = %s" % output_dir)
    travis_config = yaml.load(open(input_config_yaml, 'r'))
    print('travis_config = %s' % travis_config)
    # turn the env section of the travis config into the outer product of environments
    env = travis_config.get('env', {})
    print('env from yaml = %s', env)
    env_list = [(k, v) for k, v in env.items()]
    print('library matrix = %s' % env_list)
    if env_list:
        env_outer_prod = nest_all_the_loops(env_list.copy())
        matrix = []
        for mat in env_outer_prod:
            repos = ' '.join(['%s="{%s}"' % (k.upper(), k) for k in sorted(mat.keys()) if k != 'python'])
            matrix.append(('%s' % repos).format(**mat))
        print('env matrix = %s' % matrix)
        travis_config['matrix'] = matrix
        travis_config['env'] = {k.lower(): k.upper() for k in env.keys()}

    #explicitly format the allow_failures section
    allow_failures = travis_config.get('allow_failures', {})
    allow_failures = ["%s: %s" % (k, v) for row in allow_failures for k, v in row.items()]
    travis_config['allow_failures'] = allow_failures
    # create the jinja environment
    jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = jinja_env.get_template('nsls2.tmpl')
    try:
        os.makedirs(output_dir)
    except FileExistsError:
        # the file, uh, already exists
        pass
    travis_yml = template.render(**travis_config)
    travis_fname = os.path.join(output_dir, '.travis.yml')

    with open(travis_fname, 'w') as f:
        f.write(travis_yml)


if __name__ == "__main__":
    main()
