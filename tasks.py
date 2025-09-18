from invoke import task
from pathlib import Path
import toml
from typing import TypedDict

# HELPERS ------------------------------------------------------------------------------------------
class ProjectMeta(TypedDict):
    name: str
    version: str

def get_project() -> ProjectMeta:
    pyproject = toml.load(Path("pyproject.toml"))
    return pyproject["project"]

def check_git_clean(c):
    status = c.run("git status --porcelain", hide=True).stdout.strip()
    if status:
        raise RuntimeError("Cannot release: working directory has uncommitted changes")

def is_detached_head(c) -> bool:
    result = c.run("git symbolic-ref --quiet HEAD", warn=True, hide=True)
    return result.exited != 0 # non-zero exit means detached

def check_git_pushed(c):
    if is_detached_head(c):
        raise RuntimeError("Cannot release from a detached HEAD. Please switch to a branch with an upstream.")
    local = c.run("git rev-parse @", hide=True).stdout.strip()
    remote = c.run("git rev-parse @{u}", hide=True).stdout.strip()
    base = c.run("git merge-base @ @{u}", hide=True).stdout.strip()
    if local != remote and local != base:
        raise RuntimeError("Cannot release: local commits are not pushed")

# TASKS --------------------------------------------------------------------------------------------
@task
def clean(c):
    c.run("rm -rf dist build *.egg-info")

@task(pre=[clean])
def build(c):
    c.run("uv build")

@task
def tag(c):
    project = get_project()
    c.run(f"git tag {'v' + project['version']}")
    c.run(f"git push origin {'v' + project['version']}")

@task(pre=[build, tag])
def release(c):
    project = get_project()
    c.run(f"gh release create {'v' + project['version']} dist/*.whl")
