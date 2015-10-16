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
    args = p.parse_args()
    return execute(args, p)


def execute(args, argparser):
    meta_yaml_path = args.path
    return execute_programmatically(meta_yaml_path)


def execute_programmatically(path_to_meta_yaml):
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

    # override by environmental variables
    for name, version in version_dict.items():
        version_dict[name] = os.environ.get(name.upper(), version)
    return ["%s%s" % (k, v) for k, v in version_dict.items()]
    # return [s.replace(' ', '') for s in meta_dict['test']['requires']]


if __name__ == "__main__":
    test_requirements = main()
    for req in test_requirements:
        print(req, end=' ')
