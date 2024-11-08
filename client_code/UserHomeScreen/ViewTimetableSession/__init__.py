from ._anvil_designer import ViewTimetableSessionTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.tz
from ... import Translations
import datetime

from webbrowser import open

class ViewTimetableSession(ViewTimetableSessionTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.check_success_hub()
    self.get_and_set_map_image()
    self.load_translations()

  def check_success_hub(self):
    self.success_hub_button.visible = "Success Centre" in self.item['room']

  def load_translations(self):
    self.title_label.text = Translations.get_translation("Session information")
    self.room_label.content = f"**{Translations.get_translation('Room')}:** {self.item['room']}"
    self.session_title_label.content = f"**{Translations.get_translation('Session title')}:** {self.item['session_title']}"
    #self.tutor_label.content = f"**{Translations.get_translation('Tutor')}:** {self.item['tutor']}"
    self.session_time_label.content = f"**{Translations.get_translation('Time')}:** {self.item['start_time'].strftime('%H:%M')} - {self.item['end_time'].strftime('%H:%M')}"
    self.map_info_label.text = Translations.get_translation("Where is this session?")
    self.session_time_info_label.text = self.get_session_time_info()

  def get_session_time_info(self):
    start_time = self.item['start_time']
    end_time = self.item['end_time']
    return self.time_difference(start_time, end_time)

  def time_difference(self, start_time, end_time):
    start_time = datetime.datetime(start_time.year, start_time.month, start_time.day, start_time.hour, start_time.minute, start_time.second, start_time.microsecond, tzinfo=anvil.tz.tzlocal())
    end_time = datetime.datetime(end_time.year, end_time.month, end_time.day, end_time.hour, end_time.minute, end_time.second, end_time.microsecond, tzinfo=anvil.tz.tzlocal())
    now = datetime.datetime.now(tz=anvil.tz.tzlocal())

    if start_time > now:
      difference = start_time - now
      time_str = []
      if difference.days > 0:
        time_str.append(f"{difference.days} {Translations.get_translation('days')}")
      if difference.seconds // 3600 > 0:
        time_str.append(f"{difference.seconds // 3600} {Translations.get_translation('hours')}")
      if (difference.seconds % 3600) // 60 > 0:
        time_str.append(f"{(difference.seconds % 3600) // 60} {Translations.get_translation('minutes')}")
      if len(time_str) == 1:
        return f"{Translations.get_translation('Starts in')} {time_str[0]}"
      else:
        return f"{Translations.get_translation('Starts in')} {', '.join(time_str)}"

    if end_time > now:
      difference = now - start_time
      time_str = []
      if difference.days > 0:
        time_str.append(f"{difference.days} {Translations.get_translation('days')}")
      if difference.seconds // 3600 > 0:
        time_str.append(f"{difference.seconds // 3600} {Translations.get_translation('hours')}")
      if (difference.seconds % 3600) // 60 > 0:
        time_str.append(f"{(difference.seconds % 3600) // 60} {Translations.get_translation('minutes')}")
      if len(time_str) == 1:
        return f"{Translations.get_translation('Started')} {time_str[0]} {Translations.get_translation('ago')}"
      else:
        return f"{Translations.get_translation('Started')} {', '.join(time_str)} {Translations.get_translation('ago')}"
  
    difference = now - end_time   
    time_str = []
    if difference.days > 0:
      time_str.append(f"{difference.days} {Translations.get_translation('days')}")
    if difference.seconds // 3600 > 0:
      time_str.append(f"{difference.seconds // 3600} {Translations.get_translation('hours')}")
    if (difference.seconds % 3600) // 60 > 0:
      time_str.append(f"{(difference.seconds % 3600) // 60} {Translations.get_translation('minutes')}")
    if len(time_str) == 1:
      return f"{Translations.get_translation('Ended')} {time_str[0]} {Translations.get_translation('ago')}"
    else:
      return f"{Translations.get_translation('Ended')} {', '.join(time_str)} {Translations.get_translation('ago')}"
  
  def get_and_set_map_image(self):
    room_record = app_tables.rooms.get(room_code=self.item['room'])
    if room_record is None:
      self.map_image.visible = False
      self.map_info_label.visible = False
      return

    self.map_image.source = room_record['map_url']

  def success_hub_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open("")
    pass
      