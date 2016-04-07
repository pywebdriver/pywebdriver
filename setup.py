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
    install_requires=[ r.strip() for r in open('requirement.txt').read().splitlines() ],
    scripts = ['pywebdriverd'],
    include_package_data=True,
    zip_safe=False
    dependecy_links = [
        'https://github.com/akretion/pypostelium/archive/master.zip#egg=pypostelium-0.0.1',
    ]
    extras_require = {
        'cups':        ["pycups>=1.9.73"],
        'pypostelium': ["pypostelium>=0.0.1"],
    }
)
