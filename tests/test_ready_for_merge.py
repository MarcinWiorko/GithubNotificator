"""Tests collecting ready for merge prs"""
from src.github_notificator.collectors.collectors import Collector
from tests.mocks.MockPullRequestProxy import MockPullRequestProxy
from tests.mocks.MockRepositoryProxy import MockRepositoryProxy


class TestReadyForMerge:
    def test_ready_for_Merge(self):
        ready = MockPullRequestProxy(draft=False, author="me", title="ready", labels=["team"], mergeable_state="clean",
                                     merged_by_user="", html_url="https", link_to_discussion=[], is_approved=False)
        not_ready = MockPullRequestProxy(draft=False, author="me", title="not_ready", labels=["team"],
                                         mergeable_state="blocked", merged_by_user="", html_url="https",
                                         link_to_discussion=[], is_approved=False)
        not_yours = MockPullRequestProxy(draft=False, author="another", title="not_yours", labels=["team"],
                                         mergeable_state="clean", merged_by_user="", html_url="https",
                                         link_to_discussion=[], is_approved=False)

        repo = MockRepositoryProxy(opened_pull_request=[ready, not_ready, not_yours], closed_pull_request=[],
                                   name="name,", main_status=("status", "conclusion"))

        config = {"me": "me", "special_label": "team2", "dependabot_prs": False, "ignored_pr_labels": ["team3"],
                  "default_branch_workflow_name": "default_branch_workflow_name.yaml"}
        result = Collector(repo, config).collect()

        assert len(result) == 2
        assert result[0].pr_title == "ready"
        assert str(result[0]) == "😎 To merge: name, ready https Main branch workflow: ('status', 'conclusion')"
