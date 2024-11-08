from ._anvil_designer import AIChatTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .AI_Message import AI_Message
from .User_Message import User_Message

from .. import Translations

from anvil.js import window

import webbrowser

class AIChat(AIChatTemplate):

  def __init__(self, **properties):
    self.init_components(**properties)
    user = anvil.users.get_user()
    name = user['firstname'] or "stranger"
    email = user['email']

    # Disables chat for staff logins
    try:
      int(email.split('@')[0])
      welcome_message = f"Shwmae, {name}!  I'm here to help you with any questions about **the College** and **your course**.\n\nYou can ask me about the following:\n\n- 📖 Timetables\n\n- 📅 Campus events\n\n- ❓ How to find support\n\n- 🌍 Anything else\n\nI am always improving, so if you have any suggestions please [leave some feedback](https://forms.gle/Jk9uVbfXqs4VfNH6A)!""
    except ValueError:
      welcome_message = "Shwmae! In this space, learners are able to ask questions about their course information, including timetables, targets and citizenship. \n\nThis also functions as a general AI chat, so learners can ask any questions they would of something like Google Gemini or ChatGPT. \n\nThis feature is disabled when in staff preview mode. If you would like a demo, please contact Scott Morgan <smorgan@bridgend.ac.uk>."
      self.prompt_textbox.enabled = False
      self.send_chat_button.enabled = False
    
    # Hard-coded override to enable chat for devs
    if email.split('@')[0] in ['mjdavies','embrown','smorgan']:
      self.prompt_textbox.enabled = True
      self.send_chat_button.enabled = True
      
    self.nav.setup_repeating_convo_panel(user)
    self.conversation_id = properties.get('conversation_id')
    
    if self.conversation_id == None:
      self.add_ai_message(welcome_message, None, feedback_override=False)
      self.title_text.text = ""
    else:
      conversation = anvil.server.call('get_conversation', self.conversation_id)
      self.title_text.text = conversation['label']
      self.load_conversation(conversation)  
      
      self.prompt_textbox.placeholder = "Type a response..."
      self.ai_input_flow_panel.scroll_into_view()

      self.nav.disable_current_conversation_button(self.conversation_id)

    self.banner_utils.setup_utils(user)
    self.load_translations()
    if window.innerWidth < 760:
      self.move_banner_utils()

  def move_banner_utils(self):
    self.banner_utils.remove_from_parent()
    self.nav.insert_nav_item(self.banner_utils)
    self.banner_utils.update_button_role('filled-button')

  def load_conversation(self, conversation):
    conversation_rows = anvil.server.call('load_conversation', conversation)
    for row in conversation_rows:
      self.chat_log.add_component(User_Message(text=row['messagetext']))    
      self.add_ai_message(row['responsetext'], row)
        
  def send_chat_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.call_send_chat_message()

  def call_send_chat_message(self):
    try:
      self.send_chat_message()
    except Exception as e:
      Notification("AI chat currently unavailable.").show()
      print(e)
      return
      
  def send_chat_message(self):
    prompt = self.prompt_textbox.text
    
    if self.check_if_prompt_exceeds_max_character_limit(prompt) is True:
      # exceeds max limit
      return
      
    response = None
    
    if self.conversation_id == None:
      output = anvil.server.call('new_conversation', anvil.users.get_user(), prompt)   
      self.conversation_id = output[0]
      response = output[1]
      message_row = output[2]
  
      conversation = anvil.server.call('get_conversation', self.conversation_id)
      
      self.title_text.text = conversation['label']      
      self.add_conversation_to_nav()
    else:
      output = anvil.server.call('chat_message', anvil.users.get_user(), prompt, self.conversation_id)
      response = output[0]
      message_row = output[1]
      
    self.chat_log.add_component(User_Message(text=prompt))
    message_row = None
    self.add_ai_message(response, message_row)
    
    self.prompt_textbox.text = ""
    self.prompt_textbox.placeholder = "Type a response..."
    self.ai_input_flow_panel.scroll_into_view()
    
    pass


  def add_conversation_to_nav(self):
    self.nav.add_conversation(self.conversation_id)
    self.nav.disable_current_conversation_button(self.conversation_id)
    pass

  def prompt_textbox_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.call_send_chat_message()
    pass

  def add_ai_message(self, text, message_row, feedback_override = True):
    item = {
      'text': text,
      'message_row': message_row,
      'feedback_override': feedback_override
    }
    self.chat_log.add_component(AI_Message(item=item))

  def load_translations(self):
    self.prompt_textbox.placeholder = Translations.get_translation("Type a response...")
    
    self.nav.load_translations()

  def check_if_prompt_exceeds_max_character_limit(self, prompt):
    max_character_limit = 200
    if len(prompt) > max_character_limit:
      gemini_button = Button(text=Translations.get_translation("Ask Gemini your question"), role="filled-button", icon="fa:question")
      gemini_button.add_event_handler('click', self.open_gemini)
      rich_text_data = {
        'error_message': Translations.get_translation("This message exceeds the maximum character limit of {max_character_limit}.").replace("{max_character_limit}", str(max_character_limit)),
        'character_count': f"{len(prompt)}/{max_character_limit}",
        'gemini_button': gemini_button
      }
      rich_text = RichText(content="{error_message}\n{character_count}\n\n{gemini_button}")
      rich_text.data = rich_text_data
      alert(
        title=Translations.get_translation("Max character limit exceeded."),
        content=rich_text,
        large=False,
        dismissible=False,
        buttons=[(Translations.get_translation("Ok"), True)]
      )
      
      return True
    return False

  def open_gemini(self, **event_args):
    webbrowser.open('https://gemini.google.com/app')