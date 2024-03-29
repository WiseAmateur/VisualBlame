from events import ResultConfig, CallConfig


widget_event_listeners = {
    "blame_codelines_list": [ResultConfig(
        event="blame", callers="blame_codelines_list"),
        ResultConfig(event="commit_file", callers="blame_history")],
    "diff_files": ResultConfig(event="diff", callers=[
        "blame_codelines_list", "blame_to_diff", "log_commit_box"]),
    "diff_codelines_list": ResultConfig(event="diff", callers="diff_files"),
    "blame_commit_context": ResultConfig(event="commit_context",
                                         callers=["blame_commit_context",
                                                  "diff_to_blame",
                                                  "blame_history"]),
    "diff_commit_context": ResultConfig(event="commit_context",
                                        callers=["blame_codelines_list",
                                                 "log_commit_box"]),
    "log_commit_history": [ResultConfig(
        event="log", callers=[
            "log_commit_history", "blame_codelines_list", "diff_to_blame",
            "blame_to_diff", "blame_history"]),
        ResultConfig(event="commit_context",
                     callers=["log_commit_history", "diff_to_blame"])]
}

# You have to specify the caller to the widget id already entered as a
# key. This is implemented this way so that the gui only has to pass the
# eventconfig (resulting in less spots to change if eventconfig changes)
widget_event_triggers = {
    "blame_history": [CallConfig(
        event="commit_file", caller="blame_history"),
        CallConfig(event="commit_context", caller="blame_history"),
        CallConfig(event="log", caller="blame_history")],
    "blame_codelines_list": [CallConfig(
        event="blame", caller="blame_codelines_list"),
        CallConfig(event="commit_context", caller="blame_codelines_list"),
        CallConfig(event="diff", caller="blame_codelines_list"),
        CallConfig(event="log", caller="blame_codelines_list")],
    "blame_commit_context": CallConfig(event="commit_context",
                                       caller="blame_commit_context"),
    "log_commit_history": [CallConfig(
        event="log", caller="log_commit_history"),
        CallConfig(event="commit_context", caller="log_commit_history"),
        CallConfig(event="diff", caller="log_commit_box"),
        CallConfig(event="commit_context", caller="log_commit_box")],
    "diff_to_blame": CallConfig(event="log", caller="diff_to_blame"),
    "diff_files": CallConfig(event="diff", caller="diff_files"),
    "blame_to_diff": [CallConfig(event="diff", caller="blame_to_diff"),
                      CallConfig(event="log", caller="blame_to_diff"),
                      CallConfig(event="commit_file", caller="blame_to_diff")]
}
