import anvil.email
import anvil.secrets
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
import uuid

@anvil.server.callable
def new_conversation(user, prompt):
  new_id = str(uuid.uuid4())

  response = anvil.server.call('new_conversation_uplink', prompt=prompt, conversationid=new_id, userid=int(user["studentid"]))
  app_tables.conversations.add_row(conversationid=new_id,user=user,date_created=datetime.now(), label=response["label"])
  message_row = moderate_prompt(user, response, new_id)
  
  return new_id, response["response"], message_row

@anvil.server.callable
def get_user_conversations(user):
  rows = app_tables.conversations.search(user=user)
  if len(rows) == 0:
    print("User has no conversations!")
    return None  
  return list(reversed(rows))

@anvil.server.callable
def load_conversation(conversation):
  rows = app_tables.messages.search(conversation=conversation)
  if len(rows) == 0:
    print("Conversation not found!")
    return None
  return list(rows)

@anvil.server.callable
def get_conversation(conversation_id):
  return app_tables.conversations.get(conversationid=conversation_id)

def session_exists(conversation_id):
  return anvil.server.call('check_session_exists_uplink', conversationid=conversation_id)

@anvil.server.callable
def chat_message(user, prompt, conversationid):

  conversationhistory=None
  messages = []
  message_row=None
  if not session_exists(conversationid):
    conversationhistory = load_conversation(get_conversation(conversationid))
    for row in conversationhistory:
      messages.append({"author": "user", "content": row["messagetext"]})
      messages.append({"author": "bot", "content": row["responsetext"]})
  chat_response = anvil.server.call('chat_request_uplink', prompt=prompt, conversationid=conversationid, conversationhistory=messages, userid=int(user["studentid"]))
  if "#intent#:" in chat_response["response"]:
    return chat_response["response"]
  else: 
    message_row = moderate_prompt(user, chat_response, conversationid)
  
  return chat_response["response"], message_row
  
@anvil.server.callable
def create_conversation_label(prompt):
  response = anvil.server.call('get_label', prompt=prompt)
  return response

@anvil.server.callable
def add_message_demo(conversationid, user, response, prompt):
  new_id = str(uuid.uuid4())
  conversation = app_tables.conversations.get(conversationid=conversationid)
  row = app_tables.messages.add_row(messageid=new_id, responsetext=response, conversation=conversation, flagged=False, timestamp=datetime.now(), user=user, flagged_reasons=None, messagetext=prompt) 

@anvil.server.callable
def add_conversation_demo(user, prompt):
  new_id = str(uuid.uuid4())
  new_label = anvil.server.call('get_label', prompt=prompt)
  app_tables.conversations.add_row(conversationid=new_id,user=user,date_created=datetime.now(), label=new_label)
  return new_id

def moderate_prompt(user, chat_response, conversationid):
  '''
  moderated_categories = ["Derogatory",
          "Toxic",
          "Violent",
          "Sexual",
          "Insult",
          "Profanity",
          "Death, Harm & Tragedy",
          "Firearms & Weapons",
          "Public Safety",
          "Illicit Drugs",
          "War & Conflict",
          "Dangerous Content"]
  
  moderation_threshold = 0.5
  safety_attributes = chat_response["safetyattributes"][0]
  categories = safety_attributes.get("categories")
  scores = safety_attributes.get("safetyRatings")

  flagged_items = {}
  if categories != None:
    for score in scores:
      if score["category"] in moderated_categories and score["severityScore"] >= 0.5:
        flagged_items.update({score["category"]:score["severityScore"]})
          
  if (safety_attributes.get("blocked")):
    flagged_items.update({"Blocked":"True"})
  '''
  # Dirty - probs should move this to a new method

  #20/05/2024 - Bypassing the above as Google changes have broken it.
  flagged_items = {}
  
  new_id = str(uuid.uuid4())
  conversation = app_tables.conversations.get(conversationid=conversationid)
  row = app_tables.messages.add_row(messageid=new_id, responsetext=chat_response["response"], conversation=conversation, flagged=(flagged_items != {}), timestamp=datetime.now(), user=user, flagged_reasons=str(flagged_items), messagetext=chat_response["prompt"]) 
  return row
  return

@anvil.server.callable
def update_message_feedback(message, feedback):
  message.update(response_feedback=feedback)
  
@anvil.server.callable
def update_message_feedback_reason(message, reason):
  message.update(feedback_reason=reason)
  
