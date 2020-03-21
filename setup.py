import codecs

import setuptools


setuptools.setup(
    name='bashlint',
    version='0.1.1',
    description='Bash linting tool',
    long_description=codecs.open('README.rst', 'r', 'utf-8').read(),
    keywords='bash',
    author='Stanislav Kudriashev',
    author_email='stas.kudriashev@gmail.com',
    url='https://github.com/skudriashev/bashlint',
    download_url='https://github.com/skudriashev/bashlint/tarball/0.1.1',
    license='MIT',
    py_modules=['bashlint'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'bashlint = bashlint:main',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
