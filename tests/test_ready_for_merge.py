"""Tests collecting ready for merge prs"""
from src.github_notificator.collectors.collectors import Collector
from tests.mocks.MockPullRequestProxy import MockPullRequestProxy
from tests.mocks.MockRepositoryProxy import MockRepositoryProxy


class TestReadyForMerge:
    def test_ready_for_Merge(self):
        ready = MockPullRequestProxy(None, False, "me", "ready", ["team"], "clean", "", "https", [], False)
        not_ready = MockPullRequestProxy(None, False, "me", "not_ready", ["team"], "blocked", "", "https", [], False)
        not_yours = MockPullRequestProxy(None, False, "another", "not_yours", ["team"], "clean", "", "https", [], False)

        repo = MockRepositoryProxy(None, [ready, not_ready, not_yours], [], "name,", ("status", "conclusion"))
        config = {
            "me": "me",
            "special_label": "team2",
            "dependabot_prs": False,
            "ignored_pr_labels": ["team3"],
            "default_branch_workflow_name": "default_branch_workflow_name.yaml"
        }
        result = Collector(repo, config).collect()

        assert len(result) == 1
        assert result[0].pr_title == "ready"
        assert str(result[0]) == "😎 To merge: name, ready https Main branch workflow: ('status', 'conclusion')"
