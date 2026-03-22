import pygame
import sys
from particle import ParticleSystem

def main():
    """
    Main function to run the interactive particle wallpaper.
    Initializes Pygame, sets up the window, and runs the animation loop.
    """
    pygame.init()

    # Set up the display (will be resized by Lively, but start with a default size)
    screen_width = 1920
    screen_height = 1080
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Interactive Particle Wallpaper")

    # Create the particle system
    num_particles = 100  # Adjust for performance
    particle_system = ParticleSystem(num_particles, screen_width, screen_height)

    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(60) / 1000.0  # Delta time for smooth animation

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                # Update screen size when resized
                screen_width = event.w
                screen_height = event.h
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
                # Update particle system with new dimensions
                particle_system.screen_width = screen_width
                particle_system.screen_height = screen_height
                for particle in particle_system.particles:
                    particle.screen_width = screen_width
                    particle.screen_height = screen_height

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Clear the screen with a dark background
        screen.fill((0, 0, 0))

        # Apply mouse forces
        particle_system.apply_mouse_force(mouse_x, mouse_y)

        # Update particles
        particle_system.update()

        # Draw everything
        particle_system.draw(screen)

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()