import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 300
FPS = 600
FRAME_TIME = 150  # Time in milliseconds for each frame
SPACING = 10  # Spacing between sprites

# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Fish!')
clock = pygame.time.Clock()

# Load the sprite sheet
sprite_sheet_image = pygame.image.load('sprites.png').convert_alpha()
sprite_size = [48, 48]  # Size of each sprite frame (width, height)
offset_x = 0
offset_y = 0
# Extract frames for multiple sprites
sprites = []
number_sprites = 4  # Number of different sprites
number_rows = 8
frames_per_sprite = 3  # Number of frames per sprite

sprite_colors = {}
sprite_color_intensities = {}

def apply_tint(sprite, tint, intensity=128):
    """
    Apply a purple tint to a sprite.
    :param sprite: Pygame surface to tint.
    :param intensity: Intensity of the tint, 0 to 255.
    :return: A new surface with the tint applied.
    """
    # Create a purple surface
    tint_surface = pygame.Surface(sprite.get_size())
    tint_surface.fill(tint)  # RGB for purple

    # Set the alpha value to control the intensity of the tint
    tint_surface.set_alpha(intensity)

    # Create a copy of the original sprite to preserve it
    tinted_sprite = sprite.copy()

    # Blend the purple surface with the sprite
    tinted_sprite.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    return tinted_sprite

def extract_sprites():
    global sprites
    sprites = []
    for row in range(number_rows):
        for column in range(number_sprites):
            frames = []
            for frame in range(frames_per_sprite):
                try:
                    # Calculate x by taking the current column and adding the frame index within that sprite
                    x = offset_x + (column * frames_per_sprite + frame) * sprite_size[0]
                    # Calculate y by just using the row index, no need to add the frame index
                    y = offset_y + row * sprite_size[1]
                    # Create the subsurface for the frame
                    frame = sprite_sheet_image.subsurface(pygame.Rect(x, y, sprite_size[0], sprite_size[1]))
                    frames.append(frame)
                except ValueError as e:
                    print(f"Error extracting sprite at row {row}, column {column}, frame {frame}: {e}")
            sprites.append(frames)

def refresh_tints():
    for i, sprite in enumerate(sprites):
        sprite_colors[i] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        sprite_color_intensities[i] = random.randint(0, 255)



extract_sprites()  # Initial extraction

# Animation control
current_frame = 0
last_update = pygame.time.get_ticks()

# Game loop
running = True
while running:
    # print(f'{offset_x}, {offset_y}, {sprite_size[0]}, {sprite_size[1]}')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                sprite_size[1] += 1  # Increase height
                extract_sprites()
            elif event.key == pygame.K_DOWN:
                sprite_size[1] = max(1, sprite_size[1] - 1)  # Decrease height
                extract_sprites()
            elif event.key == pygame.K_RIGHT:
                sprite_size[0] += 1  # Increase width
                extract_sprites()
            elif event.key == pygame.K_LEFT:
                sprite_size[0] = max(1, sprite_size[0] - 1)  # Decrease width
                extract_sprites()
            elif event.key == pygame.K_a:
                offset_x -= 1
                print(f"Decreasing offset_x, new value: {offset_x}")
                extract_sprites()
            elif event.key == pygame.K_d:
                offset_x += 1
                print(f"Increasing offset_x, new value: {offset_x}")
                extract_sprites()
            elif event.key == pygame.K_w:
                offset_y -= 1
                print(f"Decreasing offset_y, new value: {offset_y}")
                extract_sprites()
            elif event.key == pygame.K_s:
                offset_y += 1
                print(f"Increasing offset_y, new value: {offset_y}")
                extract_sprites()
            elif event.key == pygame.K_r:
                offset_y += 1
                refresh_tints()


    # Update frame
    now = pygame.time.get_ticks()
    if now - last_update > FRAME_TIME:
        last_update = now
        current_frame = (current_frame + 1) % frames_per_sprite

    # Constants for grid layout
    number_display_rows = 4  # Adjust as needed
    number_display_sprites = len(sprites) // number_display_rows  # Assuming sprites list is evenly divisible by number_display_rows

    # Draw frames
    screen.fill((255, 255, 255))
    total_width = number_display_sprites * sprite_size[0] + (number_display_sprites - 1) * SPACING
    total_height = number_display_rows * sprite_size[1] + (number_display_rows - 1) * SPACING
    start_x = SCREEN_WIDTH // 2 - total_width // 2
    start_y = SCREEN_HEIGHT // 2 - total_height // 2

    try:
        for i, sprite_frames in enumerate(sprites):
            sprite_frame = sprite_frames[current_frame]
            if len(sprite_colors)-1 >= i:
                sprite_frame = apply_tint(sprite_frame, sprite_colors[i], intensity=sprite_color_intensities[i])
            column = i % number_display_sprites
            row = i // number_display_sprites
            position_x = start_x + column * (sprite_size[0] + SPACING)
            position_y = start_y + row * (sprite_size[1] + SPACING)
            screen.blit(sprite_frame, (position_x, position_y))
    except IndexError as e:
        print(f"Error drawing sprite at index {i}: {e}")

    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()
sys.exit()
