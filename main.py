import curses
import logging

from sleepcounter.core.widget import BaseWidget


logging.basicConfig(
    format='%(asctime)s[%(name)s]:%(levelname)s:%(message)s',
    # stream=stdout,
    filename='logs.txt',
    level=logging.INFO,
)


class CursesWidget(BaseWidget):
    _X_OFFSET = 2
    _Y_OFFSET = 1

    def __init__(self, screen, calendar, label=None):
        self._screen = screen
        self._screen.clear()
        self._rows, self._cols = self._screen.getmaxyx()
        # draw a border around the whole screen...
        self._screen.border(0)
        super().__init__(calendar, label)

    def update(self):
        events = sorted(
            self._calendar.events,
            key=self._calendar.sleeps_to_event,
        )
        for idx, event in enumerate(events):
            description = f"{event.name:40s}"
            if event.today:
                status = "***TODAY***"
                attr = curses.A_STANDOUT
            else:
                status = (
                    str(event.sleeps_remaining)
                    + (' sleeps' if event.sleeps_remaining > 1 else ' sleep')
                )
                attr = curses.A_NORMAL
            message = f"{description}: {status}"
            self._screen.addstr(
                idx + self._Y_OFFSET,
                self._X_OFFSET,
                message,
                attr,
            )
        self._screen.refresh()

# loading a custom diary...
with open('diary.py') as file:
    exec(file.read())

assert 'CUSTOM_DIARY' in dir()

# main...
from sleepcounter.core.application import Application

def main(stdscr):
    app = Application(
        widgets=[CursesWidget(screen=stdscr, calendar=CUSTOM_DIARY),])
    app.start()
    stdscr.getkey()

# runs the callable inside a try except that restores the state of the terminal
# if the code dies...
curses.wrapper(main)
