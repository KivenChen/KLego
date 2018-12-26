from setuptools import setup

setup(
    # to be displayed on PyPI
    name='klego',
    version='0.98.2.7',
    description='An easy-to-go, yet practical and powerful'
                ' python package for Lego NXT',
    long_description='An easy-to-go'
                ' python package for Lego NXT control'
                ' built especially for popular Lego tasks'
                ' like line-following, bonus block hitting.'
                ' More feature with ML or DL might be included'
                ' in the future as well',
    keywords='python lego nxt mindstorm easy lightweight hardware',
    project_urls={
        'Documentation': 'https://github.com/KivenChen/kLego',
        'Source Code': 'https://github.com/KivenChen/kLego',
        'More by Kiven': "https://github.com/Kivenchen",
    },
    author='Kiven',
    author_email='sdckivenchen@gmail.com',
    url='https://kivenchen,us',

    packages=['klego'],
    install_requires=['pyusb', 'nxt-python', 'numpy', 'scipy', 'configobj', 'matplotlib'],
    dependency_links=[
        'https://kivenchen.us/kiven-s-pybluez/PyBluez-0.22.1.tar.gz'],
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['nose'],
)
