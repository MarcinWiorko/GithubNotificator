"""Tests collecting ready for merge prs"""
from src.github_notificator.collectors.collectors import Collector
from tests.mocks.MockPullRequestProxy import MockPullRequestProxy
from tests.mocks.MockRepositoryProxy import MockRepositoryProxy


class TestUntested:
    def test_untested(self):
        untested = MockPullRequestProxy(None, False, "me", "title1", ["team"], "clean", "me", "https", [], False)
        other_untested = MockPullRequestProxy(None, False, "another", "title2", ["team"], "clean", "another", "https",
                                              [], False)
        already_tested = MockPullRequestProxy(None, False, "me", "title3", ["team", "Tested"], "clean", "", "https", [],
                                              False)

        repo = MockRepositoryProxy(None, [], [untested, other_untested, already_tested], "name,",
                                   ("status", "conclusion"))
        config = {
            "me": "me",
            "special_label": "team2",
            "dependabot_prs": False,
            "ignored_pr_labels": ["team3"],
            "default_branch_workflow_name": "default_branch_workflow_name.yaml"
        }
        result = Collector(repo, config).collect()

        assert len(result) == 1
        assert result[0].pr_title == "title1"
        assert str(result[0]) == "🧪 To test: name, title1 https"
