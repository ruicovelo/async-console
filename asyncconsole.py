import curses


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
    
    def move_cursor_left(self):
        min_x = 0
        min_y = 0
        if self.y == min_y:
            min_x = len(self.prompt_string)
        if self.x > min_x:
            self.x = self.x-1
        elif self.y > min_y:
            self.y = self.y = self.y-1
            (y,self.x) = self.prompt_window.getmaxyx()
        else:
            return False
        self.prompt_window.move(self.y,self.x)
        self.prompt_window.refresh()
        return True

    def move_cursor_right(self,max_x=0):
        if self.x < max_x:
            self.x = self.x+1
            self.prompt_window.move(self.y,self.x)
            self.prompt_window.refresh()
            return True
        return False
            
    def backspace(self):
        if self.move_cursor_left():
            self.prompt_window.delch()
            self.input_string = self.input_string[:-1]
        
    def readline(self):
        self.input_string = ''
        
        # interpret keypad keys like arrows
        self.prompt_window.keypad(1)
        
        while True:
            c = self.prompt_window.getch()
            (self.y,self.x) = self.prompt_window.getyx()
            
            try:
                c = chr(c)
                o = ord(c)
                
                #TODO: replace '\n' with key enter/line feed?!
                if ord(c) == ord('\n'):
                    self.prompt_window.clear()
                    self.rebuild_prompt()
                    return True
                
                if o == 127 or o == curses.KEY_BACKSPACE or o == curses.KEY_DC: # backspace
                    self.backspace()
                    continue
                    
                self.prompt_window.addstr(str(c))
                self.input_string = self.input_string + c
                self.prompt_window.refresh()
            except ValueError:   
                if c == curses.KEY_RESIZE: # resize screen
                    self.resize()
                else:
                    self.output_window.addstr(str(c)+"\n")


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