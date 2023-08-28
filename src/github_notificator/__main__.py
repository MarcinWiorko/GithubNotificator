import json
from typing import TypedDict

from github import Auth
from github import Github
from github.PullRequest import PullRequest
from github.PullRequestComment import PullRequestComment


class Config(TypedDict):
    me: str
    special_label: str
    dependabot_prs: bool
    ignored_pr_labels: list[str]
    default_branch_workflow_name: str


with open("github_token.txt") as file:
    token = file.readline()
auth = Auth.Token(token)
g = Github(auth=auth)

repos = []
with open("repos.txt") as file:
    repos.extend(repo.rstrip() for repo in file)

with open("config.json") as file:
    config: Config = json.load(file)

for repo in repos:
    opened_prs = g.get_repo(repo).get_pulls(state='open', base='main').get_page(0)
    if not config["dependabot_prs"]:
        opened_prs = list(  # if you are bot uncomment
            filter(
                lambda pr: not pr.draft and pr.user.login != "dependabot[bot]",
                opened_prs,
            )
        )
    opened_prs = list(
        filter(
            lambda pr: all(devops_thing not in pr.title for devops_thing in config["ignored_pr_labels"]) or any(
                label.name == config["special_label"] for label in pr.labels),
            opened_prs,
        )
    )
    ready_to_merge = list(
        filter(
            lambda pr: pr.mergeable_state == "clean" and pr.user.login == config["me"],
            opened_prs,
        )
    )
    opened_prs: list[PullRequest] = list(filter(lambda pr: pr.mergeable_state != "clean", opened_prs))

    for opened_pr in opened_prs:
        if any(
                f"@{config['me']}" in discussion.body
                and all(
                    reaction.user.login != config["me"]
                    for reaction in discussion.get_reactions().get_page(0)
                )
                for discussion in opened_pr.get_review_comments()
        ):
            discussion_to_resolve: PullRequestComment = list(filter(
                lambda discussion:
                all(reaction.user.login != config["me"]
                    for reaction in discussion.get_reactions().get_page(0)),
                opened_pr.get_review_comments()
            ))[0]
            print(f"🗣️To discuss: {repo} {opened_pr.title} {discussion_to_resolve.html_url}")
        elif not any(review.state == "APPROVED" and review.user.login == config["me"] for review in
                     opened_pr.get_reviews()):
            print(f"👀 To review: {repo} {opened_pr.title} {opened_pr.html_url}")
    main_branch_status = g.get_repo(repo).get_workflow('default-branch.yaml').get_runs().get_page(0)[0]
    for pr in ready_to_merge:
        print(
            f"😎 To merge: {repo} {pr.title} {pr.html_url} Main branch workflow: "
            f"{(main_branch_status.status, main_branch_status.conclusion)} "
            f"{repo.get_workflow(config['default_branch_workflow_name']).html_url}"
        )

    untested_prs = g.get_repo(repo).get_pulls(state='closed', base='main').get_page(0)
    for untested_pr in untested_prs:
        if untested_pr.merged_by and untested_pr.merged_by.login == config["me"] and all(
                label.name != "Tested" for label in untested_pr.labels):
            print(f"🧪 To test: {repo} {untested_pr.title} {untested_pr.html_url}")
