from setuptools import setup

setup(
    name="ec2reboot",
    version='0.1',
    py_modules=['ec2reboot'],
    install_requires=[
        'Click',
	'boto3',
    ],
    entry_points='''
        [console_scripts]
        ec2reboot=ec2reboot:cli
    ''',
)
