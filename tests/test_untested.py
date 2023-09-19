"""Tests collecting ready for merge prs"""
from src.github_notificator.collectors.collectors import Collector
from tests.mocks.MockPullRequestProxy import MockPullRequestProxy
from tests.mocks.MockRepositoryProxy import MockRepositoryProxy


class TestUntested:
    def test_untested(self):
        untested = MockPullRequestProxy(draft=False, author="me", title="title1", labels=["team"],
                                        mergeable_state="clean", merged_by_user="me", html_url="https",
                                        link_to_discussion=[], is_approved=False)
        other_untested = MockPullRequestProxy(draft=False, author="another", title="title2", labels=["team"],
                                              mergeable_state="clean", merged_by_user="another", html_url="https",
                                              link_to_discussion=[], is_approved=False)
        already_tested = MockPullRequestProxy(draft=False, author="me", title="title3", labels=["team", "Tested"],
                                              mergeable_state="clean", merged_by_user="me", html_url="https",
                                              link_to_discussion=[], is_approved=False)

        repo = MockRepositoryProxy(opened_pull_request=[],
                                   closed_pull_request=[untested, other_untested, already_tested],
                                   name="name,", main_status=("status", "conclusion"))

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
