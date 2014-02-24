'''
Created on Sep 25, 2013

Demo script for the AsyncConsole. A thread in the background runs in a cycle printing
the current time while the user can still type in the input prompt.

@author: pedro
'''
import curses
import threading
import time
from asyncconsole import AsyncConsole

class MyThread(threading.Thread):
    stop = False
    interval = 30.0
    console = None
    
    
    def __init__(self):
        super(MyThread, self).__init__()
    
    def run(self):
        while not self.stop:
            self.console.addline(time.strftime("%H:%M:%S", time.gmtime()))
            time.sleep(self.interval)



def main(stdscr):
    console = AsyncConsole(stdscr)
    t = MyThread()
    t.console=console
    t.interval=10.0
    t.start()
    try:
        while console.readline():
            if console.input_string == 'quit':
                break
            console.addline(console.input_string)
    finally:
        t.stop = True    
    
    

if __name__ == '__main__':
    curses.wrapper(main)
