import codecs
import os.path

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name='netbox-qrcode',
    version=get_version('netbox_qrcode/version.py'),
    description='QR Code generation for netbox objects',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/netbox-community/netbox-qrcode',
    author='Nikolay Yuzefovich',
    author_email='mgk.kolek@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.12',
    license='Apache-2.0',
    license_files=['LICENSE'],
    package_data={
        '': ['*.html'],
    },
    install_requires=[
        'qrcode',
        'Pillow',
        # Imported by template_content.py. NetBox depends on packaging too, so this
        # is satisfied in practice on a NetBox install, but it must be declared for
        # the package to be installable on its own.
        'packaging'
    ],
    extras_require={
        # Django is normally provided by the NetBox installation; the test suite
        # needs it directly so that it can run without NetBox present. Pinned to the
        # series NetBox 4.7 ships, matching this plugin's supported NetBox range.
        'test': ['Django>=6.0,<6.1'],
        'docs': ['mkdocs-material>=9.5,<10.0'],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
    ]
)
