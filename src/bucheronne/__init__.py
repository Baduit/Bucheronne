import logging

import click
from github import Github, Consts
from rich.logging import RichHandler
from rich.progress import track
from rich.traceback import install

from .github_branch import check_branches_exist, check_branch_does_not_exist, check_repos_exist, create_branch, create_new_pr, delete_branch, merge_pr_by_branch_names
from .github_token import deduce_token, read_from_file


@click.group()
@click.option("--log-level", "-l", type=str, default='WARNING', help="Log level")
def main(log_level):
    """Bucheronne CLI group"""
    install(show_locals=True)
    
    FORMAT = "%(message)s"
    logging.basicConfig(level=log_level, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])


@main.command()
@click.argument('repos', nargs=-1)
@click.option("--hostname", "-h", type=str, help="Hostname, useful for github enterprise with custom hostname")
@click.option("--token-path", "-t", type=str, help="Path of the file where the token is stored")
@click.option("--branch", "-b", required=True, type=str, help="Name of the branch to create")
@click.option("--source", "-s", type=str, default='main', help="Name of the branch we are creating the new branch from.")
def create(repos, hostname, token_path, branch, source) -> int:
    """
    Create a branch on all repositories
    """
    with _connect(hostname, token_path) as g:
        repos = check_repos_exist(g, repos)
        check_branch_does_not_exist(repos, branch)
        check_branches_exist(repos, [source])
        for repo in track(repos, description='Creating'):
            create_branch(repo, branch, source)
    return 0


@main.command()
@click.argument('repos', nargs=-1)
@click.option("--hostname", "-h", type=str, help="Hostname, useful for github enterprise with custom hostname")
@click.option("--token-path", "-t", type=str, help="Path of the file where the token is stored")
@click.option("--branch", "-b", required=True, type=str, help="Name of the branch to create")
def delete(repos, hostname, token_path, branch) -> int:
    """
    Delete a branch on all repositories
    """
    with _connect(hostname, token_path) as g:
        repos = check_repos_exist(g, repos)
        check_branches_exist(repos, [branch])
        for repo in track(repos, description='Deleting'):
            delete_branch(repo, branch)
    return 0


@main.command()
@click.argument('repos', nargs=-1)
@click.option("--hostname", "-h", type=str, help="Hostname, useful for github enterprise with custom hostname")
@click.option("--token-path", "-t", type=str, help="Path of the file where the token is stored")
@click.option("--head", "-h", required=True, type=str, help="Name of the branch you want to merge")
@click.option("--base", "-b", required=True, type=str, default='main', help="Name of the branch you want to merge into")
@click.option("--title", "-i", required=True, type=str, default='main', help="Title of the PRs.")
def create_pr(repos, hostname, token_path, head, base, title) -> int:
    """
    Create a PR on all repositories
    """
    with _connect(hostname, token_path) as g:
        repos = check_repos_exist(g, repos)
        check_branches_exist(repos, [base, head])
        for repo in track(repos, description='Creating'):
            create_new_pr(repo, head, base, title)
    return 0


@main.command()
@click.argument('repos', nargs=-1)
@click.option("--hostname", "-h", type=str, help="Hostname, useful for github enterprise with custom hostname")
@click.option("--token-path", "-t", type=str, help="Path of the file where the token is stored")
@click.option("--head", "-h", required=True, type=str, help="Name of the branch you want to merge")
@click.option("--base", "-b", required=True, type=str, default='main', help="Name of the branch you want to merge into")
@click.option("--delete-branch", "-d", type=bool, default=True, help="Flag to delete or not the branch afterward")
@click.option("--merge-method", "-m", type=click.Choice(["rebase", "merge", "squash"]), default="rebase", help="Merge method, default is rebase")
def merge_pr(repos, hostname, token_path, head, base, delete_branch, merge_method) -> int:
    """
    Merge a branch on all repositories
    """
    with _connect(hostname, token_path) as g:
        repos = check_repos_exist(repos)
        check_branches_exist(repos, [base, head])
        for repo in track(repos, description='Merging'):
            merge_pr_by_branch_names(g, repo, head, base, merge_method, delete_branch)
    return 0


def _connect(hostname: str, token_path: str | None) -> Github:
    """
    Connect to Github
    """
    auth = read_from_file(token_path) if token_path else deduce_token()
    base_url = f"https://{hostname}/api/v3" if hostname else Consts.DEFAULT_BASE_URL
    return Github(auth=auth, base_url=base_url)
