from ._anvil_designer import NavTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import webbrowser

from .ConversationObject import ConversationObject

from .. import Translations
from datetime import datetime

class Nav(NavTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def load_translations(self, lang=None):
    self.home_button.text = Translations.get_translation("Home", lang=lang)
    self.hub_button.text = Translations.get_translation("Hub", lang=lang)
    self.safeguarding_button.text = Translations.get_translation("Report a concern", lang=lang)
    self.new_chat_button.text = Translations.get_translation("New chat", lang=lang)

  def setup_repeating_convo_panel(self, user):
    conversations = anvil.server.call('get_user_conversations', user)
    self.conversation_row_limiter.set_items(conversations, ConversationObject)

  def disable_current_conversation_button(self, conversation_id):
    conversation_buttons = self.conversation_row_limiter.row_holder.get_components()
    for i in range(len(conversation_buttons)):
      if conversation_buttons[i].item['conversationid'] == conversation_id:
        state = "Inactive"
      else:
        state = "Active"
      conversation_buttons[i].set_state(state) 

  def add_conversation(self, conversation_id):
      if not hasattr(self, "repeating_conversations"):
          self.repeating_conversations = []
      
      new_conversation = anvil.server.call('get_conversation', conversation_id)
      self.repeating_conversations.insert(0, new_conversation)
  
  def new_chat_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('AIChat', conversation_id = None)

  def home_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if "UserHomeScreen" not in str(get_open_form()):
      open_form('UserHomeScreen', initialise=False)
    pass

  def safeguarding_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    webbrowser.open('')
    pass
    
  def hub_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if "Hub" not in str(get_open_form()):
      open_form('Hub')
    pass
    
  def insert_nav_item(self, item):
    self.inserted_items.add_component(item)
