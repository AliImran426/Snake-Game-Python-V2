import random
import curses
import time
import os

HIGHSCORE_FILE = "highscore.txt"

def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read() or 0)
    return 0

def save_highscore(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))


def menu(stdscr):
    stdscr.clear()
    sh, sw = stdscr.getmaxyx()
    title = "🐍 S N A K E   G A M E 🐍"
    start = "Press ENTER to Start"
    quit_txt = "Press Q to Quit"

    stdscr.addstr(sh//2 - 2, sw//2 - len(title)//2, title)
    stdscr.addstr(sh//2, sw//2 - len(start)//2, start)
    stdscr.addstr(sh//2 + 1, sw//2 - len(quit_txt)//2, quit_txt)
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == ord('\n'):
            return
        if key in [ord('q'), ord('Q')]:
            exit()


def game(stdscr):
    curses.curs_set(0)
    sh, sw = stdscr.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.keypad(1)
    w.timeout(100)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Snake
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)     # Food
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)   # Border
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Score

    # Draw border
    for i in range(sw):
        w.addch(0, i, '#', curses.color_pair(3))
        w.addch(sh-1, i, '#', curses.color_pair(3))
    for i in range(sh):
        w.addch(i, 0, '#', curses.color_pair(3))
        w.addch(i, sw-1, '#', curses.color_pair(3))

    snk_x = sw // 4
    snk_y = sh // 2
    snake = [[snk_y, snk_x],
             [snk_y, snk_x-1],
             [snk_y, snk_x-2]]

    food = [random.randint(1, sh-2), random.randint(1, sw-2)]
    w.addch(food[0], food[1], curses.ACS_PI, curses.color_pair(2))

    key = curses.KEY_RIGHT
    score = 0
    highscore = load_highscore()
    paused = False

    while True:
        # HUD
        w.addstr(0, 2, f" Score: {score} ", curses.color_pair(4))
        w.addstr(0, sw-20, f" High: {highscore} ", curses.color_pair(4))

        if paused:
            w.addstr(sh//2, sw//2 - 5, "PAUSED", curses.A_BOLD)
            w.refresh()
            k = w.getch()
            if k in [ord('p'), ord('P')]:
                paused = False
            continue

        next_key = w.getch()
        if next_key in [ord('p'), ord('P')]:
            paused = True
            continue
        key = key if next_key == -1 else next_key

        head = [snake[0][0], snake[0][1]]
        if key == curses.KEY_DOWN: head[0] += 1
        if key == curses.KEY_UP: head[0] -= 1
        if key == curses.KEY_LEFT: head[1] -= 1
        if key == curses.KEY_RIGHT: head[1] += 1

        snake.insert(0, head)

        if snake[0] == food:
            score += 1
            if score > highscore:
                highscore = score
                save_highscore(highscore)
            food = None
            while food is None:
                nf = [random.randint(1, sh-2), random.randint(1, sw-2)]
                food = nf if nf not in snake else None
            w.addch(food[0], food[1], curses.ACS_PI, curses.color_pair(2))
        else:
            tail = snake.pop()
            w.addch(tail[0], tail[1], ' ')

        if (snake[0][0] in [0, sh-1] or
            snake[0][1] in [0, sw-1] or
            snake[0] in snake[1:]):
            w.clear()
            w.addstr(sh//2 - 1, sw//2 - 8, f"Game Over!")
            w.addstr(sh//2, sw//2 - 12, f"Score: {score}  High: {highscore}")
            w.addstr(sh//2 + 2, sw//2 - 15, "Press R to Restart or Q to Quit")
            w.refresh()

            while True:
                k = w.getch()
                if k in [ord('r'), ord('R')]:
                    return "restart"
                if k in [ord('q'), ord('Q')]:
                    exit()

        w.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD, curses.color_pair(1))


def main(stdscr):
    while True:
        menu(stdscr)
        result = game(stdscr)
        if result != "restart":
            break


curses.wrapper(main)