from ._anvil_designer import User_MessageTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class User_Message(User_MessageTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    first_name = anvil.users.get_user()['firstname']
    initial = ""
    if first_name != None:
      initial = first_name[0]

    self.first_name_label.text = initial
    