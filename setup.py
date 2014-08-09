import distutils.core
from setuptools import setup
distutils.core.setup(
    name='dockit',
    version='2.0',
    packages=[ 'dockinstall','dockutils', 'dockactions', 'dockglobals'],
    url='https://github.com/humblec/dockit',
    license='LICENSE',
    author='hchiramm',
    author_email='hchiramm@redhat.com; humble.devassy@gmail.com',
    install_requires = ['docker-py','paramiko','pip'],
    entry_points={
        'console_scripts': [
            'dockit = dockinstall.install:main'
         ]
    },   
    description='A project to install docker deamon and to start containers..'

)
