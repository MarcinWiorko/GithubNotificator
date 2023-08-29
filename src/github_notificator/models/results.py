"""The file for various result of message to user"""
from dataclasses import dataclass


@dataclass
class Result:
    repo: str
    pr_title: str
    pr_link: str

    def __str__(self):
        raise NotImplemented


@dataclass
class Discussion(Result):
    """Message about that you were mentioned in discussion"""
    discussion_to_resolve_link: str

    def __str__(self):
        return f"🗣️To discuss: {self.repo} {self.pr_title} {self.discussion_to_resolve_link}"


@dataclass
class ReadyForMerge(Result):
    """Message that your pr is ready for merge"""
    main_branch_status: str
    main_branch_conclusion: str

    def __str__(self):
        return f"😎 To merge: {self.repo} {self.pr_title} {self.pr_link} Main branch workflow: " \
               f"{(self.main_branch_status, self.main_branch_conclusion)} "


class ReadyForReview(Result):
    """Message that this PR is ready for your review"""

    def __str__(self):
        return f"👀 To review: {self.repo} {self.pr_title} {self.pr_link}"


class ToTested(Result):
    """Message that your pr is not tested"""

    def __str__(self):
        return f"🧪 To test: {self.repo} {self.pr_title} {self.pr_link}"
