from distutils.core import setup

setup(
    name='TaskTracker',
    version='1.0',
    packages=[''],
    url='',
    license='',
    author='Nancy Minyanou',
    author_email='nancy.minyanou@gmail.com',
    description='Utility created to help keep track of what user is working on at x minute intervals. '
                'Output is csv labeled by the week containing timestamped records of user input.'
                'Every Monday it emails over the report from the last week to the email specified in'
                'the private_info.py file.'
)

