"""
    portal
    ~~~~~~

    A portal plugin for FlaskBB.

    :copyright: (c) 2018 by Peter Justin.
    :license: BSD License, see LICENSE for more details.
"""
import ast
import re
import os
from setuptools import find_packages, setup


def read(*parts):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, *parts), "r") as fp:
        return fp.read()


long_description = read("README.md")
version_line = re.search(
    r"__version__\s+=\s+(.*)", read("portal", "__init__.py")
).group(1)
version = str(ast.literal_eval(version_line))


setup(
    name="flaskbb-plugin-portal",
    version=version,
    url="https://flaskbb.org",
    project_urls={
        "Code": "https://github.com/flaskbb/flaskbb-plugin-portal",
        "Issue Tracker": "https://github.com/flaskbb/flaskbb-plugin-portal/issues",
    },
    license="BSD",
    author="FlaskBB Team",
    author_email="peter.justin@outlook.com",
    description="A portal plugin for FlaskBB",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="flaskbb plugin portal",
    packages=find_packages("."),
    include_package_data=True,
    package_data={
        "": ["portal/translations/*/*/*.mo", "portal/translations/*/*/*.po"]
    },
    zip_safe=False,
    platforms="any",
    entry_points={"flaskbb_plugins": ["portal = portal"]},
    install_requires=["FlaskBB>=2.1.0"],
    setup_requires=["Babel"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Environment :: Plugins",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
