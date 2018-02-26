from distutils.core import setup

setup(
    name='oyaml',
    version='0.2',
    description='Ordered YAML: drop-in replacement for PyYAML which preserves dict ordering',
    author='Wim Glenn',
    author_email='hey@wimglenn.com',
    url='https://github.com/wimglenn/oyaml',
    license='MIT',
    py_modules=['oyaml'],
    install_requires=['pyyaml'],
)
