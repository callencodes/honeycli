import os
import click

from dotenv import load_dotenv
from utils import init_setup, ask_project_questions, do_project_setup

load_dotenv()

@click.command()
def honeycli():
  if not os.getenv("IS_INITIALIZED"):
    init_setup()
  answers = ask_project_questions()
  project_name, project_type, startup_help, repo = do_project_setup(answers)
  click.echo(f"\n\n{project_name} is all set up! Just run the following commands: \n")
  for helper in startup_help:
    if not "NOTE" in helper:
      click.echo(f"[{startup_help.index(helper) + 1}] {helper}")
    if "NOTE" in helper:
      click.echo(f"\n{helper}")
  
  if repo:
    click.echo(f"\nYour Github repo was created here: {repo}")
