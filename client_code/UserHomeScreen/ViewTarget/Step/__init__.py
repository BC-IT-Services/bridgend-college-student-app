from ._anvil_designer import StepTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .... import Translations

class Step(StepTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.lang = get_open_form().lang
    self.status_dropdown.enabled = self.item['parent'].item['set_by'] == "You"
    self.set_dropdown_options()
    self.set_dropdown_color(self.item['step']['status'])

  def set_dropdown_options(self):
    self.status_dropdown.items = [
      (Translations.get_translation("Not started", self.lang), "Not started"),
      (Translations.get_translation("In progress", self.lang), "In progress"),
      (Translations.get_translation("Complete", self.lang), "Complete")
    ]

  def status_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    self.parent.parent.parent.update_step_status(self.item['index'], self.status_dropdown.selected_value)
    self.set_dropdown_color(self.status_dropdown.selected_value)
    pass

  def set_dropdown_color(self, status):
    if status == "Not started":
      new_background_color = "var(--red)"
    elif status == "In progress":
      new_background_color = "var(--yellow)"
    elif status == "Complete":
      new_background_color = "var(--green)"
    self.status_dropdown.background = new_background_color
    
