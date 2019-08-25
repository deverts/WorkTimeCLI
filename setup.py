import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="worktimecli",
    version="0.0.1",
    author="Daniel Everts",
    author_email="deverts3@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deverts/worktimecli",
    packages=setuptools.find_packages(),
    classifiers=[],
)
