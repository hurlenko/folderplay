import os
from codecs import open

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(
    os.path.join(here, "folderplay", "__version__.py"), "r", "utf-8"
) as f:
    exec(f.read(), about)

with open("README.md", "r", "utf-8") as f:
    readme = f.read()

with open("requirements.txt", "r", "utf-8") as f:
    requires = f.readlines()


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join("..", path, filename))
    return paths


setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    url=about["__url__"],
    packages=find_packages(),
    package_data={"folderplay": package_files("folderplay/assets")},
    python_requires=">=3.5",
    install_requires=requires,
    license=about["__license__"],
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    project_urls={"Source": about["__url__"]},
    entry_points={"console_scripts": ["fplay = folderplay.__main__:main"]},
)
