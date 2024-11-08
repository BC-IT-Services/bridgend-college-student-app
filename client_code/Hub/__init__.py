from ._anvil_designer import HubTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import Translations

from anvil.js import window

class Hub(HubTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.user = anvil.users.get_user()
    self.nav.setup_repeating_convo_panel(self.user)
    self.banner_utils.setup_utils(self.user)
    self.load_translations()
    if window.innerWidth < 760:
      self.move_banner_utils()

  def move_banner_utils(self):
    self.banner_utils.remove_from_parent()
    self.nav.insert_nav_item(self.banner_utils)
    self.banner_utils.update_button_role('filled-button')

  def load_translations(self):
    lang = anvil.server.call('get_user_language', self.user)
    hub_buttons = [
      self.west_button
    ]
    self.info_label.text = Translations.get_translation("Welcome to your College Hub. Here you can access useful resources and sites.", lang=lang)
    self.nav.load_translations(lang=lang)

    for button in hub_buttons:
      button.load_translations(lang=lang)
    
    