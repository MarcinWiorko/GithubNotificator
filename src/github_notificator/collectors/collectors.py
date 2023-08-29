from dataclasses import dataclass, field

from github.PullRequest import PullRequest
from github.PullRequestComment import PullRequestComment
from github.Repository import Repository

from src.github_notificator.models.config import Config
from src.github_notificator.models.results import Result, Discussion, ReadyForReview, ReadyForMerge, ToTested


@dataclass
class Collector:
    """Class that collect all message from prs in specific repo for you"""
    repo: Repository
    config: Config
    results: list[Result] = field(default_factory=list)

    def _filter_in_case_of_dependabot_prs(self, opened_prs: list[PullRequest]) -> list[PullRequest]:
        if not self.config["dependabot_prs"]:
            return list(
                filter(
                    lambda pr: not pr.draft and pr.user.login != "dependabot[bot]",
                    opened_prs,
                )
            )
        return opened_prs

    def _filter_task_for_another_team(self, opened_prs: list[PullRequest]) -> list[PullRequest]:
        return list(
            filter(
                lambda pr: all(
                    devops_thing not in pr.title for devops_thing in self.config["ignored_pr_labels"]) or any(
                    label.name == self.config["special_label"] for label in pr.labels),
                opened_prs,
            )
        )

    def _filter_ready_for_merge(self, opened_prs: list[PullRequest]) -> list[PullRequest]:
        return list(
            filter(
                lambda pr: pr.mergeable_state == "clean" and pr.user.login == self.config["me"],
                opened_prs,
            )
        )

    @staticmethod
    def _filter_not_ready_for_merge(opened_prs: list[PullRequest]) -> list[PullRequest]:
        return list(filter(lambda pr: pr.mergeable_state != "clean", opened_prs))

    def _filter_mentions_about_me(self, pr: PullRequest) -> list[PullRequestComment]:
        return list(filter(
            lambda discussion:
            all(reaction.user.login != self.config["me"]
                for reaction in discussion.get_reactions().get_page(0)),
            pr.get_review_comments()
        ))

    def _is_ready_for_review(self, pr: PullRequest) -> bool:
        return not any(review.state == "APPROVED" and review.user.login == self.config["me"] for review in
                       pr.get_reviews())

    def _is_untested(self, pr: PullRequest) -> bool:
        return pr.merged_by and pr.merged_by.login == self.config["me"] and all(
            label.name != "Tested" for label in pr.labels)

    def _prefilter(self) -> list[PullRequest]:
        opened_prs = self.repo.get_pulls(state='open', base='main').get_page(0)
        opened_prs = self._filter_in_case_of_dependabot_prs(opened_prs)
        opened_prs = self._filter_task_for_another_team(opened_prs)
        return opened_prs

    def _collect_ready_for_merge(self, opened_prs: list[PullRequest]):
        main_branch_status = self.repo.get_workflow('default-branch.yaml').get_runs().get_page(0)[0]
        for pr in opened_prs:
            pr_ready_to_merge = ReadyForMerge(self.repo.name, pr.title, pr.html_url, main_branch_status.status,
                                              main_branch_status.conclusion)
            self.results.append(pr_ready_to_merge)
            print(pr_ready_to_merge)

    def _collect_untested(self):
        untested_prs = self.repo.get_pulls(state='closed', base='main').get_page(0)
        for pr in untested_prs:
            if self._is_untested(pr):
                untested = ToTested(self.repo.name, pr.title, pr.html_url)
                self.results.append(untested)
                print(untested)

    def _collect_pr_for_discussion_and_for_review(self, opened_prs: list[PullRequest]):
        for opened_pr in opened_prs:
            if mentions := self._filter_mentions_about_me(opened_pr):
                for mention in mentions:
                    discussion = Discussion(self.repo.name, opened_pr.title, opened_pr.html_url, mention.html_url)
                    self.results.append(discussion)
                    print(discussion)
            elif self._is_ready_for_review(opened_pr):
                ready_for_review = ReadyForReview(self.repo.name, opened_pr.title, opened_pr.html_url)
                self.results.append(ready_for_review)
                print(ready_for_review)

    def collect(self):
        """Get opened pull request for specific repo"""
        opened_prs = self._prefilter()
        self._collect_ready_for_merge(self._filter_ready_for_merge(opened_prs))
        self._collect_pr_for_discussion_and_for_review(self._filter_not_ready_for_merge(opened_prs))
        self._collect_untested()
        return self.results
