from setuptools import setup, find_packages


setup(
    name='django-ttdb',
    version='0.5',
    description='Creates a django test database using a postgres template database.',
    author='William Buick',
    author_email='william.buick@encode.net.nz',
    long_description=open('README.rst', 'r').read(),
    url='http://github.com/wilbuick/django-ttdb',
    license='BSD',
    packages=find_packages(exclude=('tests',)),
    install_requires=[
        'django>=1.8',
        'mock',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ],
)
