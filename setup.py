from setuptools import setup, find_packages

setup(
  name='honeycli',
  version='0.0.0',
  packages=find_packages(),
  install_requires=[
    'click',
    'python-dotenv',
    'inquirer',
    'PyGithub'
  ],
  entry_points='''
  [console_scripts]
  honey=honeycli:honeycli
  '''
)