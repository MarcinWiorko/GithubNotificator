def pre_mutation(context):
    if context.filename in ["github_notificator/__main__.py", "github_notificator/models/PyGithubProxy.py"]:
        context.skip = True
    elif context.current_source_line.strip().startswith("print(") or context.current_source_line.strip().startswith(
            "with open(") or context.current_source_line.strip().startswith("webbrowser.open("):
        context.skip = True
