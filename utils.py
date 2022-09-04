import os
import json
from venv import create
import inquirer
from dotenv import load_dotenv
from github import Github

from files import react

load_dotenv()

PROJECT_TYPES = [
  "Express API",
  "Python CLI",
  "React (UI only)",
]
PATH = os.getenv('DEFAULT_PATH')
OPEN_BRACKET = "{"
CLOSED_BRACKET = "}"

def init_setup():
  print("Honey needs to be initialized...")
  DEFAULT_PATH = input("Full path to where your code lives (ex: ~/username/code): ")
  IDE_COMMAND = input("Command to open your editor (ex: code .): ")
  GITHUB_TOKEN = input("Github token: ")
  to_write = [
    'IS_INITIALIZED=True',
    f'DEFAULT_PATH={DEFAULT_PATH}',
    f'IDE_COMMAND={IDE_COMMAND}',
    f'GITHUB_TOKEN={GITHUB_TOKEN}'
  ]
  os.system("touch .env")
  with open('.env', 'w') as e:
    e.write("\n".join(to_write))

def ask_project_questions():
  questions = [
    inquirer.Text(
      'PROJECT_NAME', 
      message="What is the name of this project?"
    ),
    inquirer.List(
      'PROJECT_TYPE',
      message="What type of project is this?",
      choices=PROJECT_TYPES
    ),
    inquirer.List(
      'VCS',
      message="Will you be using VCS for this project?",
      choices=["Yes", "No"]
    )
  ]
  return inquirer.prompt(questions)

def do_project_setup(answers):
  project_name = answers.get('PROJECT_NAME')
  project_type = answers.get('PROJECT_TYPE')
  using_vcs = answers.get('VCS')
  folder_path = f"{PATH}/{project_name}"
  repo_to_return = ""

  if project_type != "Python CLI":
    createFolder(project_name)
    os.chdir(folder_path)
  else:
    cli_folder_path = f"{project_name}cli"
    createFolder(cli_folder_path)
    os.chdir(cli_folder_path)

  if using_vcs == 'Yes':
    user = Github(os.getenv('GITHUB_TOKEN')).get_user()
    repo = user.create_repo(project_name)
    os.system(f"echo \"# {project_name}\nA new application.\" >> README.md")
    os.system("git init")
    os.system("git add README.md")
    os.system("git commit -m \"first commit\"")
    os.system("git branch -M main")
    os.system(f"git remote add origin https://github.com/{repo.full_name}")
    os.system("git push -u origin main")
    repo_to_return = f"https://github.com/{repo.full_name}"


  if project_type == 'Express API':
    os.system('npm init -y')
    os.system('npm install --save express')
    with open('package.json', 'r') as p:
      data = json.load(p)
    data['scripts']['start'] = 'node index.js'
    with open('package.json', 'w') as p2:
      json.dump(data, p2, indent=4)
    os.system(f"echo \"const express = require(\'express\')\nconst healthRouter = require('./routes/api/health')\nconst app = express()\nconst port = \'3000'\napp.use(\'/api/health\', healthRouter)\n\napp.listen(port, () => {OPEN_BRACKET}\n\tconsole.log('Listening...')\n{CLOSED_BRACKET})\n\nmodule.exports = app\" >> index.js")
    os.mkdir('routes')
    os.chdir('routes')
    os.mkdir('api')
    os.chdir('api')
    os.system(f"echo \"const router = require(\'express\').Router()\n\n/* GET health */\nrouter.get(\'/\', async (req, res) => {OPEN_BRACKET}\n\tres.json({OPEN_BRACKET}\n\t\tname:\'{project_name}\',\n\t\talive:true\n\t{CLOSED_BRACKET})\n{CLOSED_BRACKET})\n\nmodule.exports = router \" >> health.js")
    startup_help = [f"cd {folder_path}", "npm start", 'In your browser, navigate to: http://localhost:3000/api/health']
  elif project_type == 'Python CLI':
    os.system(f"echo \"from setuptools import setup, find_packages\n\nsetup(\n\tname=\'{project_name}cli\', \n\tversion='0.0.0', \n\tpackages=find_packages(), \n\tinstall_requires=[\n\t\t'click'\n\t], \n\tentry_points=\'\'\'\n\t[console_scripts]\n\t{project_name}={project_name}cli:{project_name}cli\n\t\'\'\'\n)\" >> setup.py")
    os.system(f"echo \"import click\n\n@click.command()\ndef {project_name}cli():\n\tprint(\'Hello World!\')\" >> {project_name}cli.py")
    os.system(f"pip3 install --editable .")
    startup_help = [project_name, f"NOTE: the path to this project is -> {cli_folder_path}"]
  elif project_type == 'React (UI only)':
    os.system('npm init -y')
    os.system('npm install react react-dom react-router-dom')
    os.system('npm install --save-dev webpack webpack-cli webpack-dev-server')
    os.system('npm install --save-dev babel-loader @babel/preset-env @babel/core @babel/plugin-transform-runtime @babel/preset-react babel-eslint @babel/runtime')
    with open('.babelrc', 'w') as f:
      f.write(react.babelrc)
    with open('webpack.config.js', 'w') as f:
      f.write(react.webpack_config_js)
    os.mkdir('public')
    os.chdir('public')
    with open('index.html', 'w') as f:
      f.write(react.index_html)
    os.system('touch main.js')
    os.chdir('..')
    os.mkdir('src')
    os.chdir('src')
    with open('App.js', 'w') as f:
      f.write(react.App)
    with open('index.js', 'w') as f:
      f.write(react.index_js)  
    os.chdir('..')
    with open('package.json', 'r') as p:
      data = json.load(p)
    data['main'] = 'src/index.js'
    data['scripts']['start'] = 'webpack-dev-server .'
    data['scripts']['build'] = 'Webpack .'
    
    with open('package.json', 'w') as p2:
      json.dump(data, p2, indent=4)

    startup_help = [f"cd {folder_path}", "npm start"]

  return project_name, project_type, startup_help, repo_to_return

def createFolder(project_name):
    try:
      os.chdir(PATH)
      os.mkdir(project_name)
      return json.dumps({ 'message': f'Created folder {project_name}'})
    except FileExistsError:
      return json.dumps({ 'message': f'Folder {project_name} already exists'})

