"""Tests collecting ready for review prs"""
from src.github_notificator.collectors.collectors import Collector
from tests.mocks.MockPullRequestProxy import MockPullRequestProxy
from tests.mocks.MockRepositoryProxy import MockRepositoryProxy


class TestReadyForReview:
    def test_ready_for_review(self):
        ready = MockPullRequestProxy(None, False, "another", "ready", ["team"], "blocked", "", "https", [], False)
        draft = MockPullRequestProxy(None, True, "me", "draft", ["team"], "blocked", "", "https", [], False)
        yours = MockPullRequestProxy(None, False, "me", "yours", ["team"], "blocked", "", "https", [], False)
        another_team = MockPullRequestProxy(None, False, "another", "another_team #team3", [], "blocked", "", "https",
                                            [],
                                            False)
        another_team_but_for_you = MockPullRequestProxy(None, False, "another", "another_team_but_for_you #team3",
                                                        ["team2"], "blocked",
                                                        "", "https", [], False)
        already_approved = MockPullRequestProxy(None, False, "another", "already_approved", ["team"], "blocked", "",
                                                "https", [],
                                                True)
        repo = MockRepositoryProxy(None,
                                   [ready, draft, yours, another_team, another_team_but_for_you, already_approved], [],
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
        assert result[0].pr_title == "ready"
        assert str(result[0]) == "👀 To review: name, ready https"
        assert result[1].pr_title == "another_team_but_for_you #team3"
        assert str(result[1]) == "👀 To review: name, another_team_but_for_you #team3 https"
