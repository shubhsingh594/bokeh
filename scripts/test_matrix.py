from __future__ import print_function

import argparse
import os
import shutil
import subprocess
import textwrap


def get_parser():
    """Create the parser that will be used to add arguments to the script.
    """

    parser = argparse.ArgumentParser(description=textwrap.dedent("""
                    Creates conda environments for a given
                    version of bokeh, installed using pip and
                    conda and including python 2.7 and python 3.4.

                    The --version ('-v') option takes an earlier version of
                    bokeh, for use in creating environments where bokeh will be
                    updated.


                    Ex: ' python test_matrix.py -v 0.7.0'
                    """), formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-v', '--version', action='store', default=False,
                        help='Version of bokeh', required=True)
    # parser.add_argument('')

    return parser


def cleaner(env_path):
    """Checks that an environment path exists and, if so, deletes it.
    """

    if os.path.exists(env_path):
        shutil.rmtree(env_path)


def conda_creator(env_name, pkgs):
    """Create a conda environment of a given name containing a given string of pkgs.
    """
    subprocess.call("conda create --yes -n %s %s" % (env_name, pkgs), shell=True)


def bokeh_installer(env_name, install_string):
    """Activate an environment and run its install string to either install or update bokeh using
    conda or pip.
    """
    if os.name == 'nt':
        command_string = 'activate %s & %s' % (env_name, install_string)
    else:
        command_string = 'source activate %s; %s' % (env_name, install_string)

    result = subprocess.call(command_string, shell=True)

    return result == 0


if __name__ == '__main__':

    parser = get_parser()
    ops = parser.parse_args()

    ver = ops.version

    envs = {
        "py27_conda_clean"    : {
            "init"    : "python=2.7 nose mock",
            "install" : '; '.join([
                    # install latest version from dev channel
                    "conda install --yes -c bokeh/channel/dev bokeh",
                    # install dependencies needed for testing
                    "conda install --yes  -c auto websocket-client",
                    "conda install --yes  -c bokeh nose mock blaze abstract-rendering beautiful-soup ipython scipy websocket multiuserblazeserver pillow",
                ])
            },
        "py27_conda_update"   : {
            "init"    : "python=2.7 nose mock bokeh=%s" % ver,
            "install" : '; '.join([
                    "conda update --yes -c bokeh/channel/dev bokeh",
                    # install dependencies needed for testing
                    "conda install --yes -c auto websocket-client",
                    "conda install --yes -c bokeh nose mock blaze abstract-rendering beautiful-soup ipython scipy websocket multiuserblazeserver pillow",
                ])
            },
        # "py27_pip_clean"      : {
        #     "init"    : "python=2.7 nose mock pip",
        #     "install" : '; '.join([
        #         # Latest version of pip not included in anaconda 2.3.0
        #         "pip install --upgrade pip",
        #         "pip install --pre -i https://pypi.anaconda.org/bokeh/channel/dev/simple bokeh --extra-index-url https://pypi.python.org/simple/",
        #         # install dependencies needed for testing
        #         "pip install nose mock blaze abstract-rendering beautifulsoup4 ipython scipy websocket-client multiuserblazeserver",
        #         ])
        #     },
        # "py27_pip_update"     : {
        #     "init"    : "python=2.7 pip nose mock bokeh=%s" % ver,
        #     "install" :  '; '.join([
        #         # Latest version of pip not included in anaconda 2.3.0
        #         "pip install --upgrade pip",
        #         "pip install --upgrade --pre -i https://pypi.anaconda.org/bokeh/channel/dev/simple bokeh --extra-index-url https://pypi.python.org/simple/",
        #         # install dependencies needed for testing
        #         "pip install nose mock blaze abstract-rendering beautifulsoup4 ipython scipy websocket-client multiuserblazeserver",
        #         ])
        #     },
        "py34_conda_clean"    : {
            "init"    : "python=3.4 nose mock",
            "install" : '; '.join([
                    # install latest version from dev channel
                    "conda install --yes -c bokeh/channel/dev bokeh",
                    # install dependencies needed for testing
                    "conda install --yes  -c bokeh nose mock blaze abstract-rendering beautiful-soup ipython scipy multiuserblazeserver pillow",
                ])
            },
        "py34_conda_update"   : {
            "init"    : "python=3.4 nose mock bokeh=%s" % ver,
            "install" : '; '.join([
                    "conda update --yes -c bokeh/channel/dev bokeh",
                    # install dependencies needed for testing
                    "conda install --yes -c bokeh nose mock blaze abstract-rendering beautiful-soup ipython scipy multiuserblazeserver pillow",
                ])
            },
        # "py34_pip_clean"      : {
        #     "init"    : "python=3.4 nose mock pip",
        #     "install" : '; '.join([
        #         # Latest version of pip not included in anaconda 2.3.0
        #         "pip install --upgrade pip",
        #         "pip install --pre -i https://pypi.anaconda.org/bokeh/channel/dev/simple bokeh --extra-index-url https://pypi.python.org/simple/",
        #         # install dependencies needed for testing
        #         "pip install nose mock blaze abstract-rendering beautifulsoup4 ipython scipy websocket-client multiuserblazeserver",
        #         ])
        #     },
        # "py34_pip_update"     : {
        #     "init"    : "python=3.4 pip nose mock bokeh=%s" % ver,
        #     "install" :  '; '.join([
        #         # Latest version of pip not included in anaconda 2.3.0
        #         "pip install --upgrade pip",
        #         "pip install --upgrade --pre -i https://pypi.anaconda.org/bokeh/channel/dev/simple bokeh --extra-index-url https://pypi.python.org/simple/",
        #         # install dependencies needed for testing
        #         "pip install nose mock blaze abstract-rendering beautifulsoup4 ipython scipy websocket-client multiuserblazeserver",
        #         ])
        #     },
    }


    # Use this method rather than os.path.expanduser('~/anaconda') to provide
    # miniconda support
    root = subprocess.check_output(['conda', 'info', '--root']).rstrip()

    for environment in envs:
        successful_install = True
        cleaner(os.path.join(root, "envs", environment))
        print()
        print("CREATING NEW ENV", environment)
        conda_creator(environment, envs[environment]["init"])

        install = bokeh_installer(environment, envs[environment]["install"])
        if not install:
            successful_install = False

    print()
    print("*********************")
    if successful_install:
        print("All environments have been installed!  See below for their names.")
        for environment in envs:
            print(environment)
        print("NOTE: All of these envs will be deleted and replaced if you rerun this script.")
    else:
        print("Some (or all) of the environments failed to install.")
    print("*********************")
