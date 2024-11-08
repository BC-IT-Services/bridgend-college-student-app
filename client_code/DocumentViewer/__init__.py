from ._anvil_designer import DocumentViewerTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from anvil.js.window import jQuery
from anvil.js import get_dom_node, window


class DocumentViewer(DocumentViewerTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.load_document()

  def load_document(self):
    target_iframe_height = window.innerHeight * 0.8
    iframe = jQuery(f"<iframe width='100%' height='{target_iframe_height}px'>").attr("src", self.item['url'])
    iframe.appendTo(get_dom_node(self))