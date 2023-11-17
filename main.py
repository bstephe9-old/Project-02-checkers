#main file for the project
#main will contain the main game logic
#main will call the other files and classes to run the game

import pygame
from SecondMenu import SecondMenu
from Main_Board import MAIN_Board
from constants import BLACK, WHITE
import time
import string


# import menu currently disabled

pygame.init()
pygame.mixer.init() # initialize pygame mixer for music

# set up the drawing window
Width, Height = 1000, 700 # updated size
screen = pygame.display.set_mode([Width, Height])

#title of the game for screen 
pygame.display.set_caption("Checkers+")

# background music
tracks = ["music/Track1.mp3", "music/Track2.mp3", "music/Track3.mp3", "music/Track4.mp3"] # can add more or delete tracks if we do not like them
current_track = 0
SONG_END = pygame.USEREVENT + 1
def music_loop():
    global current_track
    pygame.mixer.music.load(tracks[current_track])
    pygame.mixer.music.set_volume(0.1) # 0.1-1.0, can change accordingly
    pygame.mixer.music.play()
    current_track = (current_track + 1) % len(tracks)

music_loop()
pygame.mixer.music.set_endevent(SONG_END) # create event for song ending/looping
music_playing = True # boolean to check if music is playing or not

# for board customization, use class when creating game
class Board:
    def __init__(self, color1, color2, boardColor):
        self.color1 = color1
        self.color2 = color2
        self.boardColor = boardColor

board = Board("red", "black", "white")

# title for display (can remove credits if we do not want them)
game_title = "Checkers+"
message = "Checkers with a twist! For all ages and skill levels!"
credits1 = "Developed by Wander Cerda-Torres, Barry Lin,"
credits2 = "Nathan McCourt, Jonathan Stanczak, and Geonhee Yu"

background_image = pygame.image.load("checkers.jpg")
background_image = pygame.transform.scale(background_image, (Width, Height))  

title_font = pygame.font.Font(None, 64)
message_font = pygame.font.Font(None, 32)
credits_font = pygame.font.Font(None, 25)

