from gui.widgets.commitcontextview import CommitContextView


class InitCommitContextView(CommitContextView):
    def init_event_call(self, event_config, function):
        super(InitCommitContextView, self).init_event_call(event_config,
                                                           function)
        self.event_call({"commit_id": "HEAD"})
