"""Fake pull request used in test"""
from dataclasses import dataclass

from src.github_notificator.models.PyGithubProxy import PullRequestProxy


@dataclass
class MockPullRequestProxy(PullRequestProxy):
    """Fake pull request uses in testt"""
    draft: bool
    author: str
    title: str
    labels: list[str]
    mergeable_state: str
    merged_by_user: str
    html_url: str
    link_to_discussion: list[str]
    is_approved: bool

    def is_draft(self) -> bool:
        """
        Check if pr is draft

        Returns
        -------
            True if it is draft otherwise false

        """
        return self.draft

    def get_author(self) -> str:
        """
        Get pr's author

        Returns
        -------
            Author of the pr
        """
        return self.author

    def get_title(self) -> str:
        """
        Get pr's title

        Returns
        -------
            Title of the pr
        """
        return self.title

    def get_labels(self) -> list[str]:
        """
        Get pr's labels

        Returns
        -------
            Labels of the pr
        """
        return self.labels

    def get_mergeable_state(self) -> str:
        """
        Get pr's mergeable state

        Returns
        -------
            Mergeable state of the pr
        """
        return self.mergeable_state

    def get_merged_user(self) -> str:
        """
        Get pr's merged user

        Returns
        -------
           Merged user of the pr
        """
        return self.merged_by_user

    def get_pr_html_url(self) -> str:
        """
        Get pr's html url

        Returns
        -------
            Html url of the pr
        """
        return self.html_url

    def get_links_to_mentions_in_discussions(self, me: str) -> list[str]:
        """
            Get links to discussions where you were mentions
        Parameters
        ----------
        me
            Your GitHub login
        Returns
        -------
            list of links to o discussions where you were mentions in the PR
        """

        return self.link_to_discussion

    def is_already_approved_by_me(self, me: str) -> bool:
        """
           Check if pr is already approved by you
        Parameters
        ----------
        me
            Your GitHub login
        Returns
        -------
           Is the pr already approved by you
        """
        return self.is_approved
