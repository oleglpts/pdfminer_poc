import os
import sys
import site
from argparse import ArgumentParser, Namespace


def activate_virtual_environment(**kwargs):
    """

    Activate virtual environment

    :param kwargs: key parameters

    Allowed following parameters:

    - root_dir (project root dir, default: current directory)
    - environment (virtual environment directory, default: 'venv')
    - packages (path to packages in environment, default: 'lib/python{VERSION}/site-packages')

    :return: condition code (0 if successful)
    :rtype: int

    """
    returned = 0
    env = kwargs.get('environment', 'venv').replace('~', os.getenv('HOME'))
    env_path = env if env[0:1] == "/" else kwargs.get('root_dir', os.getcwd()) + "/" + env
    env_activation = env_path + '/' + 'bin/activate_this.py'
    if not os.path.isfile(env_activation):
        return 1
    site.addsitedir(env_path + '/' + kwargs.get('packages', 'lib/python%s.%s/site-packages' % (
        sys.version_info.major, sys.version_info.minor)).replace(
        '{VERSION}', '%s.%s' % (sys.version_info.major, sys.version_info.minor)))
    sys.path.append('/'.join(env_path.split('/')[:-1]))
    try:
        exec(open(env_activation).read())
    except FileNotFoundError:
        returned = os.system('/bin/bash ' + env_path + '/' + 'bin/activate')
    except Exception as e:
        print('%s: (%s)' % ('virtual environment activation error', str(e)))
        returned = 2
    return returned


def virtual_environment(parser):
    """

    Completion of parsing the command line and activating the virtual environment

    :param parser: command line parser
    :type parser: ArgumentParser
    :return: arguments namespace
    :rtype: Namespace

    """
    parser.add_argument('-e', '--environment', help='virtual environment', default='venv')
    parser.add_argument('-p', '--packages', help='packages path', default='lib/python%s.%s/site-packages' % (
        sys.version_info.major, sys.version_info.minor))
    cmd_args = parser.parse_args()
    activate_virtual_environment(root_dir='.', environment=cmd_args.environment, packages=cmd_args.packages)
    return cmd_args
