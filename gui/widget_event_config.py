from events import ResultConfig, CallConfig


widget_event_listeners = {
  "blame_codelines_list": ResultConfig(event="blame", callers="blame_codelines_list"),
  "diff_files": ResultConfig(event="diff", callers="blame_codelines_list"),
  "blame_commit_context": ResultConfig(event="commit_context", callers="diff_to_blame"),
  "diff_commit_context": ResultConfig(event="commit_context", callers="blame_codelines_list")
}

# You have to specify the caller to the widget id already entered as a
# key. This is implemented this way so that the gui only has to pass the
# eventsconfig (resulting in less spots to change if eventsconfig changes)
widget_event_triggers = {
  "blame_codelines_list": CallConfig(events={"blame": [{"commit_context": []}, {"diff": []}]},
                                     caller="blame_codelines_list", result_args="commit_id")
}
