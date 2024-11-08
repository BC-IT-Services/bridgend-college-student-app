import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

def get_translation(default, lang=None):
  database_safe_default = default.replace("\n", "~")
  if lang is None:
    lang = anvil.server.call('get_user_language', anvil.users.get_user())
    
  if lang == "english":
    return default.replace("~", "\n")
  try:
    english_reference = app_tables.translations.get(english=database_safe_default)
  except Exception:
    print("DUPLICATE: " + database_safe_default)
    return default.replace("~", "\n")
  if english_reference is None:
    print("NO ENGLISH ENTRY ERROR: " + default)
    return default.replace("~", "\n")
    
  translation = english_reference[lang].replace("~", "\n")
  if translation == "" or translation is None:
    print("NO " + lang.upper() + " ENTRY ERROR: " + default)
    return default.replace("~", "\n")
    
  return translation

def get_reverse_translation(default):
  database_safe_str = default.replace("\n", "~")
    
  lang = anvil.server.call('get_user_language', anvil.users.get_user())
  if lang == "cymraeg":
    return default
  welsh_reference = app_tables.translations.get(cymraeg=database_safe_str)
  
  if welsh_reference is None:
    print("NO WELSH ENTRY ERROR: " + default)
    return default
    
  translation = welsh_reference[lang].replace("~", "\n")
  if translation == "" or translation is None:
    print("NO " + lang.upper() + " ENTRY ERROR: " + default)
    return default
    
  return translation
