

# TODO one list for registering, one list for triggering
widget_event_listeners = {
                         "blame_codelines_list": {"caller": "", "event": "blame"},
                         "diff_files": {"caller": "", "event": "diff"},
                         "blame_commit_context": {"caller": "diff_to_blame", "event": "commit_context"},
                         "diff_commit_context": {"caller": "blame_codelines_list", "event": "commit_context"}
                       }

widget_event_triggers = {
  "blame_codelines_list": "blame"
  # "blame_codelines_list": {"trigger1": ["trigger2 using trigger1 data", "trigger3 using trigger1 data"]}
}
