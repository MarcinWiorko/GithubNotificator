"""Tests collecting discussion to you in prs"""
from src.github_notificator.collectors.collectors import Collector
from tests.mocks.MockPullRequestProxy import MockPullRequestProxy
from tests.mocks.MockRepositoryProxy import MockRepositoryProxy


class TestDiscussion:
    def test_discussion(self):
        discussion_to_you = MockPullRequestProxy(None, False, "another", "discussion_to_you", ["team"], "blocked", "",
                                                 "https",
                                                 ["https2"], False)
        discussion_in_your_pr = MockPullRequestProxy(None, False, "me", "discussion_in_your_pr", ["team"], "blocked",
                                                     "another", "https",
                                                     ["https2"], False)
        draft_discussion_in_your_pr = MockPullRequestProxy(None, True, "me", "draft_discussion_in_your_pr", ["team"],
                                                           "clean", "another", "https",
                                                           ["https2"], False)
        draft_discussion_to_you = MockPullRequestProxy(None, True, "another", "draft_discussion_to_you", ["team"],
                                                       "clean", "", "https",
                                                       ["https2"], False)

        repo = MockRepositoryProxy(None, [discussion_to_you, discussion_in_your_pr,
                                          draft_discussion_in_your_pr, draft_discussion_to_you], [],
                                   "name,", ("status", "conclusion"))
        config = {
            "me": "me",
            "special_label": "team2",
            "dependabot_prs": False,
            "ignored_pr_labels": ["team3"],
            "default_branch_workflow_name": "default_branch_workflow_name.yaml"
        }
        result = Collector(repo, config).collect()

        assert len(result) == 2
        assert result[0].pr_title == "discussion_to_you"
        assert str(result[0]) == "🗣️To discuss: name, discussion_to_you https2"
        assert result[1].pr_title == "discussion_in_your_pr"
        assert str(result[1]) == "🗣️To discuss: name, discussion_in_your_pr https2"
