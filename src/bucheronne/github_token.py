from netrc import netrc
import os
from pathlib import Path
import platform

from github import Auth


def read_from_file(token_path: os.PathLike) -> Auth.Token:
	with open(token_path, "r", encoding='utf8') as f:
		return Auth.Token(f.read().strip())


def get_from_env() -> Auth.Token | None:
	token = os.environ.get("GITHUB_TOKEN")
	return Auth.Token(token) if token else None


def _get_netrc_path() -> Path:
	filename = ".netrc" if platform.system == "Windows" else "_netrc"
	return Path.home() / filename

def read_from_netrc() -> Auth.Token | None:
	netrc_path = _get_netrc_path()
	if netrc_path.exists():
		for machine, auth_data in netrc(netrc_path).hosts.items():
			if machine == 'github.com':
				print(auth_data)
				_, _,  token = auth_data
				return Auth.Token(token)
	return None


def deduce_token() -> Auth.Token | None:
	token = get_from_env()
	return token if token else read_from_netrc()
