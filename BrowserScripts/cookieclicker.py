import time
from splinter import Browser
from threading import Thread

#
# SETUP INSTRUCTIONS
#
# sudo pip install splinter
# sudo pip install selenium
# brew install chromedriver
#
# To have launchd start chromedriver at login:
#   ln -sfv /usr/local/opt/chromedriver/*.plist ~/Library/LaunchAgents
# Then to load chromedriver now:
#   launchctl load ~/Library/LaunchAgents/homebrew.mxcl.chromedriver.plist
#

browser = Browser('chrome')
cookie = None
click_delay = 0.2
close_notes_delay = 5.0
topbar_removed = False
game_style_top_adjusted = False
support_removed = False
last_achievements_time = time.time()

def init():
  open_site()
  modify_dom()
  show_stats_panel()
  start_loop()

def open_site():
  global cookie
  browser.cookies.all()
  browser.visit('http://orteil.dashnet.org/cookieclicker/')
  cookie = browser.find_by_id('bigCookie')

def modify_dom():
  global topbar_removed, game_style_top_adjusted, support_removed
  if topbar_removed is False and browser.is_element_present_by_id('topBar'):
    browser.execute_script('document.getElementById("topBar").remove();')
    topbar_removed = True
  if game_style_top_adjusted is False:
    browser.execute_script('document.getElementById("game").style.top = "0";')
    game_style_top_adjusted = True
  if support_removed is False and browser.is_element_present_by_id('support'):
    browser.execute_script('document.getElementById("support").remove();')
    support_removed = True

def show_stats_panel():
   browser.execute_script('document.getElementById("statsButton").click();')

def start_loop():
  global last_achievements_time
  while True:
    cookie.click()
    if check_time_passed(last_achievements_time, close_notes_delay) is True:
      last_achievements_time = time.time()
      close_notes()
    time.sleep(click_delay)

def close_notes():
  browser.execute_script('Game.CloseNotes();');

def check_time_passed(oldepoch, seconds_delay):
  return time.time() - oldepoch >= seconds_delay

if __name__ == '__main__':
  init()
