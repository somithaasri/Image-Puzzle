import pygame
import random
from puzzle import Puzzle

# Constants
WIDTH, HEIGHT = 800, 600
IMAGE_PATH = "image.jpg"  # Replace with the path to your image
IMAGE_SIZE = (600, 600)   # Size to scale the image
PUZZLE_SIZE = (3, 3)      # Puzzle size (3x3 grid)
POS = (100, 50)           # Position of the puzzle on the screen

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Image Puzzle')

    # Create puzzle instance
    puzzle = Puzzle(IMAGE_PATH, IMAGE_SIZE, PUZZLE_SIZE, POS, show_scramble=True)

    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill((255, 255, 255))  # Fill the screen with a white background

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    puzzle.move_up()
                elif event.key == pygame.K_DOWN:
                    puzzle.move_down()
                elif event.key == pygame.K_LEFT:
                    puzzle.move_left()
                elif event.key == pygame.K_RIGHT:
                    puzzle.move_right()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    puzzle.handle_click(event.pos)

        # Check if the puzzle is solved
        if puzzle.is_solved():
            print("Puzzle solved!")

        # Render the puzzle
        puzzle.render(screen)

        pygame.display.flip()  # Update the display
        clock.tick(60)  # Frame rate (60 FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
