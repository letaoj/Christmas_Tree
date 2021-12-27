#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Lock, Thread
from random import choice, getrandbits, uniform
from os import system, name
from time import sleep
from playsound import playsound

class ChristmasTree:
    def __init__(self):
        # read input from tree.txt and convert to a list
        with open('tree.txt', 'r') as input:
            self.tree = list(input.read())
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
        yellow = True
        while True:
            for idx in indexes:
                if color == 'yellow':
                    self.tree[idx] = self.colored_dot(color) if yellow else '●'
                else:
                    self.tree[idx] = self.colored_dot(color) if bool(getrandbits(1)) else '●'
            self.mutex.acquire()
            system('cls' if name == 'nt' else 'clear')
            print("Merry Christmas, Chengjin!\n")
            print(''.join(self.tree))
            self.mutex.release()

            yellow = not yellow
            
            sleep(uniform(.5, 1.5))
    
    def move_flake(self):
        generate = False

        while True:
            # moving all flakes
            for idx in reversed(self.flake):
                if self.tree[idx] != ' ' and idx + 27 < len(self.tree) and self.tree[idx + 27] == ' ':
                    self.tree[idx + 27] = self.tree[idx]
                self.tree[idx] = ' '
            
            # generate new flakes at the top
            if generate:
                for idx in self.top:
                    self.tree[idx] = self.get_snowflake() if bool(getrandbits(1)) else ' '
            generate = not generate

            # print the tree
            self.mutex.acquire()
            system('cls' if name == 'nt' else 'clear')
            print("Merry Christmas, Chengjin!\n")
            print(''.join(self.tree))
            self.mutex.release()
            
            sleep(uniform(.5, 1.5))

    def populate_colors(self):
        self.yellow = []
        self.red = []
        self.green = []
        self.blue = []
        self.flake = []
        self.top = []

        for i, c in enumerate(self.tree):
            if c == 'Y':
                self.yellow.append(i)
                self.tree[i] = '●'
            if c == 'R':
                self.red.append(i)
                self.tree[i] = '●'
            if c == 'G':
                self.green.append(i)
                self.tree[i] = '●'
            if c == 'B':
                self.blue.append(i)
                self.tree[i] = '●'
            if c == ' ':
                if i < 26:
                    self.top.append(i)
                    self.tree[i] = self.get_snowflake() if bool(getrandbits(1)) else ' '
                self.flake.append(i)
    def get_snowflake(self):
        return '❄️'
    def get_random_flake(self):
        flake=chr(choice(range(0x2740, 0x2749)))
        return flake

def main():
    christmas_tree = ChristmasTree()

    ty = Thread(target=christmas_tree.lights, args=('yellow', christmas_tree.yellow), daemon=True)
    tr = Thread(target=christmas_tree.lights, args=('red', christmas_tree.red), daemon=True)
    tg = Thread(target=christmas_tree.lights, args=('green', christmas_tree.green), daemon=True)
    tb = Thread(target=christmas_tree.lights, args=('blue', christmas_tree.blue), daemon=True)
    sf = Thread(target=christmas_tree.move_flake, daemon=True)
    playsound("Jingle_Bells.mp3", False)

    for t in [ty, tr, tg, tb, sf]:
        t.start()
    for t in [ty, tr, tg, tb, sf]:
        t.join()

if __name__ == '__main__':
    main()