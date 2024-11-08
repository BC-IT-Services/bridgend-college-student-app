from ._anvil_designer import AddATargetTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import Translations

class AddATarget(AddATargetTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.load_translations()

  def load_translations(self):
    self.title.text = Translations.get_translation("Create a target")
    self.target_title_label.text = f'{Translations.get_translation("Target title")}:'
    self.target_type_label.text = f'{Translations.get_translation("Target type")}:'
    self.due_date_label.text = f'{Translations.get_translation("Due date")}:'
    self.steps_label.text = Translations.get_translation("Steps")
    self.target_input.placeholder = Translations.get_translation("Enter a target title...")
    self.target_type_dropdown.items = [
      (Translations.get_translation("Skills Target"), "Skills Target"),
      (Translations.get_translation("Personal Target"), "Personal Target"),
      (Translations.get_translation("Course Target"), "Course Target"),
    ]

  def delete_step(self, index):
    items = self.item['steps']
    del items[index]
    self.item['steps'] = items
    self.load_steps()
    self.add_step_button.enabled = True

  def update_step(self, index, new_step_text):
    items = self.item['steps']
    items[index]['name'] = new_step_text
    self.item['steps'] = items

  def load_steps(self):
    items = self.item['steps']
    i = 0
    formatted_items = []
    for item in items:
      formatted_items.append({
        'index': i,
        'step': item,
      })
      i+=1
    self.repeating_steps.items = formatted_items
    print(self.item['steps'])

  def add_step_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if len(self.item['steps']) >= 5:
      return
    self.item['steps'].append({'step': "", 'status': "Not started"})
    self.load_steps()
    if len(self.item['steps']) >= 5:
      self.add_step_button.enabled = False
