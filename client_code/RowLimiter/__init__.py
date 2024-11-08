from ._anvil_designer import RowLimiterTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import Translations

class RowLimiter(RowLimiterTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.current_offset = 0
    self.show_more_button.visible = self.show_more_buttons_visible
    self.show_less_button.visible = self.show_more_buttons_visible
    self.rows = []
    self.lang = None

  def get_lang(self):
    if self.lang is None:
      return anvil.server.call('get_user_language', anvil.users.get_user())
    return self.lang

  def load_translations(self, lang=None):
    self.lang = lang
    self.show_more_button.text = Translations.get_translation("Show more", lang=lang)
    self.show_less_button.text = Translations.get_translation("Show less", lang=lang)
    for x in range(0, len(self.rows)):
      print(self.rows[x])
      try:
        self.rows[x].load_translations(lang)
      except Exception as e:
        print(e)
      
  def set_items(self, items, form):
    self.new_object_form = form
    self.item = items
    self.load_rows()

  def load_rows(self):
    self.row_holder.clear()
    try:
      self.show_more_button.visible = self.max_rows + self.current_offset < len(self.item) and self.show_more_buttons_visible is True
      self.show_less_button.visible = self.max_rows + self.current_offset > self.max_rows and self.show_more_buttons_visible is True
      for x in range(0, self.max_rows + self.current_offset):
        if len(self.item) > x:
          row = self.item[x]
          row = self.new_object_form(item=row, lang=self.get_lang())
          self.rows.append(row)
          self.row_holder.add_component(row)
    except TypeError as e:
      print(f"Error: {e} \n\n This error seems to happen when a user has no previous conversations.") # Scott 23/08/2024
      self.show_more_button.visible = False
      self.show_less_button.visible = False

  def show_more_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.current_offset += self.show_more_and_less_offset
    if self.current_offset + self.max_rows > len(self.item):
      self.current_offset = len(self.item) - self.max_rows
    self.load_rows()
    pass

  def show_less_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.current_offset -= self.show_more_and_less_offset
    if self.current_offset < 0:
      self.current_offset = 0
    self.load_rows()
    pass
