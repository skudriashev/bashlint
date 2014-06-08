import setuptools


setuptools.setup(
    name='bashlint',
    version='0.0.1',
    description="Bash linting tool",
    long_description="Simple Bash linting tool written in Python.",
    keywords='bash',
    author='Stanislav Kudriashev',
    author_email='stas.kudriashev@gmail.com',
    url='https://github.com/skudriashev/bashlint',
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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
