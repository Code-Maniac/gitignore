from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='gitignore',
    version='0.1.0',
    description='Gitignore file generation and management',
    long_description=readme,
    author='Nick Jaycock',
    author_email='jaycock.n@gmail.com',
    url='https://gitlab.com/CodeGremlin/gitignore.git',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
