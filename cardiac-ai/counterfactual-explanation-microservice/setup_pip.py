from setuptools import setup, find_packages
import os

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(name='counterfactual-explanation-microservice',
      version=version,
      description='Counterfactuals explanations for arrhythmia detection, procedure, and medication- A Python toolbox',
      long_description=readme(),
      keywords='machine learning counterfactual explanation',
      url='https://github.com/prodiptaPromit/prototype-cphs',
      author='Prodipta Promit Mukherjee',
      author_email='prodipta.promit@ieee.org',
      python_requires='>=3.6',
      install_requires=install_requires,
      packages=find_packages(),
      include_package_data=True,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Science/Research',
          'Intended Audience :: Developers',
          'Programming Language :: Python :: 3.6',
          'Topic :: Scientific/Engineering :: Artificial Intelligence'
      ],
      zip_safe=False)
