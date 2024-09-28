import os

from bucheronne.github_token import deduce_token, get_from_env, read_from_file, read_from_netrc


def test_get_from_env():
	os.environ['GITHUB_TOKEN'] = 'trololol'
	assert get_from_env().token == 'trololol'

	del os.environ['GITHUB_TOKEN']
	assert get_from_env() is None


def test_read_from_file(tmp_path):
	token_path = tmp_path / 'github_token.txt'
	with open(token_path, 'w', encoding='utf8') as f:
		f.write('  lol\n')
	assert read_from_file(token_path).token ==  'lol'


def test_read_from_netrc_does_not_exist(tmp_path, mocker):
	fake_netrc = tmp_path / 'fake_netrc'
	mocker.patch('bucheronne.github_token._get_netrc_path', return_value=fake_netrc)
	assert read_from_netrc() is None


def test_read_from_netrc_no_github_com_machine(tmp_path, mocker):
	fake_netrc = tmp_path / 'fake_netrc'
	mocker.patch('bucheronne.github_token._get_netrc_path', return_value=fake_netrc)
	with open(fake_netrc, 'w', encoding='utf8') as f:
		f.write('machine lol\nlogin lol\n password lol')
	assert read_from_netrc() is None


def test_read_from_netrc_success(tmp_path, mocker):
	fake_netrc = tmp_path / 'fake_netrc'
	mocker.patch('bucheronne.github_token._get_netrc_path', return_value=fake_netrc)
	with open(fake_netrc, 'w', encoding='utf8') as f:
		f.write('machine lol\nlogin lol\n password lol\nmachine github.com\nlogin lol\n password notlol\n')
	assert read_from_netrc().token == 'notlol'


def test_deduce_token_from_env(tmp_path, mocker):
	fake_netrc = tmp_path / 'fake_netrc'
	mocker.patch('bucheronne.github_token._get_netrc_path', return_value=fake_netrc)
	with open(fake_netrc, 'w', encoding='utf8') as f:
		f.write('machine lol\nlogin lol\n password lol\nmachine github.com\nlogin lol\n password notlol\n')
	os.environ['GITHUB_TOKEN'] = 'trololol'
	assert deduce_token().token == 'trololol'
	del os.environ['GITHUB_TOKEN']


def test_deduce_token_from_netrc(tmp_path, mocker):
	fake_netrc = tmp_path / 'fake_netrc'
	mocker.patch('bucheronne.github_token._get_netrc_path', return_value=fake_netrc)
	with open(fake_netrc, 'w', encoding='utf8') as f:
		f.write('machine lol\nlogin lol\n password lol\nmachine github.com\nlogin lol\n password notlol\n')
	if os.environ.get('GITHUB_TOKEN') is not None:
		del os.environ['GITHUB_TOKEN']
	assert deduce_token().token == 'notlol'


def test_deduce_token_fail(tmp_path, mocker):
	fake_netrc = tmp_path / 'fake_netrc'
	mocker.patch('bucheronne.github_token._get_netrc_path', return_value=fake_netrc)
	if os.environ.get('GITHUB_TOKEN') is not None:
		del os.environ['GITHUB_TOKEN']
	assert deduce_token() is None
