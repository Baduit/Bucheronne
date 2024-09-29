from github import Github

def create_branch(g: Github, new_branch: str, source_branch: str, repo_name: str):
	repo = g.get_repo(repo_name)
	source_ref = repo.get_git_ref(f"heads/{source_branch}")
	source_sha = source_ref.object.sha
	repo.create_git_ref(ref=f"refs/heads/{new_branch}", sha=source_sha)
	print(f"Branch '{new_branch}' created successfully!")

