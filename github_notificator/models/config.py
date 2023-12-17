"""File with config representation"""
from typing import TypedDict


class Config(TypedDict):
    """Representation of the configuration"""
    me: str
    special_label: str
    dependabot_prs: bool
    ignored_pr_labels: list[str]
    default_branch_workflow_name: str
