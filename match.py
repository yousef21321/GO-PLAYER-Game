from game.go import Board, opponent_color
from game.ui import UI
import pygame
# from playsound import playsound
import time
from agent.search.search_agent import AlphaBetaAgent
import agent.util
from os.path import join
from argparse import ArgumentParser
import main2
from tkinter import *
from tkinter import messagebox


class Match:
    def __init__(self, agent_black=None, agent_white=None, gui=True, dir_save=None):
        """
        BLACK always has the first move on the center of the board.
        :param agent_black: agent or None(human)
        :param agent_white: agent or None(human)
        :param gui: if show GUI; always true if there are human playing
        :param dir_save: directory to save board image if GUI is shown; no save for None
        """
        self.agent_black = agent_black
        self.agent_white = agent_white

        self.board = Board(next_color='BLACK')

        gui = gui if agent_black and agent_white else True
        self.ui = UI() if gui else None
        self.dir_save = dir_save

        # Metadata
        self.time_elapsed = None

    @property
    def winner(self):
        return self.board.winner

    @property
    def next(self):
        return self.board.next

    @property
    def counter_move(self):
        return self.board.counter_move

    def start(self):
        if self.ui:
            self._start_with_ui()
        else:
            self._start_without_ui()

    def _start_with_ui(self):
        """Start the game with GUI."""
        self.ui.initialize()
        self.time_elapsed = time.time()

        x = int(input("Enter x :"))
        y = int(input("Enter y :"))
        m=x
        n=y
        first_move = (m , n)
        self.board.put_stone(first_move, check_legal=False)
        self.ui.draw(first_move, opponent_color(self.board.next))

        # Take turns to play move
        while self.board.winner is None:
            if self.board.next == 'WHITE':

                point = self.perform_one_move(self.agent_black)

            else:
                point = self.perform_one_move(self.agent_white)

            # Check if action is legal
            if point not in self.board.legal_actions:
                continue

            # Apply action
            prev_legal_actions = self.board.legal_actions.copy()
            self.board.put_stone(point, check_legal=False)
            # Remove previous legal actions on board
            for action in prev_legal_actions:
                self.ui.remove(action)
            # Draw new point
            self.ui.draw(point, opponent_color(self.board.next))
            # Update new legal actions and any removed groups
            if self.board.winner:
                for group in self.board.removed_groups:
                    for point in group.points:
                        self.ui.remove(point)
                if self.board.end_by_no_legal_actions:
                    print(
                        'Game ends early (no legal action is available for %s)' % self.board.next)
            else:
                for action in self.board.legal_actions:
                    self.ui.draw(action, 'BLUE', 6)

        self.time_elapsed = time.time() - self.time_elapsed
        if self.dir_save:
            path_file = join(self.dir_save, 'go_' + str(time.time()) + '.jpg')
            self.ui.save_image(path_file)
            print('Board image saved in file ' + path_file)

    def _start_without_ui(self):
        """Start the game without GUI. Only possible when no human is playing."""
        # First move is fixed on the center of board

        self.time_elapsed = time.time()
        x = int(input("Enter x :"))
        y = int(input("Enter y :"))
        m=x
        n=y
        first_move = (m , n)
        self.board.put_stone(first_move, check_legal=False)

        # Take turns to play move
        while self.board.winner is None:
            if self.board.next == 'BLACK':
                point = self.perform_one_move(self.agent_black)
            else:
                point = self.perform_one_move(self.agent_white)

            # Apply action
            # Assuming agent always gives legal actions
            self.board.put_stone(point, check_legal=False)

        if self.board.end_by_no_legal_actions:
            print('Game ends early (no legal action is available for %s)' %
                  self.board.next)

        self.time_elapsed = time.time() - self.time_elapsed

    def perform_one_move(self, agent):
        if agent:
            return self._move_by_agent(agent)
        else:
            return self._move_by_human()

    def _move_by_agent(self, agent):
        if self.ui:
            pygame.time.wait(200)
            pygame.event.get()
        return agent.get_action(self.board)

    def _move_by_human(self):
        while True:
            pygame.time.wait(200)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.ui.outline.collidepoint(event.pos):
                        x = int(round(((event.pos[0] - 5) / 40.0), 0))
                        y = int(round(((event.pos[1] - 5) / 40.0), 0))
                        point = (x, y)
                        stone = self.board.exist_stone(point)
                        if not stone:
                            return point


def get_args():
    parser = ArgumentParser('Mini Go Game')
    parser.add_argument('-b', '--agent_black', default='minimax',
                        help='possible agents: human; DEFAULT is minimax')
    parser.add_argument('-w', '--agent_white', default=None,
                        help='possible agents: minimax; DEFAULT is None (human)')
    parser.add_argument('-d', '--search_depth', type=int, default=1,
                        help='the search depth for searching agents if applicable; DEFAULT is 1')
    parser.add_argument('-g', '--gui', type=bool, default=True,
                        help='if show GUI; always true if human plays; DEFAULT is True')
    parser.add_argument('-s', '--dir_save', default=None,
                        help='if not None, save the image of last board state to this directory; DEFAULT is None')
    return parser.parse_args()

# Black or White
def get_agent(whoPlay_agent, color, depth):#Depth اخر نود من الشجره الى عندى لمااجى احط الاستون 
    if whoPlay_agent is None:
        return None
   # whoPlay_agent = whoPlay_agent
    if whoPlay_agent == 'none':
        return None
    elif whoPlay_agent == 'minimax':
        return AlphaBetaAgent(color, depth=depth)
    else:
        raise ValueError('Invalid agent for ' + color)


def main():
    args = get_args()
    depth = args.search_depth
    agent_black = get_agent(args.agent_white, 'WHITE', depth)#black Ai
    agent_white = get_agent(args.agent_black, 'BLACK', depth)#white human
    gui = args.gui
    dir_save = args.dir_save

    print('Agent for BLACK: ' + (str(agent_black) if agent_black else 'Human'))
    print('Agent for WHITE: ' + (str(agent_white) if agent_white else 'Human'))
    if dir_save:
        print('Directory to save board image: ' + dir_save)

    match = Match(agent_black=agent_black,
                  agent_white=agent_white, gui=gui, dir_save=dir_save)

    print('Match starts!')

    match.start()
    
    
    while True:
         
        messagebox.showinfo("Score", match.winner + 'wins!')
        break

    print('Match ends in ' + str(match.time_elapsed) + ' seconds')
    print('Match ends in ' + str(match.counter_move) + ' moves')


if __name__ == '__main__':
    main()
