from setuptools import setup, find_packages

setup(
    name='mirrulations',
    version='0.0.0',
    description='The objective of the Mirrulations project is to make the'
                'data on Regulations.gov more easily accessible to the'
                'public by acting as a mirror to the site.',
    long_description='Read README.md',
    author='Moravian College',
    author_email='colemanb@moravian.edu',
    url='https://github.com/MoravianCollege/mirrulations',
    python_requires='>=3.7.2',
    install_requires=['flask==1.0.2',
                      'pytest==4.3.0',
                      'mock==2.0.0',
                      'redis==3.1.0',
                      'fakeredis[lua]==1.0.2',
                      'python-redis-lock==3.3.1',
                      'requests==2.21.0',
                      'requests-mock==1.5.2',
                      'pytest-cov==2.6.1',
                      'pycodestyle==2.5.0'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={'console_scripts': ['mirrulations_client='
                                      'mirrulations_client.__main__:main',
                                      'mirrulations_server='
                                      'mirrulations_server.__main__:main',
                                      'mirrulations_web='
                                      'mirrulations_web.__main__:main']}
)
