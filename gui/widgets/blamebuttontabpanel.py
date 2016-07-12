from gui.widgets.buttontabpanel import ButtonTabPanel


class BlameButtonTabPanel(ButtonTabPanel):
    def update_active_file(self, active_file):
        self._init_tab_panel(data=[active_file])
        super(BlameButtonTabPanel, self).update_active_file(active_file)
