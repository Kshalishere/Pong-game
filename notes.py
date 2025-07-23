import pygame, sys, random, os  # Import necessary libraries for game, system, randomness, and file operations

pygame.init()  # Initialize all imported pygame modules
pygame.mixer.init()  # Initialize the mixer module for sound

class SoundManager:  # Define a class to manage game sounds
    def __init__(self):  # Constructor for SoundManager
        pygame.mixer.music.load("THEME.wav")  # Load the background music file
        pygame.mixer.music.set_volume(0.5)  # Set the music volume to 50%
        pygame.mixer.music.play(-1)  # Play the music in a continuous loop
        self.hit_sound = pygame.mixer.Sound('audio_shot.mp3')  # Load the hit sound effect
    def play_hit(self):  # Method to play the hit sound
        self.hit_sound.play()  # Play the hit sound

sound_manager = SoundManager()  # Create an instance of SoundManager

WIDTH, HEIGHT = 1280, 720  # Set the width and height of the game window
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))  # Create the game window with the specified size
pygame.display.set_caption("Pong!")  # Set the window title to "Pong!"
FONT = pygame.font.SysFont("Consolas", int(WIDTH / 20))  # Set the font and size for game text
CLOCK = pygame.time.Clock()  # Create a clock object to control the frame rate
shop_button = pygame.Surface((300, 200))  # Create a surface for the shop button
shop_button.fill("red")  # Fill the shop button with red color
shop_button_text = FONT.render('Shop', True, 'white')  # Render the text "Shop" in white
shop_button.blit(shop_button_text, (shop_button.get_width() // 2 - shop_button_text.get_width() // 2, shop_button.get_height() // 2 - shop_button_text.get_height() // 2))  # Center the text on the button

inventory_button_width = 320  # Set the width of the inventory button
inventory_button_height = 60  # Set the height of the inventory button
inventory_button = pygame.Surface((inventory_button_width, inventory_button_height))  # Create a surface for the inventory button
inventory_button.fill("green")  # Fill the inventory button with green color
inventory_button_text = FONT.render('Inventory', True, 'white')  # Render the text "Inventory" in white
inventory_button.blit(inventory_button_text, (inventory_button.get_width() // 2 - inventory_button_text.get_width() // 2, inventory_button.get_height() // 2 - inventory_button_text.get_height() // 2))  # Center the text on the button

player_score = 0  # Initialize the player's score to 0
opponent_score = 0  # Initialize the opponent's score to 0
coins = 50  # Initialize the coin count to 0
player_paddle_color = "white"  # Set the default paddle color to white
inventory = []  # Create an empty list to store owned paddles

def reset_ball():  # Function to reset the ball to the center with random direction
    return pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, 20), random.choice([-1, 1]), random.choice([-1, 1])  # Return new ball rect and random x/y directions

def draw_menu():  # Function to draw the main menu
    SCREEN.fill("Black")  # Fill the background with black
    title_text = FONT.render("Pong!", True, "white")  # Render the game title
    startbot_text = FONT.render("Press Enter to start against bot", True, "white")  # Render the start vs bot text
    startfriend_text = FONT.render("Press F to start against friend", True, "white")  # Render the start vs friend text
    credits_text = FONT.render("Created by Kaushal", True, "white")  # Render the credits text
    coins_text = FONT.render(f"Coins: {coins}", True, "yellow")  # Render the coins count

    SCREEN.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, HEIGHT / 2 - 260))  # Draw the title on screen
    SCREEN.blit(startbot_text, (WIDTH / 2 - startbot_text.get_width() / 2, HEIGHT / 2 - 100))  # Draw the bot start text
    SCREEN.blit(startfriend_text, (WIDTH / 2 - startfriend_text.get_width() / 2, HEIGHT / 2 - 50))  # Draw the friend start text
    SCREEN.blit(credits_text, (WIDTH / 2 - credits_text.get_width() / 2, HEIGHT / 2 + 200))  # Draw the credits
    SCREEN.blit(coins_text, (WIDTH - 400, 50))  # Draw the coins count
    SCREEN.blit(shop_button, (WIDTH - 1200, HEIGHT - 700))  # Draw the shop button
    SCREEN.blit(inventory_button, (20, HEIGHT - inventory_button_height - 20))  # Draw the inventory button

def draw_difficulty_select():  # Function to draw the difficulty selection screen
    SCREEN.fill("Black")  # Fill the background with black
    prompt = FONT.render("Enter your difficulty level (1-3):", True, "white")  # Render the prompt text
    easy = FONT.render("1: Easy", True, "green")  # Render the easy option
    medium = FONT.render("2: Medium", True, "yellow")  # Render the medium option
    hard = FONT.render("3: Hard", True, "red")  # Render the hard option
    SCREEN.blit(prompt, (WIDTH / 2 - prompt.get_width() / 2, HEIGHT / 2 - 100))  # Draw the prompt
    SCREEN.blit(easy, (WIDTH / 2 - easy.get_width() / 2, HEIGHT / 2))  # Draw the easy option
    SCREEN.blit(medium, (WIDTH / 2 - medium.get_width() / 2, HEIGHT / 2 + 60))  # Draw the medium option
    SCREEN.blit(hard, (WIDTH / 2 - hard.get_width() / 2, HEIGHT / 2 + 120))  # Draw the hard option

def draw_game(player, opponent, ball, player_score, opponent_score, coins, player_paddle_color):  # Function to draw the game screen
    SCREEN.fill("Black")  # Fill the background with black
    pygame.draw.rect(SCREEN, player_paddle_color, player)  # Draw the player's paddle
    pygame.draw.rect(SCREEN, "white", opponent)  # Draw the opponent's paddle
    pygame.draw.ellipse(SCREEN, "white", ball)  # Draw the ball

    player_text = FONT.render(str(player_score), True, "white")  # Render the player's score
    opponent_text = FONT.render(str(opponent_score), True, "white")  # Render the opponent's score
    coins_text = FONT.render(f"Coins: {coins}", True, "yellow")  # Render the coins count

    SCREEN.blit(player_text, (WIDTH / 2 + 50, 50))  # Draw the player's score
    SCREEN.blit(opponent_text, (WIDTH / 2 - 100, 50))  # Draw the opponent's score
    SCREEN.blit(coins_text, (WIDTH - 400, 50))  # Draw the coins count

def show_inventory_window():  # Function to show the inventory window
    global player_paddle_color  # Use the global paddle color variable
    overlay = pygame.Surface((WIDTH, HEIGHT))  # Create an overlay surface
    overlay.set_alpha(240)  # Set the overlay transparency
    overlay.fill((30, 30, 30))  # Fill the overlay with dark gray
    SCREEN.blit(overlay, (0, 0))  # Draw the overlay on the screen

    close_button_size = 50  # Set the close button size
    close_button_rect = pygame.Rect(WIDTH - close_button_size - 30, 30, close_button_size, close_button_size)  # Create the close button rectangle
    pygame.draw.rect(SCREEN, (200, 0, 0), close_button_rect, border_radius=8)  # Draw the close button
    close_text = FONT.render('X', True, 'white')  # Render the close button text
    SCREEN.blit(close_text, (close_button_rect.x + close_button_size // 2 - close_text.get_width() // 2, close_button_rect.y + close_button_size // 2 - close_text.get_height() // 2))  # Center the close text

    title = FONT.render('Inventory', True, 'white')  # Render the inventory title
    SCREEN.blit(title, (60, 60))  # Draw the inventory title

    equip_buttons = []  # List to store equip button rectangles and paddle types

    if inventory:  # If the player owns paddles
        for idx, item in enumerate(inventory):  # Loop through each paddle
            item_name = item.replace('_paddle', '').capitalize()  # Get the paddle name
            item_text = FONT.render(item_name, True, 'white')  # Render the paddle name
            y_pos = 150 + idx * 60  # Calculate the y position for this item
            SCREEN.blit(item_text, (100, y_pos))  # Draw the paddle name

            button_width, button_height = 140, 40  # Set the equip button size
            button_x = 350  # Set the x position for the button
            button_y = y_pos  # Set the y position for the button
            equip_rect = pygame.Rect(button_x, button_y, button_width, button_height)  # Create the equip button rectangle
            is_equipped = (player_paddle_color == item.replace('_paddle', ''))  # Check if this paddle is equipped
            button_color = (100, 200, 100) if is_equipped else (70, 70, 200)  # Set button color based on equipped status
            pygame.draw.rect(SCREEN, button_color, equip_rect, border_radius=8)  # Draw the equip button
            btn_text = 'Equipped' if is_equipped else 'Equip'  # Set the button text
            btn_text_render = FONT.render(btn_text, True, 'white')  # Render the button text
            SCREEN.blit(btn_text_render, (button_x + button_width // 2 - btn_text_render.get_width() // 2, button_y + button_height // 2 - btn_text_render.get_height() // 2))  # Center the button text
            equip_buttons.append((equip_rect, item.replace('_paddle', '')))  # Add the button and paddle type to the list
    else:  # If no paddles are owned
        empty_text = FONT.render('No paddles owned.', True, 'gray')  # Render the empty inventory text
        SCREEN.blit(empty_text, (100, 150))  # Draw the empty inventory text

    pygame.display.update()  # Update the display
    running = True  # Set the running flag to True
    while running:  # Loop until the window is closed
        for event in pygame.event.get():  # Get all events
            if event.type == pygame.QUIT:  # If the window is closed
                pygame.quit()  # Quit pygame
                sys.exit()  # Exit the program
            elif event.type == pygame.MOUSEBUTTONDOWN:  # If the mouse is clicked
                if close_button_rect.collidepoint(event.pos):  # If the close button is clicked
                    running = False  # Close the inventory window
                for equip_rect, paddle_color in equip_buttons:  # Check all equip buttons
                    if equip_rect.collidepoint(event.pos):  # If an equip button is clicked
                        player_paddle_color = paddle_color  # Equip the selected paddle
            elif event.type == pygame.KEYDOWN:  # If a key is pressed
                if event.key == pygame.K_ESCAPE:  # If the escape key is pressed
                    running = False  # Close the inventory window

        SCREEN.blit(overlay, (0, 0))  # Redraw the overlay
        pygame.draw.rect(SCREEN, (200, 0, 0), close_button_rect, border_radius=8)  # Redraw the close button
        SCREEN.blit(close_text, (close_button_rect.x + close_button_size // 2 - close_text.get_width() // 2, close_button_rect.y + close_button_size // 2 - close_text.get_height() // 2))  # Redraw the close text
        SCREEN.blit(title, (60, 60))  # Redraw the inventory title
        equip_buttons = []  # Reset the equip buttons list
        if inventory:  # If paddles are owned
            for idx, item in enumerate(inventory):  # Loop through each paddle
                item_name = item.replace('_paddle', '').capitalize()  # Get the paddle name
                item_text = FONT.render(item_name, True, 'white')  # Render the paddle name
                y_pos = 150 + idx * 60  # Calculate the y position
                SCREEN.blit(item_text, (100, y_pos))  # Draw the paddle name
                button_width, button_height = 140, 40  # Set the button size
                button_x = 350  # Set the x position
                button_y = y_pos  # Set the y position
                equip_rect = pygame.Rect(button_x, button_y, button_width, button_height)  # Create the button rectangle
                is_equipped = (player_paddle_color == item.replace('_paddle', ''))  # Check if equipped
                button_color = (100, 200, 100) if is_equipped else (70, 70, 200)  # Set button color
                pygame.draw.rect(SCREEN, button_color, equip_rect, border_radius=8)  # Draw the button
                btn_text = 'Equipped' if is_equipped else 'Equip'  # Set button text
                btn_text_render = FONT.render(btn_text, True, 'white')  # Render button text
                SCREEN.blit(btn_text_render, (button_x + button_width // 2 - btn_text_render.get_width() // 2, button_y + button_height // 2 - btn_text_render.get_height() // 2))  # Center button text
                equip_buttons.append((equip_rect, item.replace('_paddle', '')))  # Add to list
        else:  # If no paddles are owned
            empty_text = FONT.render('No paddles owned.', True, 'gray')  # Render empty text
            SCREEN.blit(empty_text, (100, 150))  # Draw empty text
        pygame.display.update()  # Update the display

def shop():  # Function to show the shop window
    global coins, player_paddle_color  # Use global variables for coins and paddle color
    running = True  # Set running flag to True
    paddle_x = 100  # Set the x position for paddles
    blue_y = HEIGHT // 2 - 50  # Set the y position for blue paddle
    red_y = HEIGHT // 2 + 50  # Set the y position for red paddle
    orange_y = HEIGHT // 2 + 150  # Set the y position for orange paddle
    text_x = paddle_x + 20  # Set the x position for paddle text

    while running:  # Loop until shop is closed
        SCREEN.fill("black")  # Fill the background with black
        shop_text = FONT.render("Welcome to the shop", True, "white")  # Render shop title
        coins_text = FONT.render(f"Coins: {coins}", True, "yellow")  # Render coins count
        bluepaddle_surface = pygame.Surface((10, 100))  # Create blue paddle surface
        redpaddle_surface = pygame.Surface((10,100))  # Create red paddle surface
        redpaddle_surface.fill("red")  # Fill red paddle with red
        redpaddle_text = FONT.render("Red Paddle - 20", True, "white")  # Render red paddle text
        bluepaddle_surface.fill("blue")  # Fill blue paddle with blue
        bluepaddle_text = FONT.render("Blue Paddle - 10", True, "white")  # Render blue paddle text
        orangepaddle_surface = pygame.Surface((10, 100))  # Create orange paddle surface
        orangepaddle_surface.fill("orange")  # Fill orange paddle with orange
        orangepaddle_text = FONT.render("Orange Paddle - 30", True, "white")  # Render orange paddle text
        SCREEN.blit(coins_text, (WIDTH - 400, 50))  # Draw coins count
        SCREEN.blit(shop_text, (60,  20))  # Draw shop title
        SCREEN.blit(bluepaddle_surface, (paddle_x, blue_y))  # Draw blue paddle
        SCREEN.blit(bluepaddle_text, (text_x + 20, blue_y))  # Draw blue paddle text
        SCREEN.blit(redpaddle_surface, (paddle_x, red_y))  # Draw red paddle
        SCREEN.blit(redpaddle_text, (text_x + 20, red_y))  # Draw red paddle text
        SCREEN.blit(orangepaddle_surface, (paddle_x, orange_y))  # Draw orange paddle
        SCREEN.blit(orangepaddle_text, (text_x + 20, orange_y))  # Draw orange paddle text
        pygame.display.update()  # Update the display

        for event in pygame.event.get():  # Get all events
            if event.type == pygame.QUIT:  # If window is closed
                running = False  # Exit shop
            elif event.type == pygame.KEYDOWN:  # If a key is pressed
                if event.key == pygame.K_ESCAPE:  # If escape key is pressed
                    running = False  # Exit shop
            elif event.type == pygame.MOUSEBUTTONDOWN:  # If mouse is clicked
                mouse_pos = event.pos  # Get mouse position

                redpaddle_rect = redpaddle_surface.get_rect(topleft=(paddle_x, red_y))  # Get red paddle rect
                if redpaddle_rect.collidepoint(mouse_pos):  # If red paddle is clicked
                    if "red_paddle" in inventory:  # If already owned
                        already_owned = FONT.render("Red paddle already owned!", True, "white")  # Render already owned text
                        SCREEN.blit(already_owned, (paddle_x + 20, red_y + 150))  # Draw already owned text
                        pygame.display.update()  # Update display
                        pygame.time.delay(1000)  # Wait 1 second
                    elif coins >= 20:  # If enough coins
                        coins -= 20  # Deduct coins
                        player_paddle_color = "red"  # Set paddle color to red
                        inventory.append("red_paddle")  # Add to inventory
                        purchased_text = FONT.render("Red paddle purchased!", True, "white")  # Render purchased text
                        SCREEN.blit(purchased_text, (paddle_x + 20, red_y + 150))  # Draw purchased text
                        pygame.display.update()  # Update display
                        pygame.time.delay(1000)  # Wait 1 second
                    else:  # Not enough coins
                        broke_text = FONT.render("Not enough coins!", True, "white")  # Render not enough coins text
                        SCREEN.blit(broke_text, (paddle_x + 20, red_y + 150))  # Draw not enough coins text
                        pygame.display.update()  # Update display
                        pygame.time.delay(1000)  # Wait 1 second

                bluepaddle_rect = bluepaddle_surface.get_rect(topleft=(paddle_x, blue_y))  # Get blue paddle rect
                if bluepaddle_rect.collidepoint(mouse_pos):  # If blue paddle is clicked
                    if "blue_paddle" in inventory:  # If already owned
                        already_owned = FONT.render("Blue paddle already owned!", True, "white")  # Render already owned text
                        SCREEN.blit(already_owned, (paddle_x + 20, blue_y + 150))  # Draw already owned text
                        pygame.display.update()  # Update display
                        pygame.time.delay(1000)  # Wait 1 second
                    elif coins >= 10:  # If enough coins
                        coins -= 10  # Deduct coins
                        player_paddle_color = "blue"  # Set paddle color to blue
                        inventory.append("blue_paddle")  # Add to inventory
                        purchased_text = FONT.render("Blue paddle purchased!", True, "white")  # Render purchased text
                        SCREEN.blit(purchased_text, (paddle_x + 20, blue_y + 150))  # Draw purchased text
                        pygame.display.update()  # Update display
                        pygame.time.delay(1000)  # Wait 1 second
                    else:  # Not enough coins
                        broke_text = FONT.render("Not enough coins!", True, "white")  # Render not enough coins text
                        SCREEN.blit(broke_text, (paddle_x + 20, blue_y + 150))  # Draw not enough coins text
                        pygame.display.update()  # Update display
                        pygame.time.delay(1000)  # Wait 1 second

                orangepaddle_rect = orangepaddle_surface.get_rect(topleft=(paddle_x, orange_y))  # Get orange paddle rect
                if orangepaddle_rect.collidepoint(mouse_pos):  # If orange paddle is clicked
                    if "orange_paddle" in inventory:  # If already owned
                        already_owned = FONT.render("Orange paddle already owned!", True, "white")  # Render already owned text
                        SCREEN.blit(already_owned, (paddle_x + 20, orange_y + 150))  # Draw already owned text
                        pygame.display.update()  # Update display
                        pygame.time.delay(1000)  # Wait 1 second
                    elif coins >= 30:  # If enough coins
                        coins -= 30  # Deduct coins
                        player_paddle_color = "orange"  # Set paddle color to orange
                        inventory.append("orange_paddle")  # Add to inventory
                        purchased_text = FONT.render("Orange paddle purchased!", True, "white")  # Render purchased text
                        SCREEN.blit(purchased_text, (paddle_x + 20, orange_y + 150))  # Draw purchased text
                        pygame.display.update()  # Update display
                        pygame.time.delay(1000)  # Wait 1 second
                    else:  # Not enough coins
                        broke_text = FONT.render("Not enough coins!", True, "white")  # Render not enough coins text
                        SCREEN.blit(broke_text, (paddle_x + 20, orange_y + 150))  # Draw not enough coins text
                        pygame.display.update()  # Update display
                        pygame.time.delay(1000)  # Wait 1 second

def main():  # Main function to run the game
    global player_score, opponent_score, coins, player_paddle_color  # Use global variables
    state = "menu"  # Set initial state to menu
    bot_mode = True  # Set bot mode to True
    player = None  # Initialize player paddle
    opponent = None  # Initialize opponent paddle
    ball = None  # Initialize ball
    x_speed = 0  # Initialize ball x speed
    y_speed = 0  # Initialize ball y speed
    difficulty = 1  # Set default difficulty

    while True:  # Main game loop
        for event in pygame.event.get():  # Get all events
            if event.type == pygame.QUIT:  # If window is closed
                pygame.quit()  # Quit pygame
                sys.exit()  # Exit program
            if event.type == pygame.MOUSEBUTTONDOWN:  # If mouse is clicked
                shop_rect = shop_button.get_rect(topleft=(WIDTH - 1200, HEIGHT - 700))  # Get shop button rect
                inventory_rect = pygame.Rect(20, HEIGHT - inventory_button_height - 20, inventory_button_width, inventory_button_height)  # Get inventory button rect
                if shop_rect.collidepoint(event.pos):  # If shop button is clicked
                    shop()  # Open shop
                elif inventory_rect.collidepoint(event.pos):  # If inventory button is clicked
                    show_inventory_window()  # Open inventory
            if state == "menu":  # If in menu state
                if event.type == pygame.KEYDOWN:  # If key is pressed
                    if event.key == pygame.K_RETURN:  # If Enter is pressed
                        state = "difficulty_select"  # Go to difficulty select
                    elif event.key == pygame.K_f:  # If F is pressed
                        bot_mode = False  # Set bot mode to False (friend mode)
                        player = pygame.Rect(WIDTH - 100, HEIGHT // 2 - 50, 10, 100)  # Create player paddle
                        opponent = pygame.Rect(100, HEIGHT // 2 - 50, 10, 100)  # Create opponent paddle
                        ball, x_speed, y_speed = reset_ball()  # Reset ball
                        player_score = 0  # Reset player score
                        opponent_score = 0  # Reset opponent score
                        pygame.mixer.music.stop()  # Stop music
                        state = "game"  # Go to game state
            elif state == "difficulty_select":  # If in difficulty select state
                if event.type == pygame.KEYDOWN:  # If key is pressed
                    if event.key == pygame.K_1:  # If 1 is pressed
                        difficulty = 1  # Set difficulty to 1
                        bot_mode = True  # Set bot mode to True
                        player = pygame.Rect(WIDTH - 100, HEIGHT // 2 - 50, 10, 100)  # Create player paddle
                        opponent = pygame.Rect(100, HEIGHT // 2 - 50, 10, 100)  # Create opponent paddle
                        ball, x_speed, y_speed = reset_ball()  # Reset ball
                        player_score = 0  # Reset player score
                        opponent_score = 0  # Reset opponent score
                        pygame.mixer.music.stop()  # Stop music
                        state = "game"  # Go to game state
                    elif event.key == pygame.K_2:  # If 2 is pressed
                        difficulty = 2  # Set difficulty to 2
                        bot_mode = True  # Set bot mode to True
                        player = pygame.Rect(WIDTH - 100, HEIGHT // 2 - 50, 10, 100)  # Create player paddle
                        opponent = pygame.Rect(100, HEIGHT // 2 - 50, 10, 100)  # Create opponent paddle
                        ball, x_speed, y_speed = reset_ball()  # Reset ball
                        player_score = 0  # Reset player score
                        opponent_score = 0  # Reset opponent score
                        pygame.mixer.music.stop()  # Stop music
                        state = "game"  # Go to game state
                    elif event.key == pygame.K_3:  # If 3 is pressed
                        difficulty = 3  # Set difficulty to 3
                        bot_mode = True  # Set bot mode to True
                        player = pygame.Rect(WIDTH - 100, HEIGHT // 2 - 50, 10, 100)  # Create player paddle
                        opponent = pygame.Rect(100, HEIGHT // 2 - 50, 10, 100)  # Create opponent paddle
                        ball, x_speed, y_speed = reset_ball()  # Reset ball
                        player_score = 0  # Reset player score
                        opponent_score = 0  # Reset opponent score
                        pygame.mixer.music.stop()  # Stop music
                        state = "game"  # Go to game state
                    elif event.key == pygame.K_ESCAPE:  # If escape is pressed
                        state = "menu"  # Go back to menu
            elif state == "game":  # If in game state
                if event.type == pygame.KEYDOWN:  # If key is pressed
                    if event.key == pygame.K_ESCAPE:  # If escape is pressed
                        pygame.mixer.music.play(-1)  # Resume music
                        state = "menu"  # Go back to menu

        if state == "menu":  # If in menu state
            draw_menu()  # Draw the menu
        elif state == "difficulty_select":  # If in difficulty select state
            draw_difficulty_select()  # Draw the difficulty select screen
            pygame.display.update()  # Update the display
        elif state == "game":  # If in game state
            keys = pygame.key.get_pressed()  # Get all pressed keys
            if keys[pygame.K_UP] and player.top > 0:  # If up arrow is pressed and paddle is not at top
                player.top -= 4  # Move player paddle up
            if keys[pygame.K_DOWN] and player.bottom < HEIGHT:  # If down arrow is pressed and paddle is not at bottom
                player.bottom += 4  # Move player paddle down

            if bot_mode:  # If playing against bot
                bot_speed = 2 * difficulty  # Set bot speed based on difficulty
                if opponent.centery < ball.centery:  # If opponent paddle is above ball
                    opponent.top += bot_speed  # Move opponent paddle down
                if opponent.centery > ball.centery:  # If opponent paddle is below ball
                    opponent.top -= bot_speed  # Move opponent paddle up
            else:  # If playing against friend
                if keys[pygame.K_w] and opponent.top > 0:  # If W is pressed and paddle is not at top
                    opponent.top -= 4  # Move opponent paddle up
                if keys[pygame.K_s] and opponent.bottom < HEIGHT:  # If S is pressed and paddle is not at bottom
                    opponent.bottom += 4  # Move opponent paddle down

            ball.x += x_speed * 6  # Move ball horizontally
            ball.y += y_speed * 6  # Move ball vertically

            if ball.top <= 0 or ball.bottom >= HEIGHT:  # If ball hits top or bottom
                y_speed *= -1  # Reverse vertical direction

            if ball.left <= 0:  # If ball goes past left edge
                player_score += 1  # Increase player score
                coins += 1  # Increase coins
                ball, x_speed, y_speed = reset_ball()  # Reset ball

            if ball.right >= WIDTH:  # If ball goes past right edge
                opponent_score += 1  # Increase opponent score
                ball, x_speed, y_speed = reset_ball()  # Reset ball
                pygame.time.delay(500)  # Wait half a second

            if ball.colliderect(player) or ball.colliderect(opponent):  # If ball hits a paddle
                sound_manager.play_hit()  # Play hit sound
                x_speed *= -1  # Reverse horizontal direction

            draw_game(player, opponent, ball, player_score, opponent_score, coins, player_paddle_color)  # Draw the game

        pygame.display.update()  # Update the display
        CLOCK.tick(60)  # Limit the frame rate to 60 FPS

main()  # Start the game