import curses
from curses import textpad


class AsyncConsole(object):

    screen = None
    output_window = None
    prompt_window = None
    prompt_string = None
    x = 0
    y = 0

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
        self.edit = textpad.Textbox(self.prompt_window,insert_mode=True)

        
        # let output_window scroll by itself when number of lines are more than window size
        self.output_window.scrollok(True)
        self.prompt_window.scrollok(True) #FIX: not working with textpad.Textbox
        



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
    
    def _validate_input(self,key):
        #TODO: handle up and down arrows
        # terminate editing when pression enter key
        if key == ord('\n'):
            return curses.ascii.BEL # this is equivalent to CONTROL+G - terminate editing and return content
        if key in (curses.ascii.STX,curses.KEY_LEFT, curses.ascii.BS,curses.KEY_BACKSPACE):
            minx = len(self.prompt_string)
            (y,x) = self.prompt_window.getyx()
            if x == minx:
                return None
        return key
        
    def readline(self,handle_interrupt=True):
        
        # interpret keypad keys like arrows
        self.prompt_window.keypad(1)
        try:
            self.input_string = self.edit.edit(self._validate_input)[len(self.prompt_string):]
        except KeyboardInterrupt:
            #TODO: I still don't know if I want to handle this here or not
            if handle_interrupt:
                return False
            else:
                raise KeyboardInterrupt
        self.rebuild_prompt()
        return True

    def addline(self,line):
        '''
        Add a string line to the output screen
        '''
        #TODO: make this thread safe?
        self.output_window.addstr(line+'\n')
        self.output_window.refresh()

    def restore_screen(self):
        # to be used if not using the wrapper module
        curses.nocbreak()
        curses.echo()
        curses.endwin()



def main(stdscr):
    # demo code
    console = AsyncConsole(stdscr)
    while console.readline():
        if console.input_string == 'quit':
            break
        console.addline(console.input_string)                  



if __name__ == '__main__':
    curses.wrapper(main)
