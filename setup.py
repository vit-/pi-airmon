from setuptools import setup, find_packages

setup(
    name='airmon',
    description='Simple air quality monitoring and forecasting tool for Raspberry Pi',
    classifiers=[
        'Programming Language :: Python',
    ],
    author='Vitalii Vokhmin',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'aiotg',
        'matplotlib',
        'numpy',
        'pandas',
        'pony',
        'serial',
        'statsmodels',
    ]
)
