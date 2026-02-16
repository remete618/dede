# dede
dede-test

## GitHub Repository Importer

This repository contains a tool to import (clone) GitHub repositories.

### Usage

```bash
# Import a repository
python3 import_github_repo.py https://github.com/user/repo.git

# Import to a specific directory
python3 import_github_repo.py https://github.com/user/repo.git -d my-folder

# Import a specific branch
python3 import_github_repo.py https://github.com/user/repo.git -b main

# Combine options
python3 import_github_repo.py https://github.com/user/repo.git -d my-folder -b develop
```

### Requirements

- Python 3.x
- Git installed on your system

### Options

- `repo_url` (required): The GitHub repository URL to import
- `-d, --destination`: Specify the destination directory (optional)
- `-b, --branch`: Specify a specific branch to clone (optional)
- `-h, --help`: Show help message
