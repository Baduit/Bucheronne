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


def merge_pr_by_branch_names(g: Github, repo_name: str, head_branch: str, base_branch: str, merge_method: str, delete_branch: bool):
	repo = g.get_repo(repo_name)
	pull_requests = repo.get_pulls(base=base_branch, head=head_branch, state="open")
	assert pull_requests.totalCount == 1
	pull_requests[0].merge(merge_method=merge_method, delete_branch=delete_branch)
	print("Sucess")
