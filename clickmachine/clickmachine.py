from __future__ import division

import time
import logging

logger = logging.getLogger('Click Machine')
logger.handlers = []
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

from pymouse import PyMouse # PyUserInput required
import math


class Mouse(PyMouse):
    MIN_DISTANCE = 30
    prev_position = None
    
    def move(self, x, y):
        super(Mouse, self).move(x, y)
        self.prev_position = x, y
    
    def click(self, x, y, button = 1):
        super(Mouse, self).click(x, y, button)
        self.prev_position = x, y
    
    def is_disturbed(self):
        time.sleep(0.005)
        x, y = self.position()
        if self.prev_position:
            px, py = self.prev_position
        else:
            px, py = x, y
        self.prev_position = x, y
        distance = math.sqrt((x - px)**2 + (y - py)**2)
        if distance > self.MIN_DISTANCE:
            return True
        return False

    def reset_disturbed(self):
        self.prev_position = None
mouse = Mouse()

from collections import namedtuple
    
from abc import ABCMeta, abstractmethod

import sys
import getpass

INTERVAL = 0.03

def basicConfig(**options):
    global INTERVAL
    INTERVAL = options['interval']
    
class Action:
    __metaclass__ = ABCMeta
    def repeat(self, times = None, interval = INTERVAL):
        return Repeat(self, times, interval)
    @abstractmethod
    def act(self):
        logger.info(`self`)
        if mouse.is_disturbed():
            mouse.reset_disturbed()
            getpass.getpass('KEEP YOUR HANDS OFF THE MOUSE!\n'
                            'Press <ENTER> to continue.')
            
            for n in reversed(xrange(2, 10 + 2)):
                print '\r\033[K' + ' <- '.join(map(str, range(1, n))) + ' \a',
                sys.stdout.flush()
                time.sleep(0.5)
                print '\b\b\b\b\033[K\a',
                sys.stdout.flush()
                time.sleep(0.5)
        

class Actions(Action):
    def __init__(self, *actions, **options):
        self.interval = options.get('interval', INTERVAL)
        if not all(isinstance(action, Action) for action in actions):
            raise TypeError
        self.actions = actions
    def interval(self, interval = INTERVAL):
        return Actions(*self.actions, interval = interval)
    def act(self):
        super(Actions, self).act()
        for action in self.actions:
            time.sleep(self.interval)
            action.act()
    def __repr__(self):
        return '{classname}({actions})'.format(
            classname = self.__class__.__name__,
            actions = ', '.join(map(repr, self.actions)))

import itertools
class Repeat ( namedtuple('Repeat', ['action', 'times', 'interval' ]), Action ):
    def __new__(cls, action , times = None, interval = INTERVAL):
        if not isinstance(action, Action):
            raise TypeError('Can\'t Repeat(object of {}). Should be an object of Move, Click, Sleep, Actions ...'.format(action.__class__.__name__))
        return super(Repeat, cls).__new__(cls, action, times, interval)
    def act(self):
        super(Repeat, self).act()
        if self.times:
            for _ in itertools.repeat(None, self.times):
                time.sleep(self.interval)
                self.action.act()
        else:
            while True:
                time.sleep(self.interval)
                self.action.act()
                
               
class Move(namedtuple('Move', [ 'x', 'y' ]),Action):
    def to_click(self):
        return Click(*self)
    def act(self):
        super(Move, self).act()
        mouse.move(self.x, self.y)

class Click(namedtuple('Click', ['x', 'y']), Action):
    def to_click(self):
        return Click(*self)
    def __new__(cls, x, y ):
        return super(Click, cls).__new__(cls, x,y)
    def act(self):
        super(Click, self).act()
        mouse.click(self.x, self.y)

# class Clicks(namedtuple('Clicks', [ 'x', 'y' , 'times', 'interval' ]), Action):
#     def to_click(self):
#         return Click(self.x, self.y)
#     def to_move(self):
#         return Move(self.x, self.y)
#     def __new__(cls, x, y ,  times = 1, interval = INTERVAL):
#         self = super(Clicks, cls).__new__(cls, x, y, times=times, interval=interval)
#         self.act = Repeat(Click(x, y), times, interval).act
#         return self

class Sleep(namedtuple('Sleep', ['seconds']), Action):
    def __new__(cls, seconds = 1):
        return super(Sleep, cls).__new__(cls, seconds)
    def act(self):
        super(Sleep, self).act()
        time.sleep(self.seconds)


class Number:
    __metaclass__=ABCMeta
Number.register(int)
from collections import namedtuple
class Coord(namedtuple('Coord', ['x', 'y'])):
    @staticmethod
    def mouse_relative_coord_locator():
        getpass.getpass('Move the mouse point to TOP-LEFT corner of your WORK SPACE.\n'
                        'Press <ENTER> to continue.')
        left, top = mouse.position()
        getpass.getpass('\nMove the mouse point to BOTTOM-RIGHT corner of your WORK SPACE.\n'
                        'Press <ENTER> to continue.')
        right, bottom = mouse.position()
        print 'work space: (left = {}, top = {} right = {}, bottom = {})'.format(left, top, right, bottom)
        while raw_input('\nGet current relative coordinate <Y/n>: ').strip() != 'n':
            x, y = mouse.position()
            print Coord((x- left) / (right - left), (y - top) / (bottom - top))
    @staticmethod
    def current_coord():
        return Coord(*mouse.position())

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Coord(self.x - other.x, self.y - other.y)
    def __truediv__(self, other):
        if isinstance(other, int):
            return Coord(self.x / other, self.y / other)
        return NotImplemented
    __div__ = __truediv__
    def __mul__(self, other):
        if isinstance(other, int):
            return Coord(self.x * other, self.y * other)
        return NotImplemented
    def n_points_to(self, end, n):
        diff = (end - self) / (n - 1)
        return [ self + diff*i for i in range(n) ]
    def mxn_points_to(self, end, m, n):
        xdiff = (end.x - self.x) / (m - 1)
        x_coords = [ self.x + xdiff*i for i in range(m) ]
        ydiff = (end.y - self.y) / (n - 1)
        y_coords = [ self.y + ydiff*i for i in range(n) ]
        return [ Coord(x, y) for x in x_coords for y in y_coords ]
    def project_to_space(self, left, top, right, bottom):
        return Coord(left + self.x * (right - left), top + self.y * (bottom - top))
    def to_click(self):
        return Click(*self)
    # def to_clicks(self, times = 1, interval = INTERVAL):
        # return Clicks(*self, times = times, interval = interval)
    def to_move(self):
        return Move(*self)

class CoordsMap(dict):
    def project_to_space(self, left, top, right, bottom):
        import operator
        project_to_the_space = operator.methodcaller('project_to_space',left, top, right, bottom)
        real_coords_map = CoordsMap()
        for name, coords in self.items():
            if isinstance(coords, list):
                real_coords_map[name] = map(project_to_the_space, coords)
            else:
                real_coords_map[name] = project_to_the_space(coords)
        return real_coords_map

        
if __name__ == '__main__':
    # Move 
    Move(500, 500).act()
    # Click one time
    Click(200, 200).act()
    # Click 3 times
    # Clicks(300, 300, times = 3, interval = 0.5).act()

    i_got_a_move = Actions(
        Move(200, 100),
        Move(300, 200),
        Repeat(Sleep(0.5), times = 3)
    )

    # Series actions
    i_got_more_moves = Actions(
            Move(500, 500),
            Click(200, 200),
            # Clicks(300, 300, times = 3, interval = 0.5),
            i_got_a_move
        ).interval(1).repeat()

    i_got_more_moves.act()
    

    
