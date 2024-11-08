from ._anvil_designer import AI_MessageTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class AI_Message(AI_MessageTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.load_feedback_section()

  def load_feedback_section(self):
    if self.item['message_row'] == None:
      return
    response_feedback = self.item['message_row']['response_feedback']
    feedback_response = self.item['message_row']['feedback_reason']
    if response_feedback == None:
      self.load_feedback_items(True, False, False)
    elif response_feedback == "Good":
      self.load_feedback_items(False, False, False)
    elif response_feedback == "Bad":
      self.load_feedback_items(False, False, False)
      
  def load_feedback_items(self, feedback_panel, bad, good):
    if feedback_panel == False:
      self.spacer_2.visible = False
    self.response_feedback_panel.visible = feedback_panel
    self.bad_feedback_reason_panel.visible = bad
    self.good_feedback_panel.visible = good

  def good_response_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call('update_message_feedback', self.item['message_row'], "Good")
    self.load_feedback_items(False, False, True)

  def bad_response_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    print(self.item['message_row'])
    anvil.server.call('update_message_feedback', self.item['message_row'], "Bad")
    self.load_feedback_items(False, True, False)

  def reason_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    feedback_reason = self.reason_dropdown.selected_value
    anvil.server.call('update_message_feedback_reason', self.item['message_row'], feedback_reason)
    

      
      
      
