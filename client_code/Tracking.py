import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

def send_tracking_request(tracking_key, value_addition=1):
  """Takes in a key and value to store in the database.

  Args:
    tracking_key = expected a string that can be used a key in the database.
    value_addition = the value to be added to the tracking key, defaults to 1.

  Returns:
    if successful, the new value (int) of the key will be returned, else a False value and the error will be printed to the console.
  """

  try:
    tracking_data = anvil.server.call('get_tracking_data', tracking_key)
    anvil.server.call('update_tracking_key_value', tracking_data, value_addition)
    return tracking_data['value']
  except Exception as e:
    print(e)
    return False
  
  
  


