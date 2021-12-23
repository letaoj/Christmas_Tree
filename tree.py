#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Lock, Thread
from random import uniform
from os import system, name
from time import sleep
from playsound import playsound

class ChristmasTree:
    def __init__(self):
        # read input from tree.txt and convert to a list
        with open('tree.txt', 'r') as input:
            self.tree = list(input.read().rstrip())
        self.mutex = Lock()
        self.populate_colors()

    def colored_dot(self, color):
        return {
            'red': f'\033[91m●\033[0m',
            'green': f'\033[92m●\033[0m',
            'yellow': f'\033[93m●\033[0m',
            'blue': f'\033[94m●\033[0m',
        }[color]     

    def lights(self, color, indexes):
        off = True
        while True:
            for idx in indexes:
                self.tree[idx] = self.colored_dot(color) if off else '●'

            self.mutex.acquire()
            system('cls' if name == 'nt' else 'clear')
            print(''.join(self.tree))
            self.mutex.release()

            off = not off

            sleep(uniform(.5, 1.5))

    def populate_colors(self):
        self.yellow = []
        self.red = []
        self.green = []
        self.blue = []

        for i, c in enumerate(self.tree):
            if c == 'Y':
                self.yellow.append(i)
                self.tree[i] = '⏺'
            if c == 'R':
                self.red.append(i)
                self.tree[i] = '⏺'
            if c == 'G':
                self.green.append(i)
                self.tree[i] = '⏺'
            if c == 'B':
                self.blue.append(i)
                self.tree[i] = '⏺'

def main():
    christmas_tree = ChristmasTree()

    ty = Thread(target=christmas_tree.lights, args=('yellow', christmas_tree.yellow), daemon=True)
    tr = Thread(target=christmas_tree.lights, args=('red', christmas_tree.red), daemon=True)
    tg = Thread(target=christmas_tree.lights, args=('green', christmas_tree.green), daemon=True)
    tb = Thread(target=christmas_tree.lights, args=('blue', christmas_tree.blue), daemon=True)
    playsound("Jingle_Bells.mp3", False)
    

    for t in [ty, tr, tg, tb]:
        t.start()
    for t in [ty, tr, tg, tb]:
        t.join()

if __name__ == '__main__':
    main()