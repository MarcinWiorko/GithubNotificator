"""Contains class which collect information from Github"""
from dataclasses import dataclass, field

from src.github_notificator.models.PyGithubProxy import RepositoryProxy, PullRequestProxy
from src.github_notificator.models.config import Config
from src.github_notificator.models.results import Result, Discussion, ReadyForReview, ReadyForMerge, ToTested


@dataclass
class Collector:
    """Class that collect all message from prs in specific repo for you"""
    repo: RepositoryProxy
    config: Config
    results: list[Result] = field(default_factory=list)

    def _filter_in_case_of_dependabot_prs(self, opened_prs: list[PullRequestProxy]) -> list[PullRequestProxy]:
        if not self.config["dependabot_prs"]:
            return list(
                filter(
                    lambda pr: not pr.is_draft() and pr.get_author() != "dependabot[bot]",
                    opened_prs,
                )
            )
        return opened_prs

    def _filter_task_for_another_team(self, opened_prs: list[PullRequestProxy]) -> list[PullRequestProxy]:
        return list(
            filter(
                lambda pr: all(
                    another_team_thing not in pr.get_title() for another_team_thing in
                    self.config["ignored_pr_labels"]) or any(
                    label == self.config["special_label"] for label in pr.get_labels()),
                opened_prs,
            )
        )

    def _filter_ready_for_merge(self, opened_prs: list[PullRequestProxy]) -> list[PullRequestProxy]:
        return list(
            filter(
                lambda pr: pr.get_mergeable_state() == "clean" and pr.get_author() == self.config["me"],
                opened_prs,
            )
        )

    def _filter_mentions_about_me(self, pr: PullRequestProxy) -> list[str]:
        return pr.get_links_to_mentions_in_discussions(self.config['me'])

    def _is_ready_for_review(self, pr: PullRequestProxy) -> bool:
        return (
                not pr.is_already_approved_by_me(self.config['me'])
                and pr.get_author() != self.config["me"]
        )

    def _is_untested(self, pr: PullRequestProxy) -> bool:
        return pr.get_merged_user() == self.config["me"] and all(
            label != "Tested" for label in pr.get_labels())

    def _prefilter(self) -> list[PullRequestProxy]:
        opened_prs = self.repo.get_open_pulls()
        opened_prs = self._filter_in_case_of_dependabot_prs(opened_prs)
        opened_prs = self._filter_task_for_another_team(opened_prs)
        return opened_prs

    def _collect_ready_for_merge(self, opened_prs: list[PullRequestProxy]) -> None:
        for pr in opened_prs:
            pr_ready_to_merge = ReadyForMerge(self.repo.get_name(), pr.get_title(), pr.get_pr_html_url(),
                                              self.repo.get_main_branch_status_and_conclusion(
                                                  self.config['default_branch_workflow_name']))
            self.results.append(pr_ready_to_merge)
            print(pr_ready_to_merge)

    def _collect_untested(self) -> None:
        untested_prs = self.repo.get_closed_pulls()
        for pr in untested_prs:
            if self._is_untested(pr):
                untested = ToTested(self.repo.get_name(), pr.get_title(), pr.get_pr_html_url())
                self.results.append(untested)
                print(untested)

    def _collect_pr_for_discussion_and_for_review(self, opened_prs: list[PullRequestProxy]) -> None:
        for opened_pr in opened_prs:
            if mentions := self._filter_mentions_about_me(opened_pr):
                for mention in mentions:
                    discussion = Discussion(self.repo.get_name(), opened_pr.get_title(), opened_pr.get_pr_html_url(),
                                            mention)
                    self.results.append(discussion)
                    print(discussion)
            elif self._is_ready_for_review(opened_pr):
                ready_for_review = ReadyForReview(self.repo.get_name(), opened_pr.get_title(),
                                                  opened_pr.get_pr_html_url())
                self.results.append(ready_for_review)
                print(ready_for_review)

    def collect(self) -> list[Result]:
        """Get opened pull request for specific repo"""
        opened_prs = self._prefilter()
        self._collect_ready_for_merge(self._filter_ready_for_merge(opened_prs))
        self._collect_pr_for_discussion_and_for_review(opened_prs)
        self._collect_untested()
        return self.results
