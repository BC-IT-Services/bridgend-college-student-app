from ._anvil_designer import TargetObjectTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import datetime
from ..ViewTarget import ViewTarget

from ... import Translations

class TargetObject(TargetObjectTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def view_target_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    
    if self.item['set_by'] == "You":
      buttons = [(Translations.get_translation("Delete target"), 0), (Translations.get_translation("Ok"), True)]
    else:
      buttons=[(Translations.get_translation("Ok"), True)]
      
    a = alert(
      ViewTarget(item=self.item),
      large=True,
      dismissible=False,
      buttons=buttons
    )
    # Cant use false for this because the alert is dismissable which i believe returns False if the user clicks anywhere else
    
    if a == 0:
      text = Translations.get_translation("Are you sure you want to delete this target?\n\nThis action cannot be undone.")
      b = alert(
        text,
        title=Translations.get_translation("Delete target"),
        large=True,
        dismissible=True,
        buttons=[(Translations.get_translation("Cancel"), False), (Translations.get_translation("Delete target"), True)])
      if b is True:
        anvil.server.call('delete_target', anvil.users.get_user(), self.item['target_index'])
        get_open_form().setup_target_panel()
    pass

