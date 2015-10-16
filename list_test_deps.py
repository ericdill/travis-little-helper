from __future__ import print_function, absolute_import
import yaml
from argparse import ArgumentParser
import re
import os


def safe_yaml_read(fpath, replace_str=''):
    """
    Reads a yaml file stripping all of the jinja templating markup
    Parameters
    ----------
    fpath : str
        Path to yaml file to sanitize
    replace_str : str
        String to replace the template markup with, defaults to ''.
    Returns
    -------
    yaml_dict : dict
        The dictionary with all of the jinja2 templating fields
        replaced with ``replace_str``.
    """
    with open(fpath, 'r') as f:
        lns = []
        for ln in f:
            lns.append(re.sub(r'{[{%].*?[%}]}', '', ln))
    meta_dict = yaml.load(''.join(lns))
    return meta_dict


def main():
    p = ArgumentParser()
    p.add_argument(
        '-p', '--path',
        help="Path to meta.yaml",
        nargs="?"
    )
    p.add_argument(
        '-e', '--environment',
        help="Environmental variables to grab",
        nargs="+",
    )
    args = p.parse_args()
    return execute(args, p)


def execute(args, argparser):
    meta_yaml_path = args.path
    env = args.environment
    return execute_programmatically(meta_yaml_path, env)


def execute_programmatically(path_to_meta_yaml, env=None):
    if env is None:
        env = []
    meta_dict = safe_yaml_read(path_to_meta_yaml)
    test_section = meta_dict.get('test', {})
    test_deps = test_section.get('requires', {})
    test_deps = [k.split(' ') for k in test_deps]
    version_dict = {}
    for dep in test_deps:
        name = dep[0]
        version = dep[1] if len(dep) == 2 else ''
        version_dict[name] = version
    # print('version_dict = %s' % version_dict)
    # override conda recipe versions with environmental variable versions
    for lib_name in env:
        version_dict[lib_name.lower()] = os.environ[lib_name.upper()]
    return ["%s%s" % (k, v) for k, v in version_dict.items()]
    # return [s.replace(' ', '') for s in meta_dict['test']['requires']]


if __name__ == "__main__":
    test_requirements = main()
    for req in test_requirements:
        print(req, end=' ')
