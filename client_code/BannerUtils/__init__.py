from ._anvil_designer import BannerUtilsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import Translations
import webbrowser

class BannerUtils(BannerUtilsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    
  def setup_utils(self, user):
    self.user = user
    lang = anvil.server.call('get_user_language', user)
    if lang == "english":
      self.change_language_button.text = "Cymraeg"
    elif lang == "cymraeg":
      self.change_language_button.text = "English"

    self.feedback_button.text = Translations.get_translation("Feedback")

  def change_language_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    lang = anvil.server.call('get_user_language', self.user)
    if lang == "english":
      new_lang = "cymraeg"
    elif lang == "cymraeg":
      new_lang = "english"
    anvil.server.call('set_user_language', self.user, new_lang)
    self.setup_utils(self.user)
    # update the current open form
    # for this to run, you need the parent from that's open to have a function with this
    # signature, as long as it has this func, it shouldn't trigger the except
    try:
      get_open_form().load_translations()
    except Exception:
      print('NO FUNCTION "load_translations(lang)" ON OPEN FORM')

  def feedback_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    webbrowser.open('')
    pass
    
  def update_button_role(self, role):
    self.feedback_button.role = role
    self.change_language_button.role = role