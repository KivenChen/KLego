from setuptools import setup

setup(
    # to be displayed on PyPI
    name='klego',
    version='0.98.2.5',
    description='An easy-to-go, yet specific and powerful'
                ' python package for Lego NXT',
    long_description='An easy-to-go'
                ' python package for Lego NXT control'
                ' built especially for popular Lego tasks'
                ' like line-following, bonus block hitting.'
                ' More feature with ML or DL might be included'
                ' in the future as well',
    keywords='python lego nxt mindstorm easy',
    project_urls={
        'Documentation': 'https://github.com/KivenChen/PyLego',
        'Source Code': 'https://github.com/KivenChen/PyLego',
        'More by Kiven': "https://github.com/Kivenchen",
    },
    author='Kiven',
    author_email='sdckivenchen@gmail.com',
    url='https://kivenchen,us',

    packages=['klego'],
    install_requires=['pyusb', 'nxt-python', 'numpy', 'scipy'],
    dependency_links=[
        'https://kivenchen.us/kiven-s-pybluez/PyBluez-0.22.1.tar.gz'],
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['nose'],
)
