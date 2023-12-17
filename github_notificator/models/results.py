"""The file for various result of message to user"""
from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class Result:
    repo: str
    pr_title: str
    pr_link: str
    prefix: ClassVar[str]

    def __str__(self) -> str:
        raise NotImplementedError  # pragma: no cover

    def get_paragraph_html(self) -> str:
        return f"<p>{self.prefix}: {self.repo} <a href='{self.pr_link}'>{self.pr_title}</a></p>"


@dataclass
class Discussion(Result):
    """Message about that you were mentioned in discussion"""
    discussion_to_resolve_link: str = ""
    prefix: ClassVar[str] = "🗣️To discuss"

    def __str__(self) -> str:
        return f"{self.prefix}: {self.repo} {self.pr_title} {self.discussion_to_resolve_link}"

    def get_paragraph_html(self) -> str:
        return (f"<p>{self.prefix}: {self.repo} <a href='{self.pr_link}'>{self.pr_title}</a>"
                f"&nbsp;<a href='{self.discussion_to_resolve_link}'>Discussion</a></p>")


@dataclass
class ReadyForMerge(Result):
    """Message that your pr is ready for merge"""
    main_branch_status: tuple[str, str] = field(default_factory=lambda: ("", ""))
    prefix: ClassVar[str] = "😎 To merge"

    def _interpreter_status_main_workflow(self) -> str:
        if self.main_branch_status[0] == "succeed" and self.main_branch_status[1] == "completed":
            return "🟢"
        else:
            return "🔴"

    def __str__(self) -> str:
        return f"{self.prefix}: {self.repo} {self.pr_title} {self.pr_link} Main branch workflow: " \
               f"{self._interpreter_status_main_workflow()} {(self.main_branch_status[0], self.main_branch_status[1])}"

    def get_paragraph_html(self) -> str:
        return (f"<p>{self.prefix}: {self.repo} <a href='{self.pr_link}'>{self.pr_title}</a>"
                f'&nbsp;<span class="tooltip">Main branch: {self._interpreter_status_main_workflow()}'
                f'<span class="tooltiptext">'
                f'{self.main_branch_status[0]} {self.main_branch_status[1]}'
                f'</span></span></p>')



class ReadyForReview(Result):
    """Message that this PR is ready for your review"""
    prefix: ClassVar[str] = "👀 To review"

    def __str__(self) -> str:
        return f"{self.prefix}: {self.repo} {self.pr_title} {self.pr_link}"


class ToTested(Result):
    """Message that your pr is not tested"""
    prefix: ClassVar[str] = "🧪 To test"

    def __str__(self) -> str:
        return f"{self.prefix}: {self.repo} {self.pr_title} {self.pr_link}"
