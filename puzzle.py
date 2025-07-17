import pygame
import random
import os
from pygame.locals import *

class Puzzle:
    def __init__(self, image_path, image_size, puzzle_size, pos, show_scramble=False):
        self.image_path = image_path
        self.image_size = image_size
        self.puzzle_size = puzzle_size
        self.pos = pos

        # Load and scale the image
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, image_size)

        # Create the puzzle grid
        self.tile_width = image_size[0] // puzzle_size[0]
        self.tile_height = image_size[1] // puzzle_size[1]
        
        self.tiles = []
        for i in range(puzzle_size[1]):
            for j in range(puzzle_size[0]):
                x = j * self.tile_width
                y = i * self.tile_height
                self.tiles.append(pygame.Surface((self.tile_width, self.tile_height)))
                self.tiles[-1].blit(self.image, (0, 0), (x, y, self.tile_width, self.tile_height))
        
        self.puzzle = [[(i * puzzle_size[0]) + j for j in range(puzzle_size[0])] for i in range(puzzle_size[1])]
        self.void = [puzzle_size[1] - 1, puzzle_size[0] - 1]  # The empty space is at the bottom-right corner

        if show_scramble:
            self.shuffle()

    def shuffle(self):
        # Shuffle the puzzle by randomly swapping the empty space
        moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        for _ in range(1000):  # Shuffle the puzzle 1000 times
            move = random.choice(moves)
            self.move_empty(*move)

    def move_empty(self, dx, dy):
        # Calculate the new position of the empty space
        new_row = self.void[0] + dy
        new_col = self.void[1] + dx

        if 0 <= new_row < self.puzzle_size[1] and 0 <= new_col < self.puzzle_size[0]:
            self.puzzle[self.void[0]][self.void[1]], self.puzzle[new_row][new_col] = self.puzzle[new_row][new_col], self.puzzle[self.void[0]][self.void[1]]
            self.void = [new_row, new_col]

    def render(self, screen):
        # Render the puzzle grid
        for row in range(self.puzzle_size[1]):
            for col in range(self.puzzle_size[0]):
                tile_number = self.puzzle[row][col]
                if tile_number == self.puzzle_size[0] * self.puzzle_size[1] - 1:  # The empty space
                    continue
                screen.blit(self.tiles[tile_number], (self.pos[0] + col * self.tile_width, self.pos[1] + row * self.tile_height))

    def move_up(self):
        self.move_empty(-1, 0)

    def move_down(self):
        self.move_empty(1, 0)

    def move_left(self):
        self.move_empty(0, -1)

    def move_right(self):
        self.move_empty(0, 1)

    def is_solved(self):
        # Check if the puzzle is solved
        return self.puzzle == [[(i * self.puzzle_size[0]) + j for j in range(self.puzzle_size[0])] for i in range(self.puzzle_size[1])]

    def handle_click(self, pos):
        """Handle mouse click to move the tile into the empty space."""
        col = (pos[0] - self.pos[0]) // self.tile_width
        row = (pos[1] - self.pos[1]) // self.tile_height

        # Ensure the click is within bounds of the puzzle grid
        if 0 <= col < self.puzzle_size[0] and 0 <= row < self.puzzle_size[1]:
            # Check if the clicked tile is adjacent to the empty space
            if (abs(self.void[0] - row) == 1 and self.void[1] == col) or (abs(self.void[1] - col) == 1 and self.void[0] == row):
                # Swap the clicked tile with the empty space
                self.puzzle[self.void[0]][self.void[1]], self.puzzle[row][col] = self.puzzle[row][col], self.puzzle[self.void[0]][self.void[1]]
                self.void = [row, col]
