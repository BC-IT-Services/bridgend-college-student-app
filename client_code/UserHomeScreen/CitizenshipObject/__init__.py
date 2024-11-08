from ._anvil_designer import CitizenshipObjectTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import datetime

from ..ViewCitizenship import ViewCitizenship

from ... import Translations

class CitizenshipObject(CitizenshipObjectTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.


  def view_citizenship_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    a = alert(
      ViewCitizenship(item=self.item),
      large=True,
      dismissible=False,
      buttons=[(Translations.get_translation("Ok"), True)]
    )
    pass