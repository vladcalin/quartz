from setuptools import setup, find_packages
import re
import os


def read_dependencies(req_file):
    with open(req_file) as req:
        return [line.strip() for line in req]


def get_file_content(filename):
    with open(filename) as f:
        return f.read()


def get_meta_attr_from_string(meta_attr, content):
    result = re.search("{attrname}\s*=\s*['\"]([^'\"]+)['\"]".format(attrname=meta_attr), content)
    if not result:
        raise RuntimeError("Unable to extract {}".format(meta_attr))
    return result.group(1)


module_content = get_file_content(os.path.join("quartz", "__init__.py"))

setup(
    name="quartz",
    version=get_meta_attr_from_string("__version__", module_content),

    description="Track events in other applications",

    author=get_meta_attr_from_string("__author__", module_content),
    author_email=get_meta_attr_from_string("__email__", module_content),

    packages=find_packages(),
    install_requires=read_dependencies("requirements.txt"),
    include_package_data=True,

    entry_points={
        "console_scripts": [
            "quartz = quartz.cli:cli"
        ]
    }
)
