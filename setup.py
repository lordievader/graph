from setuptools import setup

setup(
    name='graph',
    version='1.0.1',
    description='Graph library based on NetworkX',
    author='Olivier van der Toorn',
    author_email='oliviervdtoorn@gmail.com',
    packages=['graph'],
    install_requires=['matplotlib', 'networkx', 'pygraphviz'],
)
