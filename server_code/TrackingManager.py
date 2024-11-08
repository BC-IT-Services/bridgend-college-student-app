import anvil.email
import anvil.secrets
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def update_tracking_key_value(tracking_data, value_addition):
  tracking_data.update(value=tracking_data['value'] + value_addition)

@anvil.server.callable
def get_tracking_data(tracking_key):
  tracking_data = app_tables.tracking.get(field=tracking_key)
  if tracking_data is None:
    tracking_data = app_tables.tracking.add_row(field=tracking_key, value=0)
  return tracking_data