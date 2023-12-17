"""Tests collecting ready for review prs"""

from github_notificator.collectors.collectors import Collector
from github_notificator.models.config import Config
from tests.mocks.MockPullRequestProxy import MockPullRequestProxy
from tests.mocks.MockRepositoryProxy import MockRepositoryProxy


class TestReadyForReview:
    def test_ready_for_review(self) -> None:
        ready = MockPullRequestProxy(
            draft=False, author="another", title="ready", labels=["team"], mergeable_state="blocked", merged_by_user="",
            html_url="https", link_to_discussion=[], is_approved=False
            )
        ready_dependabot = MockPullRequestProxy(
            draft=False, author="dependabot[bot]", title="ready_dependabot", labels=["team"], mergeable_state="blocked",
            merged_by_user="", html_url="https", link_to_discussion=[], is_approved=False
            )
        draft = MockPullRequestProxy(
            draft=True, author="me", title="draft", labels=["team"], mergeable_state="blocked", merged_by_user="",
            html_url="https", link_to_discussion=[], is_approved=False
            )
        yours = MockPullRequestProxy(
            draft=False, author="me", title="yours", labels=["team"], mergeable_state="blocked", merged_by_user="",
            html_url="https", link_to_discussion=[], is_approved=False
            )
        another_team = MockPullRequestProxy(
            draft=False, author="another", title="another_team #team3", labels=[], mergeable_state="blocked",
            merged_by_user="", html_url="https", link_to_discussion=[], is_approved=False
            )
        another_team_but_for_you = MockPullRequestProxy(
            draft=False, author="another", title="another_team_but_for_you #team3", labels=["team2"],
            mergeable_state="blocked", merged_by_user="", html_url="https", link_to_discussion=[], is_approved=False
            )
        already_approved = MockPullRequestProxy(
            draft=False, author="another", title="already_approved", labels=["team"], mergeable_state="blocked",
            merged_by_user="", html_url="https", link_to_discussion=[], is_approved=True
            )
        repo = MockRepositoryProxy(
            opened_pull_request=[ready, ready_dependabot, draft, yours, another_team, another_team_but_for_you,
                                 already_approved], closed_pull_request=[], name="name,",
            main_status=("status", "conclusion")
        )

        config: Config = {"me": "me", "special_label": "team2", "dependabot_prs": False, "ignored_pr_labels": ["team3"],
                          "default_branch_workflow_name": "default_branch_workflow_name.yaml"}
        result = Collector(repo, config).collect()

        assert len(result) == 2
        assert result[0].pr_title == "ready"
        assert str(result[0]) == "👀 To review: name, ready https"
        assert result[1].pr_title == "another_team_but_for_you #team3"
        assert str(result[1]) == "👀 To review: name, another_team_but_for_you #team3 https"

    def test_ready_for_review_dependabot(self) -> None:
        ready = MockPullRequestProxy(
            draft=False, author="another", title="ready", labels=["team"], mergeable_state="blocked", merged_by_user="",
            html_url="https", link_to_discussion=[], is_approved=False
            )
        draft = MockPullRequestProxy(
            draft=True, author="another", title="draft", labels=["team"], mergeable_state="blocked", merged_by_user="",
            html_url="https", link_to_discussion=[], is_approved=False
        )
        ready_dependabot = MockPullRequestProxy(
            draft=False, author="dependabot[bot]", title="ready_dependabot", labels=["team"], mergeable_state="blocked",
            merged_by_user="", html_url="https", link_to_discussion=[], is_approved=False
            )

        repo = MockRepositoryProxy(
            opened_pull_request=[ready, draft, ready_dependabot], closed_pull_request=[], name="name,",
            main_status=("status", "conclusion")
            )

        config: Config = {"me": "me", "special_label": "team2", "dependabot_prs": True, "ignored_pr_labels": ["team3"],
                          "default_branch_workflow_name": "default_branch_workflow_name.yaml"}
        result = Collector(repo, config).collect()

        assert len(result) == 2
        assert result[0].pr_title == "ready"
        assert str(result[0]) == "👀 To review: name, ready https"
        assert result[1].pr_title == "ready_dependabot"
        assert str(result[1]) == "👀 To review: name, ready_dependabot https"
