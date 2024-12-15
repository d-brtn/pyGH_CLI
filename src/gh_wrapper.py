import os
import subprocess
import dataclasses
import json
import sys
import re
import time
import datetime
import logging
import doctest



FORMAT = '{"Time": "%(asctime)s", "level": "%(levelname)s","file_name":"%(filename)s:%(lineno)s", "function":"%(funcName)s()", "message":"%(message)s"}'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    
class GH_CLI():
    """
    A class for interacting with the GitHub CLI (gh).

    Attributes:
        api_version (str): The GitHub API version to use.
        username (str): The username of the authenticated user.
        gh_cli_path (str): Path to the gh CLI executable.
        repos_raw (list): List of raw repository data for the user.
        repo_perm_index (dict): A dictionary mapping repository names to permissions.
    """

    def __init__ (self, api_version= "2022-11-28"):
        """
        Initialize the GH_CLI instance.

        Args:
            api_version (str): The GitHub API version to use. Default is "2022-11-28".

        Example:
            >>> gh = GH_CLI()
            >>> isinstance(gh.username, str)
            True
        """        

        self.logger = logging.getLogger(__name__)
        self.gh_cli_path = self.get_gh_cli_path()
        self._api_version = api_version
        self.api_version_header = f"X-GitHub-API-Version:{self._api_version}"        
        self._user = self.run_gh_command("api", "/user")
        self.username = self._user['login']
        self.repos_raw = self.pull_all_user_repos()
        self.repo_perm_index = self.setup_repo_index()

        
        pass
    def setup_repo_index(self):
        """
        Set up a dictionary mapping repository names to permissions.

        Returns:
            dict: A dictionary where keys are repository names and values are lists of permissions.

        Example:
            >>> gh = GH_CLI()
            >>> isinstance(gh.repo_perm_index, dict)
            True
        """
        return {repo['full_name']:[permission for permission in repo['permissions'] if permission] for repo in self.repos_raw} 
    
    def get_gh_cli_path(self):
        """
        Get the path to the gh CLI executable.

        Returns:
            str: The path to the gh CLI executable.

        Raises:
            SystemExit: If the gh CLI is not found in the PATH.

        Example:
            >>> gh = GH_CLI()
            >>> isinstance(gh.gh_cli_path, str)
            True
        """
        try:
            gh_cli_path = subprocess.check_output(['which', 'gh']).decode('utf-8').strip()
            return gh_cli_path
        except subprocess.CalledProcessError:
            self.logger.error("gh CLI not found in PATH")
            sys.exit(1)
    def log_cli_error(self, command, error: Exception, *args):
        """
        Log an error that occurred while running a gh CLI command.

        Args:
            command (str): The gh CLI command that caused the error.
            error (Exception): The exception raised.
            *args: Additional arguments passed to the command.
        """
        self.logger.error({"command":{command}, 
                       "error":{error}, 
                       "args": {args}
                       }
                      )
        pass

    
    def run_gh_command(self, command, *args):
        """
        Run a gh CLI command and return the output.

        Args:
            command (str): The gh CLI command to run.
            *args: Additional arguments for the command.

        Returns:
            dict or None: The parsed JSON output from the command, or None if an error occurred.

        Example:
            >>> gh = GH_CLI()
            >>> result = gh.run_gh_command("api", "/user")
            >>> isinstance(result, dict)
            True
        """
        _subprocess_cmd = [self.gh_cli_path, "-H", f"{self.api_version_header}" , command, *args]
        self.logger.debug(f"run_gh_command _subprocess_cmd{_subprocess_cmd}")
        _gh_run = subprocess.run(_subprocess_cmd, capture_output=True, text=True)
        try:
            output = json.loads(_gh_run.stdout)
            logging.debug (f"Running gh command: {command} {[i for i in args]}")
            if isinstance(output, dict) and 'status' in output.keys():
                match output['status']:
                    case '200':
                        logging.info(f"Success running gh command: {command} \t {len(output)}")
                    case '201':
                        logging.info(f"Success running gh command: {command} \t {len(output)}")
                    case '204':
                        logging.info(f"Success running gh command: {command} \t {len(output)}")
                    case '404':
                        raise ValueError(output)
                    case '422':
                        raise ValueError(output)
                    case _:
                        logging.error(f"Error running gh command: {command} \t {output}")
                        raise ValueError(output)            
            return output
        except subprocess.CalledProcessError as e:     
            self.log_cli_error(command=command,
                               error=e,
                               )
        except ValueError as e:
            self.log_cli_error(command=command,
                               error=e,
                               )
        except json.JSONDecodeError as e:
            logging.debug(f"gh command returned non-json output: {command} {_gh_run.stdout}")
        
        except Exception as e:
            self.log_cli_error(
                command=command,
                error=e,
            )
            return None
        
        

    def run_gh_api_get(self, api_url):
        """
        Run a GET request using the gh CLI.

        Args:
            api_url (str): The API endpoint to call.

        Returns:
            dict or None: The parsed JSON output from the command, or None if an error occurred.

        Example:
        >>> gh = GH_CLI()
        >>> result = gh.run_gh_api_get("/user")
        >>> isinstance(result, dict)
        True
        """
        return  self.run_gh_command("api", api_url)
    
    def run_gh_api_post(self, api_url, *args):
        """
        Run a POST request using the gh CLI.

        Args:
            api_url (str): The API endpoint to call.
            *args: Additional arguments for the POST request.

        Returns:
            dict or None: The parsed JSON output from the command, or None if an error occurred.

        Example:
        >>> gh = GH_CLI()
        >>> result = gh.run_gh_api_post("/some/endpoint", "--field", "value")
        >>> result is None or isinstance(result, dict)
        True
        """
        return self.run_gh_command("api", api_url, '-X', "POST", *args)

    def pull_all_user_repos(self):
        """
        Pull all repositories for the authenticated user.

        Returns:
            list: A list of repositories.

        Example:
        >>> gh = GH_CLI()
        >>> repos = gh.pull_all_user_repos()
        >>> isinstance(repos, list)
        True
        """
        return self.run_gh_api_get(f"/users/{self.username}/repos")
    


if __name__ == "__main__":
    gh = GH_CLI()
    tp1 = gh.run_gh_api_get("/search/repositories?q=user:d-brtn")
    import doctest
    doctest.testmod()
    #tp2 = gh.run_gh_api_get('/user/d-brtn/repos')
    print(gh.gh_cli_path)