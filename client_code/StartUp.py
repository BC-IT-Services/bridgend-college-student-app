import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import *
# Small change, but still saves some overhead on the import
from time import sleep 

import random
import string

def startup():

  if app_tables.misc.get(field="maintenance_in_progress")['bool'] is True:
    if anvil.app.environment.tags == ['debug']:
      print("Skipping Maintenance screen: App running from designer.")
    else:
      open_form('Maintenance')
      return
      
  sleep(0.01)
  
  if not anvil.users.get_user():
    anvil.users.login_with_form(show_signup_option=False, remember_by_default=True, allow_cancel=False)
  user = anvil.users.get_user()
  valid_user = anvil.server.call('check_bridgend_college_user')
  
  if not valid_user[0]:
    email = valid_user[1]
    anvil.users.logout()
    #Move them to a error screen
    open_form('ProhibitedUserScreen', email=email)
    return

  # Set the users name
  first_name = anvil.server.call('update_name', user, user['studentid']) # Not currently used here
  open_form('UserHomeScreen', initialise=True)
  
startup()
