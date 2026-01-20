import curses
import random
import time

def setup_screen():
    """Initializes the curses screen settings."""
    screen = curses.initscr()
    # Turn off key echoing
    curses.noecho()
    # Hide the cursor
    curses.curs_set(0)
    # Allow instant key input
    screen.keypad(1)
    # Set the screen refresh rate (game speed in ms)
    screen.timeout(100)
    return screen

def create_food(snake, max_y, max_x):
    """Generates food at a random position not occupied by the snake."""
    while True:
        # Generate coordinates within the border
        y = random.randint(1, max_y - 2)
        x = random.randint(1, max_x - 2)
        # Ensure food doesn't spawn on the snake
        if [y, x] not in snake:
            return [y, x]

def draw_game(screen, snake, food, score, max_y, max_x):
    """Clears the screen and draws the game elements."""
    screen.clear()

    # Draw the boundary (optional visual border)
    for y in range(max_y):
        screen.addch(y, 0, '#')
        screen.addch(y, max_x - 1, '#')
    for x in range(max_x):
        screen.addch(0, x, '#')
        screen.addch(max_y - 1, x, '#')

    # Draw food
    screen.addch(int(food[0]), int(food[1]), '*')

    # Draw snake
    for i, (y, x) in enumerate(snake):
        # Head 'O', body 'o'
        char = 'O' if i == 0 else 'o'
        screen.addch(int(y), int(x), char)

    # Display score
    score_text = "Score: {}".format(score)
    screen.addstr(0, 2, score_text) # Display score inside the top border

    screen.refresh()

def game_loop(screen):
    """The main game loop and logic."""
    max_y, max_x = screen.getmaxyx()

    # Initial snake position (list of [y, x])
    snake = [
        [max_y // 4, max_x // 4],
        [max_y // 4, max_x // 4 - 1],
        [max_y // 4, max_x // 4 - 2]
    ]

    food = create_food(snake, max_y, max_x)
    
    # Initial direction (RIGHT)
    key = curses.KEY_RIGHT
    score = 0
    game_over = False

    while not game_over:
        # Get next key press
        next_key = screen.getch()
        # If no key is pressed, keep the current direction
        key = key if next_key == -1 else next_key

        # 1. Calculate new head position
        new_head = [snake[0][0], snake[0][1]]
        
        if key == curses.KEY_DOWN:
            new_head[0] += 1
        elif key == curses.KEY_UP:
            new_head[0] -= 1
        elif key == curses.KEY_LEFT:
            new_head[1] -= 1
        elif key == curses.KEY_RIGHT:
            new_head[1] += 1
        
        # Insert the new head
        snake.insert(0, new_head)

        # 2. Check for Game Over (Collision)
        
        # Hit the wall (0 or max_y - 1, 0 or max_x - 1)
        if (snake[0][0] in [0, max_y - 1] or 
            snake[0][1] in [0, max_x - 1] or
            # Hit itself (check if the head is in the rest of the body)
            snake[0] in snake[1:]): 
            game_over = True
            break

        # 3. Check for Eating Food
        
        if snake[0] == food:
            score += 10
            food = create_food(snake, max_y, max_x)
            # The snake grows because we DON'T pop the tail
        else:
            # Snake moves: Remove the tail
            snake.pop()

        # 4. Draw the game state
        draw_game(screen, snake, food, score, max_y, max_x)
        
        # Optional: Increase speed with score (decrease timeout)
        screen.timeout(100 - (score // 5))


    # Game Over Screen
    screen.clear()
    msg = "GAME OVER! Final Score: {}".format(score)
    screen.addstr(max_y // 2, max_x // 2 - len(msg) // 2, msg)
    screen.refresh()
    time.sleep(3) # Wait for 3 seconds before exiting


def main():
    screen = None
    try:
        # Setup curses
        screen = setup_screen()
        # Run the game
        game_loop(screen)
    except Exception as e:
        # Print error if something goes wrong outside the game loop
        print("An error occurred:", e)
    finally:
        # Always clean up curses settings
        if screen:
            curses.endwin()

if __name__ == '__main__':
    main()