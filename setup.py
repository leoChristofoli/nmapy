from setuptools import setup, find_packages

setup(
    name='skyline',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'xmltodict'
    ],
    entry_points='''
        [console_scripts]
        infoc=package.commands.infoc:cli
    ''',
)