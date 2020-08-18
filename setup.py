from setuptools import setup

setup(
    name="oyaml",
    version="1.0",
    description="Ordered YAML: drop-in replacement for PyYAML which preserves dict ordering",
    long_description=open("README.rst").read(),
    author="Wim Glenn",
    author_email="hey@wimglenn.com",
    url="https://github.com/wimglenn/oyaml",
    license="MIT",
    py_modules=["oyaml"],
    install_requires=["pyyaml"],
)
