import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from . import Translations

def get_readable_translated_date(date, lang):
  day_of_week =  Translations.get_translation(date.strftime("%A"), lang=lang)
  day = date.strftime("%d")
  day += Translations.get_translation(get_date_suffix(day), lang=lang)
  month = Translations.get_translation(date.strftime("%B"), lang=lang)
  return f"{day_of_week} {day} {month}"
  
def get_date_suffix(day):
  day = int(day)
  if day == 1:
    return "st"
  elif day == 2:
    return "nd"
  elif day == 3:
    return "rd"
  elif 11 <= day <= 13:
    return "th"
  elif day % 10 == 1:
    return "st"
  elif day % 10 == 2:
    return "nd"
  elif day % 10 == 3:
    return "rd"
  else:
    return "th"
