"""
    This is a
    multiline
    description for the portal

    plugin.
"""
from setuptools import find_packages, setup


setup(
    name='flaskbb-plugin-portal',
    version='1.0',
    url='http://github.com/sh4nks/flaskbb/',
    license='BSD',
    author='FlaskBB Team',
    author_email='peter.justin@outlook.com',
    description='A portal plugin for FlaskBB',
    long_description=__doc__,
    packages=find_packages('.'),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    entry_points={
        'flaskbb_plugins': [
            'portal = portal'
        ]
    }
)
