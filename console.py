import curses,os,sys,traceback


class AsyncConsole(object):

    screen = None
    output_window = None
    prompt_window = None
    prompt_string = None

    def __init__(self,screen=None,prompt_string='> '):
        self.screen = screen
            
        self.prompt_string=prompt_string
        self._initialize()
        self.rebuild_prompt()
        

    def _initialize(self):
        if not self.screen:
            # if wrapper has been used, we don't need this
            self.screen = curses.initscr()
            curses.noecho()
            curses.cbreak()
        
        # get the current size of screen    
        (y,x) = self.screen.getmaxyx()
        
        # leave last lines for prompt
        self.output_window = self.screen.subwin(y-2,x,0,0)
        self.prompt_window = self.screen.subwin(1,x,y-2,0)
        
        # let output_window scroll by itself when number of lines are more than window size
        self.output_window.scrollok(True)
        self.prompt_window.scrollok(True)
        



    def rebuild_prompt(self,default_text=None):
        self.prompt_window.clear()
        self.prompt_window.addstr(self.prompt_string)
        if default_text:
            self.prompt_window.addstr(default_text)
        self.prompt_window.refresh()


    def resize(self):
        #FIX: leaving garbage behind
        
        # get new size of screen
        (y,x)=self.screen.getmaxyx()

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
                o = self.prompt_window.getch()
                c = chr(o)
                
                #TODO: replace '\n' with key enter/line feed?!
                if ord(c) == ord('\n'):
                    if input_string == 'quit':
                        break
                    
                    self.prompt_window.clear()
                    self.output_window.addstr(input_string+'\n')
                    self.output_window.refresh()
                    self.rebuild_prompt()
                    input_string = ''
                    continue
                if o == 127 or o == curses.KEY_BACKSPACE or o == curses.KEY_DC: # backspace
                    (y,x) = self.prompt_window.getyx()
                    if x > len(self.prompt_string):
                        self.prompt_window.move(y,x-1)
                        input_string = input_string[:-1]
                        self.prompt_window.delch()
                        self.prompt_window.refresh()
                    continue

                self.prompt_window.addstr(str(c))
                input_string = input_string + c
                self.prompt_window.refresh()
            except ValueError:
                if c == curses.KEY_RESIZE: # resize screen
                    self.resize()
                else:
                    self.output_window.addstr(str(c)+"\n")

    def restore_screen(self):
        # to be used if not using the wrapper module
        curses.nocbreak()
        curses.echo()
        curses.endwin()



def main(stdscr):
    console = AsyncConsole(stdscr)
    console.start()


if __name__ == '__main__':
    curses.wrapper(main)
