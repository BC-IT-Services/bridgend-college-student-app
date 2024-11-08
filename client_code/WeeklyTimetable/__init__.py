from ._anvil_designer import WeeklyTimetableTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import datetime

from ..UserHomeScreen.TimetableSession import TimetableSession
from .. import Translations

from anvil.js import window

class WeeklyTimetable(WeeklyTimetableTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    # these are split in 2, the week offset is to allow me to account for it being saturday, so just to put it forward by 1
    # the user controlled one lets them cycle through weeks
    self.user_controlled_offset = 0
    self.week_offset = 0
    if datetime.date.today().weekday() >= 5:
      self.week_offset = 1

    user = anvil.users.get_user()
    self.nav.setup_repeating_convo_panel(user)
    self.banner_utils.setup_utils(user)
    if window.innerWidth < 760:
      self.move_banner_utils()
    # this also calls setup timetable, this is to account for language changes dynamically
    self.load_translations()

  def move_banner_utils(self):
    self.banner_utils.remove_from_parent()
    self.nav.insert_nav_item(self.banner_utils)
    self.banner_utils.update_button_role('filled-button')

  def load_translations(self):
    self.title.text = Translations.get_translation("Weekly timetable")
    self.prev_week_button.text = Translations.get_translation("Previous week")
    self.next_week_button.text = Translations.get_translation("Next week")
    self.setup_timetable()
    self.load_current_week_text()
    self.nav.load_translations()

  def setup_timetable(self):
    self.load_current_week_text()
    day_1 = self.get_desired_monday()
    day_2 = day_1 + datetime.timedelta(days=1)
    day_3 = day_2 + datetime.timedelta(days=1)
    day_4 = day_3 + datetime.timedelta(days=1)
    day_5 = day_4 + datetime.timedelta(days=1)
    self.setup_timetable_day(self.day_1_panel, self.day_1_label, day_1, self.get_timetable_data_for_date(day_1))
    self.setup_timetable_day(self.day_2_panel, self.day_2_label, day_2, self.get_timetable_data_for_date(day_2))
    self.setup_timetable_day(self.day_3_panel, self.day_3_label, day_3, self.get_timetable_data_for_date(day_3))
    self.setup_timetable_day(self.day_4_panel, self.day_4_label, day_4, self.get_timetable_data_for_date(day_4))
    self.setup_timetable_day(self.day_5_panel, self.day_5_label, day_5, self.get_timetable_data_for_date(day_5))

  def setup_timetable_day(self, linear_panel, day_label, day, data):
    day_str = Translations.get_translation(day.strftime("%A"))
    date_str = day.strftime("%d/%m/%Y")
    day_label.text = f"{day_str}\n{date_str}"
    linear_panel.clear()
    for item in data:
      new_session = TimetableSession(item=item)
      linear_panel.add_component(new_session)
      
  def get_timetable_data_for_date(self, date):  
    date_str = date.strftime("%d/%m/%Y")
    if date_str in self.item:
      return self.item[date_str]
    return []
  
  def get_desired_monday(self):
    today = datetime.date.today()
    # Calculate the difference between today and the previous Monday
    days_to_subtract = today.weekday()
    # Subtract the difference to get the previous Monday
    monday_of_current_week = today - datetime.timedelta(days=days_to_subtract)
    monday_of_desired_week = monday_of_current_week + datetime.timedelta(days=7*(self.week_offset + self.user_controlled_offset))
    return monday_of_desired_week    

  def prev_week_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.user_controlled_offset == 0:
      return
      
    self.user_controlled_offset -= 1

    if self.user_controlled_offset == 0:
      self.prev_week_button.enabled = False
    
    self.setup_timetable()

  def next_week_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.prev_week_button.enabled = True
    self.user_controlled_offset += 1
    self.setup_timetable()

  def load_current_week_text(self):
    if self.user_controlled_offset == 0:
      self.current_week_label.text = Translations.get_translation("This week")
    elif self.user_controlled_offset == 1: 
      self.current_week_label.text = Translations.get_translation("Next week")
    else:
      self.current_week_label.text = f'{self.user_controlled_offset} {Translations.get_translation("weeks away")}'