from dataclasses import dataclass
import logging
from typing import Iterable, List

from rich.progress import track
from github import Github, GithubException
from github.Repository import Repository

log = logging.getLogger("rich")

# Error codes
MISSING_BRANCH = 1
BRANCH_ALREADY_EXIST = 2
REPOSITORY_DOES_NOT_EXIST = 3


def create_branch(repo: Repository, new_branch: str, source_branch: str):
	source_ref = repo.get_git_ref(f"heads/{source_branch}")
	source_sha = source_ref.object.sha
	repo.create_git_ref(ref=f"refs/heads/{new_branch}", sha=source_sha)
	log.info('Branch "%s" created from %s in repo "%s"', new_branch, repo.name, source_branch)


def delete_branch(repo: Repository, branch: str):
	repo.get_git_ref(f"heads/{branch}").delete()
	log.info('Branch "%s" deleted in repo "%s"', branch, repo.name)


def create_new_pr(repo: Repository, head_branch: str, base_branch: str, title: str):
	"""
	Args:
		g: github object
		repo: name of the github repository
		head_branch: the branch I want to merge
		base_branch: the branch I want to merge into
		title: title of the PR
	"""
	pr = repo.create_pull(base=base_branch, head=head_branch, title=title)
	log.info('PR created in repo "%s": %s', repo.name, pr.html_url)


def merge_pr_by_branch_names(repo: Repository, head_branch: str, base_branch: str, merge_method: str, delete_branch: bool):
	pull_requests = repo.get_pulls(base=base_branch, head=head_branch, state="open")
	assert pull_requests.totalCount == 1
	pull_requests[0].merge(merge_method=merge_method, delete_branch=delete_branch)
	log.info('Branch "%s" was successfully merged into "%s" in repo %s', head_branch, base_branch, repo.name)


def check_branches_exist(repos: List[Repository], branches: Iterable[str]):
	missing_branches = _get_missing_branches(repos, branches)
	if missing_branches:
		for missing in missing_branches:
			log.error('The branch "%s" is missing in repo "%s"', missing.branch_name, missing.repo_name)
		exit(MISSING_BRANCH)


def check_branch_does_not_exist(repos: List[Repository], branch: str):
	error_found = False
	for repo in track(repos, description='Check branches do not exist'):
		if not _is_branch_missing(repo, branch):
			log.error('The branch "%s" already exists in repo "%s"', branch, repo.name)
			error_found = True
	if error_found:
		exit(BRANCH_ALREADY_EXIST)


@dataclass
class _MissingBranch:
	repo_name: str
	branch_name: str


def _get_missing_branches(repos: List[Repository], branches: Iterable[str]) -> List[_MissingBranch]:
	missing_branches: List[_MissingBranch] = []
	checks = [(repo, branch_name) for repo in repos for branch_name in branches]
	for repo, branch in track(checks, description='Check branches exist'):
		if _is_branch_missing(repo, branch):
			missing_branches.append(_MissingBranch(repo, branch))
	return missing_branches


def _is_branch_missing(repo: Repository, branch_name: str) -> bool:
	try:
		repo.get_branch(branch_name)
	except GithubException as e:
		if e.status == 404:
			return True
		else:
			raise e
	return False


def check_repos_exist(g: Github, repos: List[str]) -> List[Repository]:
	checked_repos: List[Repository] = []
	for repo_name in track(repos, description='Check repositories exist'):
		try:
			repo = g.get_repo(repo_name)
			checked_repos.append(repo)
		except GithubException as e:
			if e.status == 404:
				log.error('Repository "%s" does not exist', repo_name)
			else:
				raise e
	if len(checked_repos) != len(repos):
		exit(REPOSITORY_DOES_NOT_EXIST)
	return checked_repos
