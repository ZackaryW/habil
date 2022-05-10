from setuptools import setup

setup(
    name='habil',
    version='0.0.4',
    url='https://github.com/ZackaryW/habil',
    description="a lite python wrapper for habitica api",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='ZackaryW',
    author_email='zackaryxcw@gmail.com',
    packages=[
        'habil',
        'habil.elements',
        'habil.sub',
        'habil_base',
        'habil_case',
        'habil_map',
        'habil_ext',
        'habil_utils',
    ],
    license='MIT',
    install_requires=[
        'requests',
    ],
    python_requires='>=3.10',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ]
)