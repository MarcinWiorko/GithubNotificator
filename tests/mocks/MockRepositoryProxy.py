"""Fake repository used in test"""
from dataclasses import dataclass, field

from github.Repository import Repository
from github.Requester import Requester

from github_notificator.models.PyGithubProxy import RepositoryProxy, PullRequestProxy


@dataclass
class MockRepositoryProxy(RepositoryProxy):
    """Fake repository used in test"""
    opened_pull_request: list[PullRequestProxy] = field(default_factory=list)
    closed_pull_request: list[PullRequestProxy] = field(default_factory=list)
    name: str = ""
    main_status: tuple[str, str] = field(default_factory=lambda: ("", ""))
    original_instance: Repository = Repository(attributes={}, completed=True, headers={},
                                               requester=Requester(auth=None, base_url='https://example.org',
                                                                   per_page=30, pool_size=None, retry=None,
                                                                   timeout=60,
                                                                   user_agent='', verify=True))

    def get_closed_pulls(self) -> list[PullRequestProxy]:
        """
        Get closed pulls

        Returns
        -------
            Closed pulls
        """
        return self.closed_pull_request

    def get_open_pulls(self) -> list[PullRequestProxy]:
        """
        Get open pulls

        Returns
        -------
            Open pulls
        """
        return self.opened_pull_request

    def get_name(self) -> str:
        """
        Get name of the repo

        Returns
        -------
           Name of the repo
        """
        return self.name

    def get_main_branch_status_and_conclusion(self, default_branch_workflow_name: str) -> tuple[str, str]:
        """
        Get main branch status and conclusion based on last run

        Parameters
        ----------
        default_branch_workflow_name
            Name of the workflow file run on default branch

        Returns
        -------
            Status and conclusion of the last run as a tuple
        """
        return self.main_status
