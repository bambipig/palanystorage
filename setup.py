"""
    Setup file for palanystorage.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 4.4.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""
from setuptools import setup

if __name__ == "__main__":
    try:
        setup(
            use_scm_version={"version_scheme": "no-guess-dev"},
            name='palanystorage',
            packages=['palanystorage'],
            install_requires=[
                'oss2==2.17.0',
                'qiniu==7.10.0',
                'cos-python-sdk-v5==1.9.24',
                'loguru==0.6.0',
                'typer==0.9.0',
                'anyconfig==0.13.0',
            ],
        )
    except:  # noqa
        print(
            "\n\nAn error occurred while building the project, "
            "please ensure you have the most updated version of setuptools, "
            "setuptools_scm and wheel with:\n"
            "   pip install -U setuptools setuptools_scm wheel\n\n"
        )
        raise
