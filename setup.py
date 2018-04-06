from setuptools import setup

setup(
    name='uqsemplanner',
    packages=['uqsemplanner'],
    include_package_data=True,
    install_requires=[
        'beautifulsoup4',
        'flask',
        'flask-restful'
    ],
)