# Title text
title_text = title_font.render(game_title, True, (255, 255, 255))
title_rect = title_text.get_rect(center=(Width // 2, 22))

# Under title text
message_text = message_font.render(message, True, (255, 255, 255))
message_rect = message_text.get_rect(center=(Width // 2, 55))

# Credits text
credits_text1 = credits_font.render(credits1, True, (255, 255, 255))
credits_rect1 = credits_text1.get_rect(center=(Width // 2, 650))
credits_text2 = credits_font.render(credits2, True, (255, 255, 255))
credits_rect2 = credits_text2.get_rect(center=(Width // 2, 670))

# Function to draw the text input box on the screen
def draw_text_input(player_name, error_msg="name error"):
    font = pygame.font.Font(None, 32)

    # Render the background box
    pygame.draw.rect(screen, (128, 128, 128), (Width // 2 - 225, Height // 2 - 25, 450, 50))  # Adjust size and position as needed

    # Render the text on the background box
    input_text = font.render("Enter Your Name: " + player_name, True, (255, 255, 255))
    input_rect = input_text.get_rect(center=(Width // 2, Height // 2))
    screen.blit(input_text, input_rect)

    # Render the error message below the input box
    if error_msg:
        error_font = pygame.font.Font(None, 24)
        error_text = error_font.render(error_msg, True, (255, 0, 0))  # Red color for error message
        error_rect = error_text.get_rect(center=(Width // 2, Height // 2 + 30))  # Adjust position as needed
        screen.blit(error_text, error_rect)


# Function to ask player's name
def get_player_name():
    input_active = True
    player_name = ""
    error_msg = ""

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    #if player_name.isalnum() and len(player_name) <= 20:
                    if (event.unicode.isalnum() or event.unicode.isspace()) and len(player_name) < 20:

                        input_active = False  # Stop taking input when Enter is pressed and the name is valid
                    else:
                        error_msg = "Invalid name. Please use English letters or numbers, and keep it under 20 characters."
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]  # Remove the last character when Backspace is pressed
                else:
                    # Check if the typed character is an English letter, a number, or a space
                    if (event.unicode.isalnum() or event.unicode.isspace()) and len(player_name) < 20:
                        player_name += event.unicode  # Append the typed character to the player_name



        screen.blit(background_image, (0, 0))
        draw_text_input(player_name, error_msg)
        pygame.display.flip()

    return player_name



# run until the user closes application
def main():

    # Get the player's name
    player_name = get_player_name()
    
    second_menu_instance = SecondMenu()

    # Display the player's name at the right bottom corner
    player_name_font = pygame.font.Font(None, 24)
    player_name_text = player_name_font.render(player_name, True, (255, 255, 255))  # White text color
    player_name_rect = player_name_text.get_rect(bottomright=(Width - 10, Height - 10))  # Adjust position as needed

    running = True
    while running:
        # did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                buttons = menu_buttons() # create array for buttons # NEED TO ADD PVC BUTTON OR MAKE PVP BUTTON COMBINED INTO BOTH
                if buttons[0].collidepoint(event.pos): # If Start Game button is clicked, show the second menu
                   second_menu_instance.start_game_menu()
                if buttons[2].collidepoint(event.pos): # if mouse is clicked on tutorial button
                    tutorial()
                elif buttons[1].collidepoint(event.pos): # if mouse is clicked on settings button
                    settings()
                # elif buttons[3].collidepoint(event.pos): # if mouse is clicked on leaderboard button (not yet implemented)
                    # code to enter leaderboard menu
                # Check if the current song has finished, loop to next song
            elif event.type == SONG_END:
                music_loop()

        #image of the background
        screen.blit(background_image, (0, 0))

        # display title information and credits
        screen.blit(title_text, title_rect)
        screen.blit(message_text, message_rect)
        screen.blit(credits_text1, credits_rect1)
        screen.blit(credits_text2, credits_rect2)
        
        # call PvP button function from menu.py
        menu_buttons()


        # Display player name in the right bottom corner
        pygame.draw.rect(screen, (0, 0, 255), player_name_rect)  # Blue box
        screen.blit(player_name_text, player_name_rect)


        # flip the display
        pygame.display.flip()

    # done! time to quit
    pygame.quit()

def menu_buttons(): # function to create menu buttons

    # Used for buttons w/ images
    icon_size = (45, 45)  # Adjust the size of the icon as needed
    button_height = 50
    spacing = 10

    # Start Game Button
    startgame_icon = pygame.image.load('pics/start_icon.png')
    # Draw the icon next to the text with the specified size
    startgame_icon_resized = pygame.transform.scale(startgame_icon, icon_size)
    startgame_icon_rect = startgame_icon_resized.get_rect(topleft=(Width // 2 - 150 + 10, Height // 3 + (button_height - icon_size[1] - 50) // 2))

    color = (128, 128, 128) # grey
    cursor_color = (100, 100, 100) # darker grey
    position = (Width // 2-150, Height // 3-25)
    size = (300, 50)  # width, height
        
    button_font = pygame.font.Font(None, 32)
    button_text = button_font.render("Start Game", True, (255, 255, 255)) # Button text and color
    button_text_rect = button_text.get_rect(center=(Width // 2, Height // 3))
    
    # Create button on screen using position and size parameters
    pygame.draw.rect(screen, color, pygame.Rect(position, size))
    screen.blit(startgame_icon_resized, startgame_icon_rect.topleft)
    screen.blit(button_text, button_text_rect)
    
    # Used to indicate if cursor is hovering over button. If so, button will be darker
    mouse = pygame.mouse.get_pos()
    button_rect = pygame.Rect(position, size)
    if button_rect.collidepoint(mouse):
        pygame.draw.rect(screen, cursor_color, button_rect)  # Change color when cursor hovered over
    else:
        pygame.draw.rect(screen, color, button_rect) # stay original color if cursor not hovering over

    screen.blit(button_text, button_text_rect)
    screen.blit(startgame_icon_resized, startgame_icon_rect.topleft)  # Draw the icon after drawing the button

    # Settings Button    
    settings_icon = pygame.image.load('pics/settings_icon.png')

    position = (Width // 2 - 150, Height // 3 + button_height + spacing)
    size = (300, button_height)  # width, height

    button_text = button_font.render("Settings", True, (255, 255, 255))  # Button text and color
    button_text_rect = button_text.get_rect(center=(Width // 2, Height // 3 + button_height + spacing + button_height // 2))

    # Draw the icon next to the text with the specified size
    settings_icon_resized = pygame.transform.scale(settings_icon, icon_size)
    settings_icon_rect = settings_icon_resized.get_rect(topleft=(Width // 2 - 150 + 10, Height // 3 + button_height + spacing + (button_height - icon_size[1]) // 2))

    # Create button on screen using position and size parameters
    pygame.draw.rect(screen, color, pygame.Rect(position, size))
    screen.blit(settings_icon_resized, settings_icon_rect.topleft)  # Draw the icon after drawing the button
    screen.blit(button_text, button_text_rect)

    # Used to indicate if the cursor is hovering over the button. If so, the button will be darker
    mouse = pygame.mouse.get_pos()
    button_rect_2 = pygame.Rect(position, size)
    if button_rect_2.collidepoint(mouse):
        pygame.draw.rect(screen, cursor_color, button_rect_2)  # Change color when cursor hovered over
    else:
        pygame.draw.rect(screen, color, button_rect_2)  # Stay the original color if the cursor is not hovering over

    screen.blit(settings_icon_resized, settings_icon_rect.topleft)  # Draw the icon after drawing the button
    screen.blit(button_text, button_text_rect)

    # Tutorial button
    tutorial_icon = pygame.image.load('pics/tutorial_icon.png')

    color = (128, 128, 128) # grey
    cursor_color = (100, 100, 100) # darker grey
    position = (Width // 2-150, Height // 3 + 135)
    size = (300, 50)  # width, height

    button_font = pygame.font.Font(None, 32)
    button_text = button_font.render("Tutorial", True, (255, 255, 255)) # Button text and color
    button_text_rect = button_text.get_rect(center=(Width // 2, Height // 3+160))
    pygame.draw.rect(screen, color, pygame.Rect(position, size))
    screen.blit(button_text, button_text_rect)

    # Draw the icon next to the text with the specified size
    tutorial_icon_resized = pygame.transform.scale(tutorial_icon, icon_size)
    tutorial_icon_rect = tutorial_icon_resized.get_rect(topleft=(Width // 2 - 150 + 10, Height // 3 + 135 + (button_height - icon_size[1]) // 2))

    pygame.draw.rect(screen, color, pygame.Rect(position, size))
    screen.blit(button_text, button_text_rect)
    
    # Used to indicate if cursor is hovering over button. If so, button will be darker
    mouse = pygame.mouse.get_pos()
    button_rect_3 = pygame.Rect(position, size)
    if button_rect_3.collidepoint(mouse):
        pygame.draw.rect(screen, cursor_color, button_rect_3)  # Change color when cursor hovered over
    else:
        pygame.draw.rect(screen, color, button_rect_3) # stay original color if cursor not hovering over

    screen.blit(tutorial_icon_resized, tutorial_icon_rect.topleft)  # Draw the icon after drawing the button
    screen.blit(button_text, button_text_rect)
    
    # Leaderboard button
    leaderboard_icon = pygame.image.load('pics/leaderboard_icon.png')

    color = (128, 128, 128) # grey
    cursor_color = (100, 100, 100) # darker grey
    position = (Width // 2 - 150, Height // 3 + 200)  # Adjust the vertical position as needed
    size = (300, 50)  # width, height

    button_font = pygame.font.Font(None, 32)
    button_text = button_font.render("View Rankings", True, (255, 255, 255)) # Button text and color
    button_text_rect = button_text.get_rect(center=(Width // 2, Height // 3 + 225))  # Adjust the vertical position as needed
    pygame.draw.rect(screen, color, pygame.Rect(position, size))
    screen.blit(button_text, button_text_rect)

    # Draw the icon next to the text with the specified size
    leaderboard_icon_resized = pygame.transform.scale(leaderboard_icon, icon_size)
    leaderboard_icon_rect = leaderboard_icon_resized.get_rect(
        topleft=(Width // 2 - 150 + 10, Height // 3 + 200 + (button_height - icon_size[1]) // 2))

    pygame.draw.rect(screen, color, pygame.Rect(position, size))
    screen.blit(button_text, button_text_rect)
    
    # Used to indicate if cursor is hovering over button. If so, button will be darker
    mouse = pygame.mouse.get_pos()
    button_rect_4 = pygame.Rect(position, size)
    if button_rect_4.collidepoint(mouse):
        pygame.draw.rect(screen, cursor_color, button_rect_4)  # Change color when cursor hovered over
        if pygame.mouse.get_pressed()[0]:  # Check if left mouse button is clicked
            show_leaderboard()  # Call the function to display the leaderboard
    else:
        pygame.draw.rect(screen, color, button_rect_4) # stay original color if cursor not hovering over

    screen.blit(leaderboard_icon_resized, leaderboard_icon_rect.topleft)  # Draw the icon after drawing the button
    screen.blit(button_text, button_text_rect)

    return button_rect, button_rect_2, button_rect_3, button_rect_4

def tutorial(): # tutorial prompt (subject to change text)
    # load image used in tutorial
    checkers_icon = pygame.image.load('pics/checkersguy_icon.png')
    tutorial_screen = pygame.display.set_mode([Width, Height])
    tutorial_screen.fill((128, 128, 128))

    # First message
    tutorial_font = pygame.font.Font(None, 64)
    tutorial_text = tutorial_font.render("Welcome to Checkers+!", True, (255, 255, 255))
    tutorial_rect = tutorial_text.get_rect(center=(Width // 2, 50))
    tutorial_screen.blit(tutorial_text, tutorial_rect)

    # Second message
    tutorial_font = pygame.font.Font(None, 32)
    tutorial_text = tutorial_font.render("This tutorial should provide you with instructions on how to play and use Checkers+.", True, (255, 255, 255))
    tutorial_rect = tutorial_text.get_rect(center=(Width // 2, 105))
    tutorial_screen.blit(tutorial_text, tutorial_rect)

    # First paragraph
    tutorial_font = pygame.font.Font(None, 25)
    tutorial_text = tutorial_font.render("There are many features accessible from the Checkers+ main menu. You can start a PvP (player versus player) game,", True, (255, 255, 255))
    tutorial_rect = tutorial_text.get_rect(center=(Width // 2, 145))
    tutorial_screen.blit(tutorial_text, tutorial_rect)
    tutorial_text = tutorial_font.render("a PvC (player versus computer) game, and access other features like the settings, leaderboard, and this tutorial!", True, (255, 255, 255))
    tutorial_rect = tutorial_text.get_rect(center=(Width // 2, 170))
    tutorial_screen.blit(tutorial_text, tutorial_rect)
    tutorial_text = tutorial_font.render("The settings will allow you to turn music on or off, and customize the checkers board to your liking.", True, (255, 255, 255))
    tutorial_rect = tutorial_text.get_rect(center=(Width // 2, 195))
    tutorial_screen.blit(tutorial_text, tutorial_rect)
    tutorial_text = tutorial_font.render("The leaderboard will show recent match results, displaying who won and loss. These will reset when you quit the app.", True, (255, 255, 255))
    tutorial_rect = tutorial_text.get_rect(center=(Width // 2, 220))
    tutorial_screen.blit(tutorial_text, tutorial_rect)

    # Create icon
    icon_size = (100, 100)
    button_height = 50
    spacing = 10
    checkers_icon_resized = pygame.transform.scale(checkers_icon, icon_size)
    checkers_icon_rect = checkers_icon_resized.get_rect(topleft=(Width // 2 - 150 + 95, Height // 3 + 30 + (button_height - icon_size[1]) // 2))
    screen.blit(checkers_icon_resized, checkers_icon_rect.topleft) 

    # Second paragraph
    tutorial_text = tutorial_font.render("To play Checkers+, standard checkers rules are applied...with a twist!", True, (255, 255, 255))
    tutorial_rect = tutorial_text.get_rect(center=(Width // 2, 365))
    tutorial_screen.blit(tutorial_text, tutorial_rect)
    tutorial_text = tutorial_font.render("In standard checkers, players can only move a piece diagonally until that piece has reached the last row", True, (255, 255, 255))
    tutorial_rect = tutorial_text.get_rect(center=(Width // 2, 390))
    tutorial_screen.blit(tutorial_text, tutorial_rect)
    tutorial_text = tutorial_font.render("of the opposing side. In our game, you will be allowed to move a piece backwards every 45 seconds, even", True, (255, 255, 255))
    tutorial_rect = tutorial_text.get_rect(center=(Width // 2, 415))
    tutorial_screen.blit(tutorial_text, tutorial_rect)
    tutorial_text = tutorial_font.render("if that piece has not yet reached the last row. You also only have 15 seconds to make a move, so think fast!", True, (255, 255, 255))
    tutorial_rect = tutorial_text.get_rect(center=(Width // 2, 440))
    tutorial_screen.blit(tutorial_text, tutorial_rect)
    tutorial_text = tutorial_font.render("Your 45 second timer will not reset until you make a backward move. Don't let them go to waste!", True, (255, 255, 255))
    tutorial_rect = tutorial_text.get_rect(center=(Width // 2, 465))
    tutorial_screen.blit(tutorial_text, tutorial_rect)
    tutorial_text = tutorial_font.render("When the game starts, you will be asked to enter the names of the players (or player, if playing against the computer).", True, (255, 255, 255))
    tutorial_rect = tutorial_text.get_rect(center=(Width // 2, 490))
    tutorial_screen.blit(tutorial_text, tutorial_rect)
    tutorial_text = tutorial_font.render("Doing this will allow your name(s) and outcome to be shown on the leaderboard.", True, (255, 255, 255))
    tutorial_rect = tutorial_text.get_rect(center=(Width // 2, 515))
    tutorial_screen.blit(tutorial_text, tutorial_rect)
    tutorial_text = tutorial_font.render("By now, you should have a basic understanding of what Checkers+ has to offer. Go give it a try!", True, (255, 255, 255))
    tutorial_rect = tutorial_text.get_rect(center=(Width // 2, 540))
    tutorial_screen.blit(tutorial_text, tutorial_rect)
    tutorial_text = tutorial_font.render("If you ever need to view this tutorial again, you can access it from the main menu. Have fun!", True, (255, 255, 255))
    tutorial_rect = tutorial_text.get_rect(center=(Width // 2, 565))
    tutorial_screen.blit(tutorial_text, tutorial_rect)

    # Exit button to return back to menu
    exit_button_font = pygame.font.Font(None, 32)
    exit_button_text = exit_button_font.render("Exit Tutorial", True, (255, 255, 255))
    exit_button_rect = exit_button_text.get_rect(center=(Width // 2, Height - 50))
    pygame.draw.rect(tutorial_screen, (64, 64, 64), exit_button_rect.inflate(20, 10))
    tutorial_screen.blit(exit_button_text, exit_button_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button_rect.collidepoint(event.pos):  # if exit tutorial button is clicked
                    return  # exit tutorial and return to menu
                
def settings(): # settings menu

    # Used for buttons w/ images
    icon_size = (45, 45)  # Adjust the size of the icon as needed
    button_height = 50
    spacing = 10

    settings_screen = pygame.display.set_mode([Width, Height])
    screen.blit(background_image, (0, 0))
    settings_screen.blit(title_text, title_rect)
    settings_screen.blit(message_text, message_rect)
    settings_screen.blit(credits_text1, credits_rect1)
    settings_screen.blit(credits_text2, credits_rect2)

    # Customize Board Button
    colorwheel_icon = pygame.image.load('pics/colorwheel_icon.png')
    # Draw the icon next to the text with the specified size
    colorwheel_icon_resized = pygame.transform.scale(colorwheel_icon, icon_size)
    colorwheel_icon_rect = colorwheel_icon_resized.get_rect(topleft=(Width // 2 - 155 + 10, Height // 3 + (button_height - icon_size[1] - 50) // 2))

    color = (128, 128, 128) # grey
    cursor_color = (100, 100, 100) # darker grey
    position = (Width // 2-150, Height // 3-25)
    size = (300, 50)  # width, height
        
    button_font = pygame.font.Font(None, 32)
    button_text = button_font.render("Customize Board", True, (255, 255, 255)) # Button text and color
    button_text_rect = button_text.get_rect(center=(Width // 2, Height // 3))
    
    # Create button on screen using position and size parameters
    pygame.draw.rect(settings_screen, color, pygame.Rect(position, size))
    settings_screen.blit(colorwheel_icon_resized, colorwheel_icon_rect.topleft)
    settings_screen.blit(button_text, button_text_rect)
    
    button_rect_4 = pygame.Rect(position, size)

    # Music Button
    music_icon = pygame.image.load('pics/music_icon.png')
    position = (Width // 2 - 150, Height // 3 + button_height + spacing)
    size = (300, button_height)  # width, height

    button_text = button_font.render("Music (On/Off)", True, (255, 255, 255))  # Button text and color
    button_text_rect = button_text.get_rect(center=(Width // 2, Height // 3 + button_height + spacing + button_height // 2))

    # Draw the icon next to the text with the specified size
    music_icon_resized = pygame.transform.scale(music_icon, icon_size)
    music_icon_rect = music_icon_resized.get_rect(topleft=(Width // 2 - 150 + 10, Height // 3 + button_height + spacing + (button_height - icon_size[1]) // 2))

    # Create button on screen using position and size parameters
    pygame.draw.rect(settings_screen, color, pygame.Rect(position, size))
    settings_screen.blit(music_icon_resized, music_icon_rect.topleft)  # Draw the icon after drawing the button
    settings_screen.blit(button_text, button_text_rect)

    button_rect_5 = pygame.Rect(position, size)

    # Exit button to return back to menu
    exit_button_font = pygame.font.Font(None, 32)
    exit_button_text = exit_button_font.render("Exit Settings", True, (255, 255, 255))
    exit_button_rect = exit_button_text.get_rect(center=(Width // 2, Height - 100))
    pygame.draw.rect(settings_screen, (128, 128, 128), exit_button_rect.inflate(20, 10))
    settings_screen.blit(exit_button_text, exit_button_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button_rect.collidepoint(event.pos):  # if exit settings button is clicked
                    return  # exit settings and return to menu
                if button_rect_5.collidepoint(event.pos):  # if music button is clicked
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()  # Stop the music
                        music_playing = False
                    else:
                        music_loop()  # Start the music from next song in tracklist
                        music_playing = True

def show_leaderboard():
    pygame.init()

    # Dummy data for the leaderboard (replace this with your actual data)
    leaderboard_data = [
        ("Player1", 150),
        ("Player2", 120),
        ("Player3", 100),
        ("Player4", 90),
        ("Player5", 80),
        ("Player6", 70),
        ("Player7", 60),
        ("Player8", 50),
        ("Player9", 40),
        ("Player10", 30)
    ]

    # Set up the new window for the leaderboard
    leaderboard_screen = pygame.display.set_mode((1000, 700))
    pygame.display.set_caption("Leaderboard")

    # Leaderboard header
    header_font = pygame.font.Font(None, 36)
    header_text = header_font.render("Leaderboard", True, (255, 255, 255))
    header_rect = header_text.get_rect(center=(500, 40))
    leaderboard_screen.blit(header_text, header_rect)

    # Display player scores
    score_font = pygame.font.Font(None, 28)
    vertical_position = 80  # Adjust the starting vertical position as needed

    for rank, (player_name, score) in enumerate(leaderboard_data, start=1):
        player_text = score_font.render(f"{rank}. {player_name}: {score}", True, (255, 255, 255))
        player_rect = player_text.get_rect(center=(500, vertical_position))
        leaderboard_screen.blit(player_text, player_rect)
        vertical_position += 30  # Adjust the vertical spacing as needed

    pygame.display.flip()

    # Exit button to return back to menu
    exit_button_font = pygame.font.Font(None, 32)
    exit_button_text = exit_button_font.render("Return to Main Menu", True, (255, 255, 255))
    exit_button_rect = exit_button_text.get_rect(center=(Width // 2, Height - 50))
    pygame.draw.rect(leaderboard_screen, (64, 64, 64), exit_button_rect.inflate(20, 10))
    leaderboard_screen.blit(exit_button_text, exit_button_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button_rect.collidepoint(event.pos):  # if exit tutorial button is clicked
                    return  # exit tutorial and return to menu

    
main()