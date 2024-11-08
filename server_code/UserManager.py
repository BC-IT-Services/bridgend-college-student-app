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
from time import sleep
from decimal import Decimal

@anvil.server.callable
def check_admin():
  return anvil.users.get_user()['admin']

@anvil.server.callable
def get_user_language(user):
  if user['language'] is None:
    user.update(language="english")
  return user['language']

@anvil.server.callable
def set_user_language(user, language):
  user.update(language=language)

@anvil.server.callable
def check_bridgend_college_user():
  sleep(0.1)
  is_bc_user = anvil.users.get_user()['email'].find("@bridgend.ac.uk") != -1
  email = anvil.users.get_user()['email']
  if is_bc_user:
    user_setup() # Check/run first time set up if needed
    return [True, email]
  else:
    process_failed_login(anvil.users.get_user()['email']) # Update failed logins table with failed attempt
    anvil.users.get_user().delete()
    anvil.users.logout()
    return [False, email]

def process_failed_login(user):
  row = app_tables.failed_logins.get(email=user)
  if row is not None:
    row['lastattempt'] = datetime.now()
    row['numattempts'] += 1
    row['lastip'] = anvil.server.context.client.ip
  else:
    row = app_tables.failed_logins.add_row(email=user,firstattempt=datetime.now(), lastattempt=datetime.now(), numattempts=1, lastip=anvil.server.context.client.ip)

def user_setup():
    user = anvil.users.get_user()
    email = user['email']
    row = app_tables.users.get(email=email)

    if row['first_login'] is not None and row['first_login'] is True:
      return
    studentid = email.replace("@bridgend.ac.uk", "")
    row['studentid'] = str(get_safe_student_id(studentid))
    row['first_login'] = True
  
def get_safe_student_id(studentid):
  try:
    int_studentid = int(studentid)
  except Exception:
    int_studentid = 8360 # A test student ID
  return int_studentid

@anvil.server.callable
def get_first_name(studentid):
  try:
    data = anvil.server.call('get_name', person_code=int(studentid))
    first_name = data[0]["Firstname"].split(" ")[0]
    return first_name    
  except Exception as e:
    print(f"-----------------------\nERROR INFO\nFUNCTION: get_first_name\nFUNCTION LOCATION: UserManager (Server) in Anvil\nCALLED FROM: StartUp\nERROR: {e}\n-----------------------")
    return ""
  
@anvil.server.callable
def update_name(user, studentid):
  try:
    data = anvil.server.call('get_name', person_code=get_safe_student_id(studentid))
    first_name = data[0]["Firstname"].split(" ")[0]
    user.update(firstname=first_name)
  except Exception:
    first_name = ""
  return first_name
  
@anvil.server.callable
def add_target(user, target):
  current_targets = user['targets']
  if current_targets is None:
    current_targets = []
  current_targets.append(target)
  user.update(targets=current_targets)

@anvil.server.callable
def update_target(user, target_index, new_target):
  current_targets = user['targets']
  if current_targets is None:
    current_targets = []
  current_targets[target_index].update(
    steps=new_target['steps'],
    target_stats=new_target['target_stats'],
  )
  user.update(targets=current_targets)

@anvil.server.callable
def delete_target(user, target_index):
  current_targets = user['targets']
  if current_targets is None:
    current_targets = []
  del current_targets[target_index]
  user.update(targets=current_targets)
  
@anvil.server.callable
def update_persistent_data(user, data):
  user.update(persistent_data=data)

@anvil.server.callable
def get_persistent_data(user):
  data = user['persistent_data']
  if data is None:
    data = {}
    user.update(persistent_data=data)
  return data

