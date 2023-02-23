#! /usr/bin/env python

import codecs
import os

from setuptools import find_packages, setup

ver_file = os.path.join('digital_patient', '_version.py')
with open(ver_file) as f:
    exec(f.read())

DISTNAME = 'patient-dt-modelling'
DESCRIPTION = 'Digital representation of patient DT model using Graph Neural Networks,'+
'Graph Adversarial Network, and Machine Learning Algorithms '
with codecs.open('README.rst', encoding='utf-8-sig') as f:
    LONG_DESCRIPTION = f.read()
MAINTAINER = 'Prodipta Promit Mukherjee'
MAINTAINER_EMAIL = 'prodipta.promit@ieee.org'
URL = 'https://github.com/prodiptaPromit/prototype-nghs-spdt'
LICENSE = 'Apache 2.0'
DOWNLOAD_URL = 'https://github.com/prodiptaPromit/prototype-nghs-spdt'
VERSION = __version__
INSTALL_REQUIRES = ['numpy', 'scipy', 'dgl', 'scikit-learn', 'pandas']
CLASSIFIERS = ['Intended Audience :: Researchers',
               'Intended Audience :: Developers',
               'License :: OSI Approved',
               'Programming Language :: Python',
               'Topic :: Software Development',
               'Topic :: Scientific/Engineering',
               'Operating System :: Unix',
               'Operating System :: Microsoft :: Windows',
               'Operating System :: POSIX',
               'Operating System :: MacOS',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3.5',
               'Programming Language :: Python :: 3.6',
               'Programming Language :: Python :: 3.7']
EXTRAS_REQUIRE = {
    'tests': [
        'pytest',
        'pytest-cov'],
    'docs': [
        'sphinx',
        'sphinx-gallery',
        'sphinx_rtd_theme',
        'numpydoc',
        'matplotlib'
    ]
}

setup(name=DISTNAME,
      maintainer=MAINTAINER,
      maintainer_email=MAINTAINER_EMAIL,
      description=DESCRIPTION,
      license=LICENSE,
      url=URL,
      version=VERSION,
      download_url=DOWNLOAD_URL,
      long_description=LONG_DESCRIPTION,
      zip_safe=False,
      classifiers=CLASSIFIERS,
      packages=find_packages(),
      install_requires=INSTALL_REQUIRES,
      extras_require=EXTRAS_REQUIRE)
