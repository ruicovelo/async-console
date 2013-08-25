# Async-Console

I'm really not sure about the name...


This is my first curses experiment. It's a console application
using  curses windows: one for displaying text and
another for receiving keyboard input.

The goal is to be able to display asynchronous output from
processes running in the background without interfering with
the input. I have tried a few line buffer hacks, the readline
module and threads but were far from perfect as stdin and stdout
are not thread safe. I hope curses will allow me to acomplish my
goal because I will have each thread accessing a different window.

I need this for MyBot project where I spawn multiple modules in
different processes and want to receive their text output while
I type in new commands.

If you know anything like this please tell me. I rather be
coding something else. It's nice to finally use curses in one of
my projects thou...
