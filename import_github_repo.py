#!/usr/bin/env python3
"""
GitHub Repository Importer

This script allows you to import (clone) GitHub repositories.
"""

import argparse
import os
import re
import subprocess
import sys


def validate_github_url(repo_url):
    """
    Validate that the URL is a valid GitHub repository URL.
    
    Args:
        repo_url: The URL to validate
    
    Returns:
        True if valid, False otherwise
    """
    # Pattern to match GitHub URLs (both HTTPS and SSH)
    patterns = [
        r'^https://github\.com/[\w\-]+/[\w\-\.]+(?:\.git)?$',
        r'^git@github\.com:[\w\-]+/[\w\-\.]+(?:\.git)?$'
    ]
    
    return any(re.match(pattern, repo_url) for pattern in patterns)


def import_github_repo(repo_url, destination=None, branch=None):
    """
    Import (clone) a GitHub repository.
    
    Args:
        repo_url: The GitHub repository URL (e.g., https://github.com/user/repo.git)
        destination: Optional destination directory (defaults to repo name)
        branch: Optional specific branch to clone
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Validate the GitHub URL to prevent command injection
        if not validate_github_url(repo_url):
            print(f"Error: Invalid GitHub repository URL: {repo_url}")
            print("Expected format: https://github.com/user/repo.git or git@github.com:user/repo.git")
            return False
        cmd = ['git', 'clone']
        
        if branch:
            cmd.extend(['--branch', branch])
        
        cmd.append(repo_url)
        
        if destination:
            cmd.append(destination)
        
        print(f"Importing repository: {repo_url}")
        if branch:
            print(f"Branch: {branch}")
        if destination:
            print(f"Destination: {destination}")
        
        # Run git clone with a timeout to prevent indefinite blocking
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("Repository imported successfully!")
            return True
        else:
            # Display both stdout and stderr for complete error information
            error_msg = result.stderr.strip() or result.stdout.strip()
            print(f"Error importing repository: {error_msg}")
            return False
            
    except FileNotFoundError:
        print("Error: git command not found. Please install git.")
        return False
    except subprocess.TimeoutExpired:
        print("Error: Git clone operation timed out after 300 seconds.")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Import (clone) a GitHub repository',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s https://github.com/user/repo.git
  %(prog)s https://github.com/user/repo.git -d my-folder
  %(prog)s https://github.com/user/repo.git -b main
        '''
    )
    
    parser.add_argument(
        'repo_url',
        help='GitHub repository URL (e.g., https://github.com/user/repo.git)'
    )
    
    parser.add_argument(
        '-d', '--destination',
        help='Destination directory (defaults to repository name)',
        default=None
    )
    
    parser.add_argument(
        '-b', '--branch',
        help='Specific branch to clone',
        default=None
    )
    
    args = parser.parse_args()
    
    success = import_github_repo(args.repo_url, args.destination, args.branch)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
