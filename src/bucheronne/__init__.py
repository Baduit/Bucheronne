import click
from github import Github, Consts

from .github_branch import create_branch, create_new_pr, delete_branch
from .github_token import deduce_token, read_from_file


@click.group()
def main():
    """Bucheronne CLI group"""
    pass


@main.command()
@click.argument('repos', nargs=-1)
@click.option("--hostname", "-h", type=str, help="Hostname, useful for github enterprise with custom hostname")
@click.option("--token-path", "-t", type=str, help="Path of the file where the token is stored")
@click.option("--branch", "-b", required=True, type=str, help="Name of the branch to create")
@click.option("--source", "-s", type=str, default='main', help="Name of the branch we are creating the new branch from.")
def create(repos, hostname, token_path, branch, source) -> int:
    auth = read_from_file(token_path) if token_path else deduce_token()
    base_url = f"https://{hostname}/api/v3" if hostname else Consts.DEFAULT_BASE_URL
    with Github(auth=auth, base_url=base_url) as g:
        for repo in repos:
            create_branch(g, repo, branch, source)
    return 0


@main.command()
@click.argument('repos', nargs=-1)
@click.option("--hostname", "-h", type=str, help="Hostname, useful for github enterprise with custom hostname")
@click.option("--token-path", "-t", type=str, help="Path of the file where the token is stored")
@click.option("--branch", "-b", required=True, type=str, help="Name of the branch to create")
def delete(repos, hostname, token_path, branch) -> int:
    auth = read_from_file(token_path) if token_path else deduce_token()
    base_url = f"https://{hostname}/api/v3" if hostname else Consts.DEFAULT_BASE_URL
    with Github(auth=auth, base_url=base_url) as g:
        for repo in repos:
            delete_branch(g, repo, branch)
    return 0


@main.command()
@click.argument('repos', nargs=-1)
@click.option("--hostname", "-h", type=str, help="Hostname, useful for github enterprise with custom hostname")
@click.option("--token-path", "-t", type=str, help="Path of the file where the token is stored")
@click.option("--head", "-h", required=True, type=str, help="Name of the branch you want to merge")
@click.option("--base", "-b", type=str, default='main', help="Name of the branch you want to merge into")
@click.option("--title", "-i", type=str, default='main', help="Title of the PRs.")
def create_pr(repos, hostname, token_path, head, base, title) -> int:
    auth = read_from_file(token_path) if token_path else deduce_token()
    base_url = f"https://{hostname}/api/v3" if hostname else Consts.DEFAULT_BASE_URL
    with Github(auth=auth, base_url=base_url) as g:
        for repo in repos:
            create_new_pr(g, repo, head, base, title)
    return 0