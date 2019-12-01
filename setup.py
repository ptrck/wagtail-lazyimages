import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='wagtail-lazyimages',
    version='0.1.5',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description=('A wagtail plugin that generates tiny blurry '
                 'placeholder images for lazy-loading.'),
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/ptrck/wagtail-lazyimages/',
    author='Patrick Dengler',
    author_email='info@patrickdengler.de',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Wagtail',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
