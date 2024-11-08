from ._anvil_designer import HubButtonTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import webbrowser

from ... import Translations

from ... import Tracking

class HubButton(HubButtonTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
  
  def load_translations(self, lang=None):
    self.label.text = Translations.get_translation(self.label_text, lang=lang)
      
  def button_click(self, **event_args):
    """This method is called when the button is clicked"""
    Tracking.send_tracking_request(f"HUB BUTTON CLICK: {self.label_text}")
    webbrowser.open(self.url)
