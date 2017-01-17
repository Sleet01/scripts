#!/usr/bin/python

import curses
import os
import sys
import re

FILES = [str(f) for f in os.listdir('.') if os.path.isfile(f) and f[-4:] == ".txt" ]

def __sort_nicely( l ):
  """Sort the given list naturally"""

  convert = lambda text: int(text) if text.isdigit() else text
  alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
  l.sort( key=alphanum_key )

__sort_nicely( FILES )

FINDEX = 0

def jumpFINDEX(jump):
  """Change FINDEX by relative amount; wrap to opposite end of index if negative or larger than file list size"""

  global FINDEX
  FINDEX = ( FINDEX + jump ) % ( len(FILES) - 1 ) 
  
def moveFINDEX(index):
  """Change FINDEX to supplied index IFF supplied index is within (len(FILES) - 1)"""

  global FINDEX 

  # Jump to the index if it is valid; otherwise for negatives go to 0; for over-large index values, go to max index
  if( (index >= 0) and (index < len(FILES) ) ):
    FINDEX = index
  elif (index < 0 ):
    FINDEX = 0
  else:
    FINDEX = len(FILES) - 1


def cursesSetup():
  # Curses setup from http://www.dev-explorer.com/articles/python-with-curses
  
  # Find max size of current terminal window
   
  screen = curses.initscr()
  curses.noecho()
  curses.curs_set(0)
  curses.cbreak()
  screen.keypad(1)
 
  return screen

def cursesTeardown(screen):
  curses.nocbreak()
  screen.keypad(0)
  curses.echo()
  screen.clear()
  curses.curs_set(1)
  curses.endwin()


def barUpdate(screen, index=None):
  """Update the bar at the bottom of the screen"""

  if index is None:
    pass

  else:
    percent = ((100.00 * index) / len(FILES))
    filename = FILES[index]
    date = filename[4:12]
    time = filename[13:19]
    status = "Index: %d - %f %%;  Filename: %s;  Date: %s/%s/%s;  Time: %s:%s:%s" % \
      ( index, percent, filename, date[0:4], date[4:6], date[6:], time[0:2], time[2:4], time[4:])


    maxy, maxx = screen.getmaxyx()
    screen.move(maxy-1, 0)
    screen.clrtoeol()
    screen.addstr(maxy-1,0, status)


def loadFile(filename):
  """Open a file, name usually determined from the list of FILES.
   Return a string object."""

  fh = open(filename, 'r')
  strVar = fh.read()
  fh.close()

  return strVar
 
 
def printFile(strVar, screen):
  """ Given a multiline string (basically, all the contents of a top screen dump),
    print each line in order from screen position (0,0)."""
  
  screen.clear()

  for y, line in enumerate(strVar.splitlines(), 0):
    screen.addstr(y, 0, line)
  
  barUpdate(screen, FINDEX)
  screen.refresh()


def moveToFile(index, screen):
  """ Automate jumping to a file name, reading it, and displaying it."""
  
  moveFINDEX(index)
  printFile(loadFile(FILES[FINDEX]), screen)


def jumpFile(jump, screen):
  """ Move forward from current index by 'jump' increment; usually +/- 1 or +/- 5 """
  
  jumpFINDEX(jump)
  printFile(loadFile(FILES[FINDEX]), screen)


if __name__ == "__main__":

  scrn = cursesSetup()

  try:
    moveToFile(0, scrn)
  except:
    cursesTeardown(scrn)
    sys.exit(1) 

  while True:
    event = scrn.getch()
    
    if event == ord("q"):
      break
    elif event == curses.KEY_RIGHT:
      jumpFile(1, scrn)
    elif event == curses.KEY_LEFT:
      jumpFile(-1, scrn)
    elif event == curses.KEY_UP:
      jumpFile(5, scrn)
    elif event == curses.KEY_DOWN:
      jumpFile(-5, scrn)
    elif event == curses.KEY_PPAGE:
      jumpFile(100, scrn)
    elif event == curses.KEY_NPAGE:
      jumpFile(-100, scrn)
    elif event == ord("0"):
      moveToFile(0,scrn)

  cursesTeardown(scrn)
