import curses,os,sys,traceback


class AsyncConsole(object):

    screen = None
    output_window = None
    prompt_window = None
    prompt_string = None

    def __init__(self,prompt_string='> '):
        self.prompt_string=prompt_string
        self._initialize()
        self.rebuild_prompt()
        

    def _initialize(self):
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        (y,x) = self.screen.getmaxyx()
        # leave last lines from prompt
        self.output_window = self.screen.subwin(y-2,x,0,0)
        self.prompt_window = self.screen.subwin(1,x,y-2,0)
        self.prompt_window.keypad(1)
        # let output_window scroll by itself when number of lines are more than window size
        self.output_window.scrollok(True)
        self.prompt_window.scrollok(True)
        #TODO: set cursor position on prompt_window?



    def rebuild_prompt(self,default_text=None):
        self.prompt_window.clear()
        self.prompt_window.addstr(self.prompt_string)
        if default_text:
            self.prompt_window.addstr(default_text)
        self.prompt_window.refresh()


    def resize(self):
        #FIX: leaving garbage behind
        (y,x)=self.screen.getmaxyx()
        #curses.resizeterm(y,x)
        self.output_window.resize(y-2,x)
        # move the prompt window to the bottom of the output_window
        self.prompt_window.mvwin(y-2,0)
        self.prompt_window.resize(1,x)
        self.output_window.refresh()
        self.prompt_window.refresh()

    def start(self):
        input_string = ''
        while True:
            try:
                c = self.screen.getch()
                c = chr(c)
                #TODO: replace 10 with key enter/line feed?!
                if ord(c) == 10:
                    self.prompt_window.clear()
                    self.output_window.addstr(input_string+'\n')
                    self.output_window.refresh()
                    self.rebuild_prompt()
                    input_string = ''
                    continue
                #TODO: replace 27 with key escape
                if ord(c) == 27:
                    break
                self.prompt_window.addstr(str(c))
                input_string = input_string + c
                self.prompt_window.refresh()
            except ValueError:
                if c == curses.KEY_RESIZE: # resize screen
                    self.resize()
                else:
                    self.output_window.addstr(str(c)+"\n")

    def restore_screen(self):
        curses.nocbreak()
        curses.echo()
        curses.endwin()

def restore_screen():
    curses.nocbreak()
    curses.echo()
    curses.endwin()

def main():
    try:
        console = AsyncConsole()
        console.start()
        restore_screen()
    except:
        restore_screen()    
        traceback.print_exc()


if __name__ == '__main__':
    main()
