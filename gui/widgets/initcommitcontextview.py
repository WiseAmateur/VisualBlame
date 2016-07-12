from gui.widgets.commitcontextview import CommitContextView


class InitCommitContextView(CommitContextView):
    # TODO this belongs in a .kv file?
    border_color = [0.25, 0.75, 0.5]

    def init_event_call(self, event_config, function):
        super(InitCommitContextView, self).init_event_call(event_config,
                                                           function)
        self.event_call({"commit_id": "HEAD"})
