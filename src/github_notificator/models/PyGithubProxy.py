"""
File contains classes which are proxy to original ones from PyGithub.
There should make easier testing
"""
from dataclasses import dataclass

from github.PullRequest import PullRequest
from github.Repository import Repository


@dataclass
class PullRequestProxy:
    """Proxy for PullRequest class in PyGithub"""
    original_instance: PullRequest

    # use pr flag to filter

    def is_draft(self) -> bool:
        """
        Check if pr is draft

        Returns
        -------
            True if it is draft otherwise false

        """
        return self.original_instance.draft  # pragma: no cover it needs real repo

    def get_author(self) -> str:
        """
        Get pr's author

        Returns
        -------
            Author of the pr
        """
        return self.original_instance.user.login  # pragma: no cover it needs real repo

    def get_title(self) -> str:
        """
        Get pr's title

        Returns
        -------
            Title of the pr
        """
        return self.original_instance.title  # pragma: no cover it needs real repo

    def get_labels(self) -> list[str]:
        """
        Get pr's labels

        Returns
        -------
            Labels of the pr
        """
        return [str(label) for label in self.original_instance.labels]  # pragma: no cover it needs real repo

    def get_mergeable_state(self) -> str:
        """
        Get pr's mergeable state

        Returns
        -------
            Mergeable state of the pr
        """
        return self.original_instance.mergeable_state  # pragma: no cover it needs real repo

    def get_merged_user(self) -> str:
        """
        Get pr's merged user

        Returns
        -------
           Merged user of the pr
        """
        return '' if self.original_instance.merged_by else self.original_instance.merged_by.login  # pragma: no cover
        # it needs real repo

    def get_pr_html_url(self) -> str:
        """
        Get pr's html url

        Returns
        -------
            Html url of the pr
        """
        return self.original_instance.html_url  # pragma: no cover it needs real repo

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

        return [discussion.html_url for discussion in  # pragma: no cover it needs real repo
                self.original_instance.get_review_comments() for reaction in discussion.get_reactions().get_page(0) if
                f"@{me}" in discussion.body and reaction.user.login != me]

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
        return any(
            review.state == "APPROVED" and review.user.login == me for review in  # pragma: no cover it needs real repo
                   self.original_instance.get_reviews())


@dataclass
class RepositoryProxy:
    """Proxy for Repository class in PyGithub"""
    original_instance: Repository

    def get_closed_pulls(self) -> list[PullRequestProxy]:
        """
        Get closed pulls

        Returns
        -------
            Closed pulls
        """
        return [PullRequestProxy(pr) for pr in  # pragma: no cover it needs real repo
                self.original_instance.get_pulls(state='closed', base='main').get_page(0)]

    def get_open_pulls(self) -> list[PullRequestProxy]:
        """
        Get open pulls

        Returns
        -------
            Open pulls
        """
        return [PullRequestProxy(pr) for pr in self.original_instance.get_pulls(state='open', base='main').get_page(
            0)]  # pragma: no cover it needs real repo

    def get_name(self) -> str:
        """
        Get name of the repo

        Returns
        -------
           Name of the repo
        """
        return self.original_instance.name  # pragma: no cover it needs real repo

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
        last_run = self.original_instance.get_workflow(default_branch_workflow_name).get_runs().get_page(0)[
            0]  # pragma: no cover it needs real repo
        return last_run.status, last_run.conclusion  # pragma: no cover it needs real repo
