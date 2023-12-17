from github_notificator.models.results import Discussion, ReadyForMerge


class TestDiscussion:
    def test_create_discussion(self) -> None:
        discussion = Discussion(repo="", pr_title="", pr_link="")
        assert discussion.prefix == "🗣️To discuss"
        assert discussion.discussion_to_resolve_link == ""


class TestReadyForMerge:
    def test_create_ready_for_merge(self) -> None:
        ready_for_merge = ReadyForMerge(repo="", pr_title="", pr_link="")
        assert ready_for_merge.prefix == "😎 To merge"
        assert ready_for_merge.main_branch_status == ('', '')

    def test_succeed_and_completed_previous_workflow(self) -> None:
        ready_for_merge = ReadyForMerge(repo="", pr_title="", pr_link="", main_branch_status=("succeed", "completed"))
        assert str(ready_for_merge) == "😎 To merge:    Main branch workflow: 🟢 ('succeed', 'completed')"

    def test_succeed_and_not_completed_previous_workflow(self) -> None:
        ready_for_merge = ReadyForMerge(
            repo="", pr_title="", pr_link="", main_branch_status=("succeed", "not completed")
            )
        assert str(ready_for_merge) == "😎 To merge:    Main branch workflow: 🔴 ('succeed', 'not completed')"

    def test_not_succeed_and_completed_previous_workflow(self) -> None:
        ready_for_merge = ReadyForMerge(
            repo="", pr_title="", pr_link="", main_branch_status=("not succeed", "completed")
            )
        assert str(ready_for_merge) == "😎 To merge:    Main branch workflow: 🔴 ('not succeed', 'completed')"

    def test_not_succeed_and_not_completed_previous_workflow(self) -> None:
        ready_for_merge = ReadyForMerge(
            repo="", pr_title="", pr_link="", main_branch_status=("not succeed", "not completed")
            )
        assert str(ready_for_merge) == "😎 To merge:    Main branch workflow: 🔴 ('not succeed', 'not completed')"
