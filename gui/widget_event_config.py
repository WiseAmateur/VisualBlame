from events import ResultConfig, CallConfig


widget_event_listeners = {
  "blame_codelines_list": ResultConfig(event="blame", callers="blame_codelines_list"),
  "diff_files": ResultConfig(event="diff", callers="blame_codelines_list"),
  "diff_codelines_list": ResultConfig(event="diff", callers="diff_files"),
  "blame_commit_context": ResultConfig(event="commit_context", callers=["blame_commit_context", "diff_to_blame"]),
  "diff_commit_context": ResultConfig(event="commit_context", callers="blame_codelines_list"),
  "log_commit_history": [ResultConfig(event="log", callers=["log_commit_history", "blame_codelines_list", "diff_to_blame"]),
                         ResultConfig(event="commit_context", callers=["log_commit_history", "diff_to_blame"])]
}

# You have to specify the caller to the widget id already entered as a
# key. This is implemented this way so that the gui only has to pass the
# eventconfig (resulting in less spots to change if eventconfig changes)
widget_event_triggers = {
  "blame_codelines_list": CallConfig(events={"blame": [{"commit_context": []}, {"diff": []},
                                                       {"log": []}]},
                                     caller="blame_codelines_list", result_args="commit_id"),
  "blame_commit_context": CallConfig(events="commit_context", caller="blame_commit_context"),
  "log_commit_history": [CallConfig(events="log", caller="log_commit_history"),
                         CallConfig(events="commit_context", caller="log_commit_history")],
  "diff_to_blame": CallConfig(events="log", caller="diff_to_blame"),
  "diff_files": CallConfig(events="diff", caller="diff_files")
}
