from netrc import netrc
import os
from pathlib import Path
import platform

from github import Auth


def read_from_file(token_path: os.PathLike) -> Auth.Token:
	"""
	Reads the github token from a file

	Args:
		token_path: The path to the file containing the token.

	Returns:
		Auth.Token: An instance of Auth.Token containing the token read from the file.

	Raises:
		FileNotFoundError: If the file at token_path does not exist.
		IOError: If there is an issue opening or reading the file.
	"""
	with open(token_path, "r", encoding='utf8') as f:
		return Auth.Token(f.read().strip())


def get_from_env() -> Auth.Token | None:
	"""
	Retrieves a GitHub token from the environment variable and returns it

	Returns:
		Auth.Token or None: An instance of Auth.Token if the "GITHUB_TOKEN" environment variable is set, 
		otherwise None.
	"""
	token = os.environ.get("GITHUB_TOKEN")
	return Auth.Token(token) if token else None


def _get_netrc_path() -> Path:
	"""
	Retrieves the path to the .netrc or _netrc file depending on the operating system.

	On Windows, the file is named "_netrc". On other systems, it is named ".netrc".
	The function returns the path to the file located in the user's home directory.

	Returns:
		Path: The full path to the .netrc or _netrc file.
	"""
	filename = ".netrc" if platform.system == "Windows" else "_netrc"
	return Path.home() / filename


def read_from_netrc() -> Auth.Token | None:
	"""
	Reads the GitHub token from the .netrc or _netrc file and returns it

	The function checks for the existence of the .netrc or _netrc file in the user's home directory.
	If the file exists and contains credentials for 'github.com', it extracts the token and returns
	it

	Returns:
		Auth.Token or None: An instance of Auth.Token if the 'github.com' credentials are found in the 
		.netrc or _netrc file, otherwise None.
	"""
	netrc_path = _get_netrc_path()
	if netrc_path.exists():
		for machine, auth_data in netrc(netrc_path).hosts.items():
			if machine == 'github.com':
				print(auth_data)
				_, _,  token = auth_data
				return Auth.Token(token)
	return None


def deduce_token() -> Auth.Token | None:
	"""
	Deduces the GitHub token by first checking the environment variable, then falling back to the .netrc file.

	The function first attempts to retrieve the token from the "GITHUB_TOKEN" environment variable.
	If no token is found, it tries to read the token from the .netrc or _netrc file.

	Returns:
		Auth.Token or None: An instance of Auth.Token if found in either the environment variable or 
		the .netrc file, otherwise None.
	"""
	token = get_from_env()
	return token if token else read_from_netrc()
