from gui.widgets.buttontabpanel import ButtonTabPanel


class BlameButtonTabPanel(ButtonTabPanel):
  def update_active_file(self, active_file):
    self.active_file = active_file

    self.process_event_result(data=[active_file])
