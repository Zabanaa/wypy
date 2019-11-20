import setuptools
from wypy.utils.constants import VERSION

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name='wypy',
    version=VERSION,
    description='A NetworkManager CLI utility.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(
        exclude=['docs', 'tests']
    ),
    url="https://github.com/Zabanaa/wypy",
    author="Karim C",
    author_email="karim.cheurfi@gmail.com",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Security'
    ],
    keywords="network-manager network manager nmcli dbus d-bus",
    python_requires='>=3.7',
    install_requires=[
        'click',
        'termcolor',
        'prettytable',
        'dbus-python'
    ],
    entry_points={
        'console_scripts': [
            'wypy=wypy.cli:cli'
        ]
    }
)
