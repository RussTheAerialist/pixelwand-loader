from setuptools import setup

setup(
    name='pixelwand-loader',
    version='1.0',
    packages=['pwl'],
    url='http://cordandruss.com/',
    license='MIT LICENSE',
    author='Russell Hay',
    author_email='me@russellhay.com',
    description='An Image Loader for the PixelWand',
    requires={
        'Pillow': '*',
        'pyserial': '*',
    },
    entry_points={
        'console_scripts':
            ['pwl = pwl.__main__:main']
    },
    test_suite='tests'
)
