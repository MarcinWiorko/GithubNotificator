"""Fake repository used in test"""
from dataclasses import dataclass

from src.github_notificator.models.PyGithubProxy import RepositoryProxy, PullRequestProxy
from tests.mocks.MockPullRequestProxy import MockPullRequestProxy


@dataclass
class MockRepositoryProxy(RepositoryProxy):
    """Fake repository used in test"""
    opened_pull_request: list[MockPullRequestProxy]
    closed_pull_request: list[MockPullRequestProxy]
    name: str
    main_status: tuple[str, str]

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

    def get_name(self):
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
