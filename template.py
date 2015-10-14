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

def execute_programmatically(input_config_yaml, output_dir):
    print("input_config_yaml = %s" % input_config_yaml)
    print("output_directory = %s" % output_dir)
    travis_config = yaml.load(open(input_config_yaml, 'r'))
    print('travis_config = %s' % travis_config)

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