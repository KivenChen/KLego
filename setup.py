from setuptools import setup, find_packages
import os

# install modified bluetooth module
os.system('python pybluez\\setup.py install')
TO_EXCLUDE = ['pybluez']

setup(
    # to be displayed on PyPI
    name='klego',
    version='0.95b0',
    description='the beta v0.95 version of klego, an easy-to-go'
                ' python package for Lego NXT control'
                ' built especially for popular Lego tasks'
                ' like line-following and bonus block hitting',
    keywords='python lego nxt mindstorm easy',
    project_urls={
        'Documentation': 'https://github.com/KivenChen/PyLego',
        'Source Code': 'https://github.com/KivenChen/PyLego',
        'More by Kiven': "https://github.com/Kivenchen",
    },
    author='Kiven',
    author_email='sdckivenchen@gmail.com',
    url='https://kivenchen,us',

    packages=[i for i in find_packages() if i not in TO_EXCLUDE],
    install_requires=['pyusb'],
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['nose'],
)
