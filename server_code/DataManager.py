import anvil.email
import anvil.secrets
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.tz
from datetime import datetime
import anvil.http

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42

@anvil.server.callable
def get_synced_users():
  queued_users = app_tables.users.search(sync_state=3)
  users = []
  for row in queued_users:
    users.append(row['email'])
  return users

@anvil.server.callable
def get_sync_state():
  user = anvil.users.get_user()
  if user:
    if user['sync_state'] is None:
      user['sync_state'] = 0
  return user['sync_state']

@anvil.server.callable
def get_queued_users():
  queued_users = app_tables.users.search(sync_state=1)
  users = []
  for row in queued_users:
    users.append(row['email'])
  return users

@anvil.server.callable
def get_interrupted_syncs():
  queued_users = app_tables.users.search(sync_state=2)
  users = []
  for row in queued_users:
    users.append(row['email'])
  return users

@anvil.server.callable
def update_sync_state():
  user = anvil.users.get_user()
  new_state = 1
  current_state = user['sync_state']
  # If state is 1 through 3 (Queue, in progress, synced), cancel their sync, if not set them to be synced
  if current_state != 0 and current_state != 4:
    new_state = 4
  if user:
    user['sync_state'] = new_state
  return new_state

@anvil.server.callable
def get_unsync_users():
  unsync_users = app_tables.users.search(sync_state=4)
  users = []
  for row in unsync_users:
    users.append(row['email'])
  return users