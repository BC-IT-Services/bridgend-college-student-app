from ._anvil_designer import ViewCitizenshipTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ... import Translations

class ViewCitizenship(ViewCitizenshipTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.load_translations()
  
  def load_translations(self):
    self.title.text = Translations.get_translation("Citizenship Information")
    self.message_label.text = f'{Translations.get_translation("Message")}:'
    self.tutor_label.content = f"**{Translations.get_translation('Tutor')}:** {self.item['tutor']}"
    self.date_label.content = f"**{Translations.get_translation('Date set')}:** {self.item['date'].strftime('%A %d/%m/%Y')}"
    self.type_label.text = Translations.get_translation(self.item['type'])