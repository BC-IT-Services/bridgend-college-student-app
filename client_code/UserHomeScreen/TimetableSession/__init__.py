from ._anvil_designer import TimetableSessionTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ..ViewTimetableSession import ViewTimetableSession

from ... import Translations

class TimetableSession(TimetableSessionTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def view_session_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    a = alert(
      ViewTimetableSession(item=self.item),
      large=True,
      dismissible=False,
      buttons=[(Translations.get_translation("Report absence"), False), (Translations.get_translation("Ok"), True)]
    )
    if a is False:
      self.show_absence_request()
    pass

  def show_absence_request(self):
    get_open_form().absence_request(self.item)
    pass
