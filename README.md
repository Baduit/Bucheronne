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

## Return codes
* 0: Success
* 1: A branch that should exist does not exist
* 2: A branch that should not exist, does exist 

## Documentation
You can find auto generated documentation here: https://baduit.github.io/Bucheronne/

## Why is it named "Bucheronne" ?
`Bucheronne` means `lumberjack` in French. A repository is a tree because it has branches and this tool can handle multiple repositories/trees so it is like a forest.
