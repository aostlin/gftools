from setuptools import setup, find_packages

import versioneer


def readme():
    with open('README.rst') as file_:
        return file_.read()


setup(
    name="gftool",
    version=versioneer.get_version(),
    description="Collection of commonly used Green's functions and utilities",
    long_description=readme(),
    keywords=["Green's function", "physics"],
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Physics',
    ],
    url="https://github.com/DerWeh/gftools",
    project_urls={
        "ReadTheDocs": "https://gftools.readthedocs.io/en/latest/",
        "Source Code": "https://github.com/DerWeh/gftools",
        "Documentation": "https://derweh.github.io/gftools/",
    },
    author="Weh",
    author_email="andreas.weh@physik.uni-augsburg.de",
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'mpmath'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'hypothesis', 'hypothesis_gufunc'],
)
