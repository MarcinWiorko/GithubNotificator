def pre_mutation(context):
    if context.filename in ["src/github_notificator/__main__.py", "src/github_notificator/models/PyGithubProxy.py"]:
        context.skip = True
    elif context.current_source_line.strip().startswith('print('):
        context.skip = True
