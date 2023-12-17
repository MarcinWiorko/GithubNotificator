"""Main file"""
import json

from github import Auth
from github import Github

from github_notificator.collectors.collectors import Collector
from github_notificator.models.PyGithubProxy import RepositoryProxy
from github_notificator.models.config import Config


def main() -> None:
    """Main function"""
    with open("github_token.txt") as file:
        token = file.readline()
    auth = Auth.Token(token)
    g = Github(auth=auth)

    repos: list[str] = []
    with open("repos.txt") as file:
        repos.extend(repo.rstrip() for repo in file)

    with open("config.json") as file:
        config: Config = json.load(file)

    for repo in repos:
        _results = Collector(RepositoryProxy(g.get_repo(repo)), config).collect()


if __name__ == "__main__":
    main()
