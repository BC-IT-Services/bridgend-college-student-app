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
def send_absence_email(to, cc, subject, html):
  print(f"Absence logged: {to} {cc} {subject} {html}")
  anvil.google.mail.send(
    to=to,
    cc=cc,
    subject=subject,
    html=html
  )
