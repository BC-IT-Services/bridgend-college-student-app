import anvil.server
import anvil.users

def simple_role_check(role):
  user = anvil.users.get_user()
  roles = user['roles']
  if roles is None:
    return False
  if role in roles or 'admin' in roles:
    return True
