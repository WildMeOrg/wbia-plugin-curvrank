#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import sys
import os
from Cython.Build import cythonize

try:
    from setuptools import setup
    from setuptools import Extension
except ImportError:
    from distutils.core import setup
    from distutils.extension import Extension


CLASSIFIERS = """
Development Status :: 3 - Alpha
Intended Audience :: Developers
Intended Audience :: Science/Research
License :: OSI Approved :: Apache Software License
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: Unix
Operating System :: MacOS
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Programming Language :: Python :: 3.3
Programming Language :: Python :: 3.4
Topic :: Scientific/Engineering :: Bio-Informatics
"""
NAME = 'wbia_curvrank_v2'
MAINTAINER = 'Wildbook Org. | IBEIS IA'
MAINTAINER_EMAIL = 'info@wildme.org'
DESCRIPTION = "A plugin wrapper for Hendrik Weideman's curvrank module"
LONG_DESCRIPTION = DESCRIPTION
KEYWORDS = ['wbia', 'plugin', 'wildbook', 'ia', 'curvrank']
URL = 'https://github.com/WildbookOrg/'
DOWNLOAD_URL = ''
LICENSE = 'Apache'
AUTHOR = MAINTAINER
AUTHOR_EMAIL = MAINTAINER_EMAIL
PLATFORMS = ['Windows', 'Linux', 'Solaris', 'Mac OS-X', 'Unix']
MAJOR = 0
MINOR = 1
MICRO = 0
SUFFIX = 'dev0'
VERSION = '%d.%d.%d.%s' % (MAJOR, MINOR, MICRO, SUFFIX)
PACKAGES = ['wbia_curvrank_v2']


def git_version():
    """Return the sha1 of local git HEAD as a string."""

    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH', 'PYTHONPATH']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=env).communicate()[0]
        return out

    try:
        out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
        git_revision = out.strip().decode('ascii')
    except OSError:
        git_revision = 'unknown-git'
    return git_revision


def write_version_py(filename=os.path.join('wbia_curvrank_v2', '__init__.py')):
    cnt = """# THIS FILE IS GENERATED FROM SETUP.PY
from wbia_curvrank_v2 import _plugin  # NOQA

__version__      = '%(version)s'
__version_git__  = '%(git_revision)s'
__version_full__ = '%%s.%%s' %% (__version__, __version_git__, )
"""
    FULL_VERSION = VERSION
    if os.path.isdir('.git'):
        GIT_REVISION = git_version()
    elif os.path.exists(filename):
        GIT_REVISION = 'RELEASE'
    else:
        GIT_REVISION = 'unknown'

    FULL_VERSION += '.' + GIT_REVISION
    text = cnt % {'version': VERSION, 'git_revision': GIT_REVISION}
    try:
        with open(filename, 'w') as a:
            a.write(text)
    except Exception as e:
        print(e)


def do_setup():
    install_requires = parse_requirements('requirements/runtime.txt')
    extras_require = {
        'all': parse_requirements('requirements.txt'),
        'runtime': parse_requirements('requirements/runtime.txt'),
        'build': parse_requirements('requirements/build.txt'),
    }

    ext_modules = [
        Extension(
            'wbia_curvrank_v2.stitch',
            sources=['wbia_curvrank_v2/stitch.pyx'],
            libraries=['m'],  # Unix-like specific
        )
    ]

    write_version_py()
    setup(
        name=NAME,
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        classifiers=CLASSIFIERS,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        url=URL,
        license=LICENSE,
        platforms=PLATFORMS,
        packages=PACKAGES,
        install_requires=install_requires,
        extras_require=extras_require,
        keywords=CLASSIFIERS.replace('\n', ' ').strip(),
        ext_modules=cythonize(ext_modules),
    )


def parse_requirements(fname='requirements.txt', with_version=False):
    """
    Parse the package dependencies listed in a requirements file but strips
    specific versioning information.

    Args:
        fname (str): path to requirements file
        with_version (bool, default=False): if true include version specs

    Returns:
        List[str]: list of requirements items

    CommandLine:
        python -c "import setup; print(setup.parse_requirements())"
        python -c "import setup; print(chr(10).join(setup.parse_requirements(with_version=True)))"
    """
    from os.path import exists
    import re

    require_fpath = fname

    def parse_line(line):
        """
        Parse information from a line in a requirements text file
        """
        if line.startswith('-r '):
            # Allow specifying requirements in other files
            target = line.split(' ')[1]
            for info in parse_require_file(target):
                yield info
        else:
            info = {'line': line}
            if line.startswith('-e '):
                info['package'] = line.split('#egg=')[1]
            else:
                # Remove versioning from the package
                pat = '(' + '|'.join(['>=', '==', '>']) + ')'
                parts = re.split(pat, line, maxsplit=1)
                parts = [p.strip() for p in parts]

                info['package'] = parts[0]
                if len(parts) > 1:
                    op, rest = parts[1:]
                    if ';' in rest:
                        # Handle platform specific dependencies
                        # http://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-platform-specific-dependencies
                        version, platform_deps = map(str.strip, rest.split(';'))
                        info['platform_deps'] = platform_deps
                    else:
                        version = rest  # NOQA
                    info['version'] = (op, version)
            yield info

    def parse_require_file(fpath):
        with open(fpath, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if line and not line.startswith('#'):
                    for info in parse_line(line):
                        yield info

    def gen_packages_items():
        if exists(require_fpath):
            for info in parse_require_file(require_fpath):
                parts = [info['package']]
                if with_version and 'version' in info:
                    parts.extend(info['version'])
                if not sys.version.startswith('3.4'):
                    # apparently package_deps are broken in 3.4
                    platform_deps = info.get('platform_deps')
                    if platform_deps is not None:
                        parts.append(';' + platform_deps)
                item = ''.join(parts)
                yield item

    packages = list(gen_packages_items())
    return packages


if __name__ == '__main__':
    do_setup()
