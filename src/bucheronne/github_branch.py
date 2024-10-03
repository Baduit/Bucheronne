from github import Github

def create_branch(g: Github, repo_name: str, new_branch: str, source_branch: str):
	repo = g.get_repo(repo_name)
	source_ref = repo.get_git_ref(f"heads/{source_branch}")
	source_sha = source_ref.object.sha
	repo.create_git_ref(ref=f"refs/heads/{new_branch}", sha=source_sha)
	print(f"Branch '{new_branch}' created successfully!")


def delete_branch(g: Github, repo_name: str, branch: str):
	repo = g.get_repo(repo_name)
	repo.get_git_ref(f"heads/{branch}").delete()
	print(f"Branch '{branch}' deleted successfully!")


def create_new_pr(g: Github, repo_name: str, head_branch: str, base_branch: str, title: str):
	"""
	Args:
		g: github object
		repo: name of the github repository
		head_branch: the branch I want to merge
		base_branch: the branch I want to merge into
		title: title of the PR
	"""
	repo = g.get_repo(repo_name)
	pr = repo.create_pull(base=base_branch, head=head_branch, title=title)
	print(f"Pull Request created successfully: {pr.html_url}")
