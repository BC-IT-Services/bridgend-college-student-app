from ._anvil_designer import UserHomeScreenTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta, timezone
from .TimetableSession import TimetableSession

from .TargetObject import TargetObject
from .CitizenshipObject import CitizenshipObject
from ..ReportAnAbsence import ReportAnAbsence
from ..AddATarget import AddATarget

from .. import Translations
from .. import Tracking
from .. import UserUtils

from anvil.js import window

import time

from random import choice

class UserHomeScreen(UserHomeScreenTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.initialise = properties.get("initialise")

    # Check what device the user is on
    self.sync_state = anvil.server.call('get_sync_state')

    self.user = anvil.users.get_user()
    self.lang = anvil.server.call('get_user_language', self.user)
    self.persistent_data = anvil.server.call_s('get_persistent_data', self.user)
    
    self.news_objects = []
    self.timetable_date_picker.date = datetime.today().date()
    self.load_screen()
    if window.innerWidth < 760:
      self.move_banner_utils()
      Tracking.send_tracking_request("LOGIN: Mobile")
    else:
      Tracking.send_tracking_request("LOGIN: Desktop")
  
  def move_banner_utils(self):
    self.banner_utils.remove_from_parent()
    self.nav.insert_nav_item(self.banner_utils)
    self.banner_utils.update_button_role('filled-button')
    
  def load_translations(self):
    lang = anvil.server.call('get_user_language', anvil.users.get_user())
    self.lang = lang
    self.targets_title.text = Translations.get_translation("Targets", lang=lang)
    self.attendance_title.text = Translations.get_translation("Attendance", lang=lang)
    self.attendance_perc_title.text = Translations.get_translation("Attendance", lang=lang)
    self.skills_attendance_perc_title.text = Translations.get_translation("Skills Attendance", lang=lang)
    self.inclass_attendance_perc_title.text = Translations.get_translation("In-Class Attendance", lang=lang)
    self.punc_perc_title.text = Translations.get_translation("Punctuality", lang=lang)
    self.citizenship_title.text = Translations.get_translation("Citizenship", lang=lang)
    self.timetable_title.text = Translations.get_translation("Timetable", lang=lang)
    self.target_row_limiter.load_translations(lang=lang)
    self.citizenship_row_limiter.load_translations(lang=lang)
    self.nav.load_translations(lang=lang)
    self.targets_title.text = Translations.get_translation("Targets", lang=lang)
    self.attendance_title.text = Translations.get_translation("Attendance", lang=lang)
    self.attendance_perc_title.text = Translations.get_translation("Attendance", lang=lang)
    self.skills_attendance_perc_title.text = Translations.get_translation("Skills Attendance", lang=lang)
    self.inclass_attendance_perc_title.text = Translations.get_translation("In-Class Attendance", lang=lang)
    self.punc_perc_title.text = Translations.get_translation("Punctuality", lang=lang)
    self.citizenship_title.text = Translations.get_translation("Citizenship", lang=lang)
    self.timetable_title.text = Translations.get_translation("Timetable", lang=lang)
    self.target_row_limiter.load_translations(lang=lang)
    self.citizenship_row_limiter.load_translations(lang=lang)
    self.nav.load_translations(lang=lang)
    
  def load_screen(self):
    user = anvil.users.get_user()
    email = user['email']
    self.load_translations()
    
    self.banner_utils.setup_utils(user)

    try:
      int(email.split('@')[0])
    except ValueError:
      self.no_sessions_label.text = Translations.get_translation('Timetable disabled in staff preview.')
    self.student_id = anvil.users.get_user()['studentid']
    self.nav.setup_repeating_convo_panel(anvil.users.get_user())
    self.timetable_data = None
    
    self.setup_timetable_panel()
    self.setup_target_panel()
    self.setup_attendance_panel()
    self.setup_citizenship_panel()

  def setup_attendance_panel(self):
    try:
      attendance_data = anvil.server.call('get_attendance', self.student_id)
    except Exception as e:
      self.attendance_error.visible = True
      self.no_error_attendance_panel.visible = False
      self.add_target_button.visible = False
      print(f"-----------------------\nERROR INFO\nFUNCTION: setup_attendance_panel\nFUNCTION LOCATION: UserHomeScreen (Form)\nERROR: {e}\n-----------------------")
      return    

    self.attendance_error.visible = False
    self.no_error_attendance_panel.visible = True
    self.add_target_button.visible = True

    if attendance_data.get('punctuality_percentage', None) is not None:
      punctuality_percentage = attendance_data.get('punctuality_percentage')
      overall_attendance_percentage = attendance_data.get('overall_attendance_percentage')
      in_class_attendance_percentage = attendance_data.get('inclass_attendance_percentage')
      skills_attendance_percentage = attendance_data.get('skills_attendance_percentage')
      self.attendance_perc_label.text = overall_attendance_percentage
      self.inclass_attendance_perc_label.text = in_class_attendance_percentage
      self.skills_attendance_perc_label.text = skills_attendance_percentage or '100.0%'
      self.punc_perc_label.text = punctuality_percentage
      self.inclass_attendance_perc_panel.background = self.get_attendance_panel_color(in_class_attendance_percentage)
      self.skills_attendance_perc_panel.background = self.get_attendance_panel_color(skills_attendance_percentage or '100.0%')
      self.attendance_perc_panel.background = self.get_attendance_panel_color(overall_attendance_percentage)
      self.punc_perc_panel.background = self.get_attendance_panel_color(punctuality_percentage)
    else:
      punctuality_percentage = '100%'
      overall_attendance_percentage = '100%'
      in_class_attendance_percentage = '100%'
      skills_attendance_percentage = '100%'
      self.attendance_perc_label.text = overall_attendance_percentage
      self.inclass_attendance_perc_label.text = in_class_attendance_percentage
      self.skills_attendance_perc_label.text = skills_attendance_percentage
      self.punc_perc_label.text = punctuality_percentage
      self.inclass_attendance_perc_panel.background = self.get_attendance_panel_color(in_class_attendance_percentage)
      self.skills_attendance_perc_panel.background = self.get_attendance_panel_color(skills_attendance_percentage)
      self.attendance_perc_panel.background = self.get_attendance_panel_color(overall_attendance_percentage)
      self.punc_perc_panel.background = self.get_attendance_panel_color(punctuality_percentage)
      pass

    pass

  def get_attendance_panel_color(self, percentage_text):
    try:
      perc = float(percentage_text.rstrip("%"))
    except:
      perc = 0  
    if perc < 80:
      return "var(--red)"
    elif perc < 90:
      return "var(--yellow)"
    else:
      return "var(--green)"

  def remove_duplicates_and_null_data(self, data):
    return_list = [i for n, i in enumerate(data) if i not in data[:n]]
    return return_list
    
  def setup_citizenship_panel(self):
    citizenship_data = []
    badge_data = {}
    try:
      citizenship_data_call = anvil.server.call('get_citizenship_data', self.student_id)
      citizenship_data = citizenship_data_call[0] 
      badge_data = citizenship_data_call[1] 
    except Exception as e:
      self.citizenship_error.visible = True
      self.no_error_citizenship_panel.visible = False
      print(f"-----------------------\nERROR INFO\nFUNCTION: setup_citizenship_panel\nFUNCTION LOCATION: UserHomeScreen (Form)\nERROR: {e}\n-----------------------")
      return

    self.citizenship_error.visible = False
    self.no_error_citizenship_panel.visible = True
    
    filtered_array = [d for d in citizenship_data if d["text"] is not None]
    clean_data = self.remove_duplicates_and_null_data(filtered_array)
    clean_data.reverse()
    if len(clean_data) == 0:
      self.no_citizenship.visible = True
      self.citizenship_row_limiter.visible = False
    else:
      self.no_citizenship.visible = False
      self.citizenship_row_limiter.visible = True
      self.citizenship_row_limiter.set_items(clean_data, CitizenshipObject)
  
  def setup_target_panel(self):
    try:
      ilp_data = anvil.server.call('get_ilp_targets', self.student_id)
      targets = ilp_data[0] if len(ilp_data) > 0 else []
    except Exception as e:
      self.targets_error.visible = True
      self.no_error_targets_panel.visible = False
      print(f"-----------------------\nERROR INFO\nFUNCTION: setup_target_panel\nFUNCTION LOCATION: UserHomeScreen (Form)\nERROR: {e}\n-----------------------")
      return

    self.targets_error.visible = False
    self.no_error_targets_panel.visible = True
  
    filtered_array = [d for d in targets if d["target"] is not None]
    clean_data = self.remove_duplicates_and_null_data(filtered_array)
    user_set_targets = anvil.users.get_user()['targets']
    length = 0
    if user_set_targets is not None:
      length = len(user_set_targets)
    for x in range(0, length):
      user_set_targets[x]['start_date_time'] = datetime.strptime(user_set_targets[x]['start_date_time'], "%d/%m/%Y")
      user_set_targets[x]['end_date_time'] = datetime.strptime(user_set_targets[x]['end_date_time'], "%d/%m/%Y")
      user_set_targets[x]['target_index'] = x
      clean_data.append(user_set_targets[x])
    clean_data.sort(key=lambda item: item['end_date_time'].replace(tzinfo=None))
    clean_data.reverse()
    if len(clean_data) == 0:
      self.target_row_limiter.visible = False
    else:
      self.target_row_limiter.visible = True
      self.target_row_limiter.set_items(clean_data, TargetObject)

  def setup_timetable_panel(self):
    error = False
    if self.timetable_data is None:
      try:
        self.timetable_data = anvil.server.call('get_timetable_data_lite', self.student_id)
      except Exception as e:
        self.timetable_error.visible = True
        self.no_error_timetable_panel.visible = False
        print(f"-----------------------\nERROR INFO\nFUNCTION: setup_timetable_panel\nFUNCTION LOCATION: UserHomeScreen (Form)\nERROR: {e}\n-----------------------")
        error = True
        return

    self.timetable_error.visible = False
    self.no_error_timetable_panel.visible = True
    
    self.load_timetable_data(error=error)

  def load_timetable_data(self, error):
    if error is True:
      # Do something here to show the error
      return
      
    self.selected_day_timetable.clear()
    date_string = self.timetable_date_picker.date.strftime("%d/%m/%Y")
    if date_string in self.timetable_data:
      selected_days_sessions = self.timetable_data[date_string]
      formatted_sessions = self.remove_duplicates_and_null_data(selected_days_sessions)
      for session in formatted_sessions:
        session_card = TimetableSession(item=session)
        self.selected_day_timetable.add_component(session_card)
      self.no_sessions_label.visible = False
    else:
      self.no_sessions_label.visible = True
      print("No Timetable data to show")

  def timetable_date_picker_change(self, **event_args):
    """This method is called when the selected date changes"""
    self.load_timetable_data(False)
    pass

  def add_target_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    new_target = {
      'target_stats': 'IN PROGRESS',
      'start_date_time': datetime.today().date().strftime("%d/%m/%Y"),
      'course_description': None, # maybe change this to be their course desc? But I dont think we acccess that yet
      'target': "",
      'end_date_time': datetime.today().date() + timedelta(days=31),
      'set_by': "You",
      'steps': []
    }

    a = alert(
      AddATarget(item=new_target),
      large=True,
      dismissible=False,
      buttons=[(Translations.get_translation("Cancel"), False), (Translations.get_translation("Add Target"), True)]
    )

    if a is True:
      new_target['end_date_time'] = new_target['end_date_time'].strftime("%d/%m/%Y")
      anvil.server.call('add_target', anvil.users.get_user(), new_target)
      self.setup_target_panel()
    
  def view_weekly_timetable_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    Tracking.send_tracking_request("HOMESCREEN BUTTON CLICK: Weekly timetable")
    open_form('WeeklyTimetable', item=self.timetable_data)
    pass

  def absence_request(self, session):
    selected_start_day = self.timetable_date_picker.date
    absence = Absence.get_default_absence()
    absence['start_date'] = selected_start_day
    absence['end_date'] = selected_start_day
    absence['selected_sessions'] = [session]
    self.start_absence_report(absence)

  def report_absence_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.start_absence_report(Absence.get_default_absence())

  def start_absence_report(self, absence):
    a = alert(
      ReportAnAbsence(item=absence, timetable=self.timetable_data),
      large=True,
      dismissible=True,
      buttons=[(Translations.get_translation("Cancel"), False),(Translations.get_translation("Send absence report"), True)]
    )

    if a is True:
      Absence.confirm_absence(absence['start_date'], absence['end_date'], absence['selected_sessions'], absence['reason'], anvil.users.get_user())
    pass