#!/usr/bin/python

import os
import sys    
import termios
import fcntl

def getch():
  fd = sys.stdin.fileno()

  oldterm = termios.tcgetattr(fd)
  newattr = termios.tcgetattr(fd)
  newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
  termios.tcsetattr(fd, termios.TCSANOW, newattr)

  oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
  fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

  try:        
    while 1:            
      try:
        c = sys.stdin.read(3)
        break
      except IOError: pass
  finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
  return c

def readch():
  
  val=""

  while(1):
    k=getch()
    if k!='':break
  if k=='\x1b[A':
    val = "up" 
  elif k=='\x1b[B':
    val = "down"
  elif k=='\x1b[C':
    val = "right"
  elif k=='\x1b[D':
    val = "left"
  else:
    val = k 

  return val

if __name__ == "__main__":

  while(1):
    print readch()
