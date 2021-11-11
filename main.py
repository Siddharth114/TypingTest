import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr('Welcome to my typing test! \nPress any key to continue.')
    stdscr.refresh()
    stdscr.getkey()


def load_text():
    with open('text.txt', 'r') as f:
        lines = [i.strip() for i in f.readlines()]
        return (' '.join(random.sample(lines, 20)))

def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(1, 0, f'WPM:{wpm}')
    stdscr.addstr(0,0,target)
    for x,i in enumerate(current):
        correct = target[x]
        if i==correct:
            stdscr.addstr(0, x, i, curses.color_pair(1))
        else:
            stdscr.addstr(0, x, target[x], curses.color_pair(2))

def wpm_test(stdscr):
    target_text = load_text()
    current_text = []    
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time()-start_time, 1)
        wpm = round((len(current_text)/(time_elapsed/60))/5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()
        
        if ''.join(current_text)==target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue
        
        if ord(key)==27:
            break

        if key in ('KEY_BACKSPACE', '\b', '^?', '\x7f'):
            if current_text:
                current_text.pop()
        elif len(current_text)<len(target_text):
            current_text.append(key)
    



def main(stdscr):
    curses.init_pair(1,curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3,curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(2,0,'You have completed the test! Press any key to continue or ESC to exit.')
        key = stdscr.getkey()
        if ord(key)==27:
            break


wrapper(main)
