"""Tests collecting discussion to you in prs"""
from github_notificator.collectors.collectors import Collector
from github_notificator.models.config import Config
from tests.mocks.MockPullRequestProxy import MockPullRequestProxy
from tests.mocks.MockRepositoryProxy import MockRepositoryProxy


class TestDiscussion:
    def test_discussion(self) -> None:
        discussion_to_you = MockPullRequestProxy(draft=False, author="another", title="discussion_to_you",
                                                 labels=["team"], mergeable_state="blocked", merged_by_user="",
                                                 html_url="https", link_to_discussion=["https2"], is_approved=False)
        discussion_in_your_pr = MockPullRequestProxy(draft=False, author="me", title="discussion_in_your_pr",
                                                     labels=["team"], mergeable_state="blocked",
                                                     merged_by_user="another", html_url="https",
                                                     link_to_discussion=["https2"], is_approved=False)
        draft_discussion_in_your_pr = MockPullRequestProxy(draft=True, author="me", title="draft_discussion_in_your_pr",
                                                           labels=["team"], mergeable_state="clean",
                                                           merged_by_user="another", html_url="https",
                                                           link_to_discussion=["https2"], is_approved=False)
        draft_discussion_to_you = MockPullRequestProxy(draft=True, author="another", title="draft_discussion_to_you",
                                                       labels=["team"], mergeable_state="clean",
                                                       merged_by_user="another", html_url="https",
                                                       link_to_discussion=["https2"], is_approved=False)

        repo = MockRepositoryProxy(
            opened_pull_request=[discussion_to_you, discussion_in_your_pr, draft_discussion_in_your_pr,
                                 draft_discussion_to_you], closed_pull_request=[], name="name,",
            main_status=("status", "conclusion"))

        config: Config = {"me": "me", "special_label": "team2", "dependabot_prs": False, "ignored_pr_labels": ["team3"],
                          "default_branch_workflow_name": "default_branch_workflow_name.yaml"}
        result = Collector(repo, config).collect()

        assert len(result) == 2
        assert result[0].pr_title == "discussion_to_you"
        assert str(result[0]) == "🗣️To discuss: name, discussion_to_you https2"
        assert result[1].pr_title == "discussion_in_your_pr"
        assert str(result[1]) == "🗣️To discuss: name, discussion_in_your_pr https2"
