from ._anvil_designer import RepeatingStepTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ... import Translations

class RepeatingStep(RepeatingStepTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.delete_button.text = Translations.get_translation("Delete")

  def step_input_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.parent.parent.parent.update_step(self.item['index'], self.step_input.text)
    pass

  def delete_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.parent.parent.parent.delete_step(self.item['index'])
    pass
