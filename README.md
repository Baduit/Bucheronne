# Bucheronne
Tool to handle branches with the same name over several repos

## Usage
```
Usage: bucheronne [OPTIONS] COMMAND [ARGS]...

  Bucheronne CLI group

Options:
  -l, --log-level TEXT  Log level
  --help                Show this message and exit.

Commands:
  create     Create a branch on all repositories
  create-pr  Create a PR on all repositories
  delete     Delete a branch on all repositories
  merge-pr   Merge a branch on all repositories
```

### Create
```
Usage: bucheronne create [OPTIONS] [REPOS]...

  Create a branch on all repositories

Options:
  -h, --hostname TEXT    Hostname, useful for github enterprise with custom
                         hostname
  -t, --token-path TEXT  Path of the file where the token is stored
  -b, --branch TEXT      Name of the branch to create  [required]
  -s, --source TEXT      Name of the branch we are creating the new branch
                         from.
  --help                 Show this message and exit.
```

### Create-pr
```
Usage: bucheronne create-pr [OPTIONS] [REPOS]...

  Create a PR on all repositories

Options:
  -h, --hostname TEXT    Hostname, useful for github enterprise with custom
                         hostname
  -t, --token-path TEXT  Path of the file where the token is stored
  -h, --head TEXT        Name of the branch you want to merge  [required]
  -b, --base TEXT        Name of the branch you want to merge into  [required]
  -i, --title TEXT       Title of the PRs.  [required]
  --help                 Show this message and exit.
```

### Delete
```
Usage: bucheronne delete [OPTIONS] [REPOS]...

  Delete a branch on all repositories

Options:
  -h, --hostname TEXT    Hostname, useful for github enterprise with custom
                         hostname
  -t, --token-path TEXT  Path of the file where the token is stored
  -b, --branch TEXT      Name of the branch to create  [required]
  --help                 Show this message and exit
```

### Merge-pr
```
Usage: bucheronne merge-pr [OPTIONS] [REPOS]...

  Merge a branch on all repositories

Options:
  -h, --hostname TEXT             Hostname, useful for github enterprise with
                                  custom hostname
  -t, --token-path TEXT           Path of the file where the token is stored
  -h, --head TEXT                 Name of the branch you want to merge
                                  [required]
  -b, --base TEXT                 Name of the branch you want to merge into
                                  [required]
  -d, --delete-branch BOOLEAN     Flag to delete or not the branch afterward
  -m, --merge-method [rebase|merge|squash]
                                  Merge method, default is rebase
  --help                          Show this message and exit.
```

## Return codes
* 0: Success
* 1: A branch that should exist does not exist
* 2: A branch that should not exist, does exist 

## Documentation
You can find auto generated documentation here: https://baduit.github.io/Bucheronne/

## Why is it named "Bucheronne" ?
`Bucheronne` means `lumberjack` in French. A repository is a tree because it has branches and this tool can handle multiple repositories/trees so it is like a forest.
