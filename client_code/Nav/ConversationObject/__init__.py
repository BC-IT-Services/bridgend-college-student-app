from ._anvil_designer import ConversationObjectTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ConversationObject(ConversationObjectTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.set_state("Active")

  def set_state(self, state):
    self.state = state
    self.view_conversation_button.enabled = self.state == "Active"
  
  def view_conversation_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # open convo
    if self.state == "Active":
      open_form('AIChat', conversation_id = self.item['conversationid'])
    else:
      n = Notification("You're already viewing that conversation!")
      n.show()
