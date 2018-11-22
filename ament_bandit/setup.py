from setuptools import find_packages
from setuptools import setup

setup(
    name='ament_bandit',
    version='0.5.2',
    packages=find_packages(exclude=['test']),
    install_requires=['setuptools'],
    package_data={'': [
        'configuration/bandit.yaml',
    ]},
    zip_safe=False,
    author='LED',
    author_email='led@led.led',
    maintainer='LED',
    maintainer_email='led@led.led',
    keywords=['ROS'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='Check Python code security using bandit.',
    long_description="""\
The ability to check code for syntax and style conventions with flake8.""",
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ament_bandit = ament_bandit.main:main',
        ],
    },
)
