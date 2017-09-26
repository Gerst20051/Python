import json
import re
import sublime
import sublime_plugin
import urllib

class PassportCheckSettingCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.reset()
    self.view.window().show_quick_panel(list(Constants.ENVIRONMENTS.keys()), self.on_done_select_environment, sublime.MONOSPACE_FONT)

  def reset(self):
    self.view.erase_status('passport')
    self.HOST = ''
    self.COUNTRY_ISO_CODE = ''
    self.OPERATOR_ID = ''

  def on_done_select_environment(self, index):
    if index == -1:
      return
    self.HOST = Constants.ENVIRONMENTS[list(Constants.ENVIRONMENTS.keys())[index]]
    self.view.window().show_quick_panel(Constants.COUNTRY_ISO_CODE_LIST, self.on_done_select_country_iso_code, sublime.MONOSPACE_FONT)

  def on_done_select_country_iso_code(self, index):
    if index == -1:
      return
    self.COUNTRY_ISO_CODE = Constants.COUNTRY_ISO_CODE_LIST[index]
    self.view.window().show_quick_panel(Utils.sort_human(list(Constants.OPERATORS.keys())), self.on_done_select_operator, sublime.MONOSPACE_FONT)

  def on_done_select_operator(self, index):
    if index == -1:
      return
    self.OPERATOR_ID = Constants.OPERATORS[Utils.sort_human(list(Constants.OPERATORS.keys()))[index]]
    URL = 'https://%s/apps/v7/mobile/api/index.php/getoperatorsettings?country_iso_code=%s&operatorid=%s' % (self.HOST, self.COUNTRY_ISO_CODE, self.OPERATOR_ID)
    self.setting_data = json.loads(urllib.request.urlopen(URL).read().decode('utf-8'))['data']
    self.setting_keys = sorted([ key for key in self.setting_data.keys() if key ], key = lambda s: s.lower())
    self.view.window().show_quick_panel(self.setting_keys, self.on_done_select_setting, sublime.MONOSPACE_FONT)

  def on_done_select_setting(self, index):
    if index == -1:
      return
    self.view.set_status('passport', '[SETTING] %s => %s' % (self.setting_keys[index], self.setting_data[self.setting_keys[index]]))

class PassportCheckStringCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.reset()
    self.view.window().show_quick_panel(list(Constants.ENVIRONMENTS.keys()), self.on_done_select_environment, sublime.MONOSPACE_FONT)

  def reset(self):
    self.view.erase_status('passport')
    self.HOST = ''
    self.LOCALE = ''
    self.OPERATOR_ID = ''
    self.SYSTEM = 'Mobile' # ignore the other systems

  def on_done_select_environment(self, index):
    if index == -1:
      return
    self.HOST = Constants.ENVIRONMENTS[list(Constants.ENVIRONMENTS.keys())[index]]
    self.view.window().show_quick_panel(Constants.LOCALE_LIST, self.on_done_select_locale, sublime.MONOSPACE_FONT)

  def on_done_select_locale(self, index):
    if index == -1:
      return
    self.COUNTRY_ISO_CODE = Constants.LOCALE_LIST[index]
    self.view.window().show_quick_panel(Utils.sort_human(list(Constants.OPERATORS.keys())), self.on_done_select_operator, sublime.MONOSPACE_FONT)

  def on_done_select_operator(self, index):
    if index == -1:
      return
    self.OPERATOR_ID = Constants.OPERATORS[Utils.sort_human(list(Constants.OPERATORS.keys()))[index]]
    VERSION = '0' # ignore the string version
    URL = 'https://%s/apps/v7/mobile/api/index.php/getstrings?locale=%s&operatorId=%s&system=%s&version=%s' % (self.HOST, self.LOCALE, self.OPERATOR_ID, self.SYSTEM, VERSION)
    self.string_data = json.loads(urllib.request.urlopen(URL).read().decode('utf-8'))['data']
    self.string_keys = sorted([ key for key in self.string_data.keys() if key ], key = lambda s: s.lower())
    self.view.window().show_quick_panel(self.string_keys, self.on_done_select_string, sublime.MONOSPACE_FONT)

  def on_done_select_string(self, index):
    if index == -1:
      return
    self.view.set_status('passport', '[STRING] %s => %s' % (self.string_keys[index], self.string_data[self.string_keys[index]]))

class Constants():
  COUNTRY_ISO_CODE_LIST = [ 'US', 'AR', 'AU', 'CA', 'CN', 'ES', 'FR', 'GB', 'GV', 'IN', 'IT', 'MX', 'PT', 'TW', 'UY', 'XX' ]
  LOCALE_LIST = [ 'en_US', 'en_AU', 'en_CA', 'en_GB', 'en_IN', 'es_ES', 'es_US', 'eu_ES', 'fr_CA', 'fr_FR', 'it_IT', 'kn_IN' ]

  ENVIRONMENTS = {
    'US': 'ppprk.com',
    'CA': 'passportca.com',
    'EU': 'passporteu.com'
  }

  OPERATORS = {
    '0_passport': '0',
    '12_parkright': '12',
    '37_omaha': '37',
    '64_chicago': '64',
    '77_go502': '77',
    '117_toronto': '117',
    '166_worldsensing': '166',
    '172_newhaven': '172',
    '186_mackay': '186',
    '187_laz': '187',
    '188_sf': '188',
    '210_comet': '210',
    '212_boston': '212',
    '225_parkvictoria': '225',
    '227_mobilemeter': '227',
    '237_gotucsonparking': '237',
    '280_parkslc': '280',
    '294_easypark': '294',
    '306_parkmontreal': '306',
    '313_cincyezpark': '313',
    '315_parkwhiteplains': '315',
    '328_gotucsontransit': '328',
    '344_detroit': '344',
    '378_spoton': '378',
    '397_sacramento': '397',
    '400_jacksonville': '400',
    '436_parkrtc': '436',
    '440_parkbyapp': '440',
    '467_gcrta': '467',
    '493_cincyezride': '493',
    '511_miami': '511',
    '512_parksavannah': '512',
    '523_parkalbany': '523',
    '538_parkcc': '538',
    '550_parkx': '550',
    '555_parkelpaso': '555',
    '566_parkingkitty': '566',
    '576_lametro': '576',
    '577_charlotte': '577',
    '586_epark': '586',
    '601_buffaloroam': '601',
    '605_asburypark': '605',
    '606_detroit': '606',
    '612_utah': '612',
    '622_woonerf': '622',
    '624_albuquerque': '624'
  }

class Utils():
  def sort_human(l):
    convert = lambda text: float(text) if text.isdigit() else text
    alphanum = lambda key: [ convert(c) for c in re.split('([-+]?[0-9]*\.?[0-9]*)', key) ]
    l.sort(key = alphanum)
    return l
