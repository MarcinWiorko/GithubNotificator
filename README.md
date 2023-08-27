# GithubNotificator

## Description:

The tool for notification you about:
* your discussion to resove or answer
* your pull requests to merge
* pull requests to review according to:
   * if you want to review dependabot's pull requests
   * if they are not approve by you
   * if they don't have special word in a title of pull request which will indicate they are not for you
 
## Config files
* `cofing.json` contains key-value structure:
  * `me` [str] - your login in github, also a name which people use to notify you
  * `special_label` [str] - label which indicates that someone need your review or your team
  * `dependabot_prs` [bool] - do you want to review dependabot's pull requests
  * `ignored_pr_labels` [list of str] - labels in a title of pull request that indicate that this pull request is not for you
  * `default_branch_workflow_name` [str] - name of the file containg workflow after merge to indicate if you can merge your pull request based on the result of the latest run
