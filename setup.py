from setuptools import setup, find_packages
version = open('VERSION').read().strip()

setup(
    name='pywebdriver',
    version=version,
    author='Akretion',
    author_email='contact@akretion.com',
    url='https://github.com/akretion/pywebdriver/',
    description='Python Web Services to communicate wih Devices',
    license="AGPLv3+",
    long_description=open('README.md').read(),
    packages=find_packages(),
    scripts = ['pywebdriverd'],
    include_package_data=True,
    zip_safe=False
)
