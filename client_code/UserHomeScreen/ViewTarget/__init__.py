from ._anvil_designer import ViewTargetTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ... import Translations

import copy

class ViewTarget(ViewTargetTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.lang = get_open_form().lang
    self.load_details()
    self.load_translations()
    self.load_steps()

  def load_translations(self):
    if 'target_type' in self.item:
      target_type = self.item['target_type']
    else:
      target_type = Translations.get_translation("Missing", self.lang)
    self.title.text = Translations.get_translation("Target Information", self.lang)
    self.set_by_label.content = f"**{Translations.get_translation('Set by', self.lang)}:** {self.item['set_by']}"
    self.set_date_label.content = f"**{Translations.get_translation('Date set', self.lang)}:** {self.item['start_date_time'].strftime('%A %d/%m/%Y')}"
    self.end_date_label.content = f"**{Translations.get_translation('Target completion date', self.lang)}:** {self.item['end_date_time'].strftime('%A %d/%m/%Y')}"
    self.objective_title_label.text = f'{Translations.get_translation("Objective", self.lang)}:'
    self.steps_title.text = Translations.get_translation("Steps", self.lang)
    self.not_started_button.text = Translations.get_translation("Not started", self.lang)
    self.in_progress_button.text = Translations.get_translation("In progress", self.lang)
    self.complete_button.text = Translations.get_translation("Complete", self.lang)
    self.target_type_label.content = f"**{Translations.get_translation('Target Type', self.lang)}:** {target_type}"
    self.details_title_label.text = Translations.get_translation("Details", self.lang)

  def load_details(self):
    if self.item['set_by'] == "You":
      key = 'additional_info'
    else:
      key = 'target_description'

    if key in self.item:
      visible = self.item[key] != ""
      self.details_label.text = self.item[key]
    else:
      visible = False
      
    self.details_title_label.visible = visible
    self.details_label.visible = visible
      
      
  def load_steps(self):
    items = self.item['steps']
    if len(items) > 0:
      formatted_items = []
      i = 0
      for item in items:
        formatted_items.append({
          'index': i,
          'step': item,
          'parent': self
        })
        i+=1
      self.steps_panel.visible = True
      self.repeating_steps.items = formatted_items
    else:
      self.steps_panel.visible = False

  def not_started_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.update_target_status("NOT STARTED")

  def in_progress_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.update_target_status("IN PROGRESS")

  def complete_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.check_for_incomplete_steps():
      a = alert(
        "There are incomplete steps, setting the target to complete will automatically set the status of the steps to complete.\n\nAre you sure you want to mark this target as complete?",
        large=True,
        dismissible=True,
        buttons=[("Cancel", False), ("Mark this target as complete.", True)]
      )
      if a is False:
        return
      else:
        for x in range(0, len(self.item['steps'])):
          self.update_step_status(x, "Complete")
        self.load_steps()
    self.update_target_status("COMPLETED")
  
  def check_for_incomplete_steps(self):
    if len(self.item['steps']) > 0:
      for step in self.item['steps']:
        if step['status'] != "Complete":
          return True
    return False

  def update_target_status(self, status):
    self.item['target_stats'] = status
    self.refresh_data_bindings()
    
  def update_step_status(self, index, status):
    self.item['steps'][index]['status'] = status
    anvil.server.call('update_target', get_open_form().user, self.item['target_index'], self.item)
