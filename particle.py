import pygame
import random
import math

class Particle:
    """
    Represents a single particle in the system.
    Each particle has position, velocity, and acceleration.
    It can be updated with forces and drawn on the screen.
    """
    def __init__(self, x, y, screen_width, screen_height):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1)  # Initial velocity
        self.vy = random.uniform(-1, 1)
        self.ax = 0  # Acceleration
        self.ay = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.radius = 2
        self.color = (255, 255, 255)  # White particle

    def apply_force(self, fx, fy):
        """Apply a force to the particle, affecting its acceleration."""
        self.ax += fx
        self.ay += fy

    def update(self):
        """Update the particle's position based on velocity and acceleration."""
        # Update velocity with acceleration
        self.vx += self.ax
        self.vy += self.ay

        # Limit velocity to prevent particles from moving too fast
        speed = math.sqrt(self.vx**2 + self.vy**2)
        max_speed = 2
        if speed > max_speed:
            self.vx = (self.vx / speed) * max_speed
            self.vy = (self.vy / speed) * max_speed

        # Update position
        self.x += self.vx
        self.y += self.vy

        # Reset acceleration
        self.ax = 0
        self.ay = 0

        # Wrap around screen edges
        if self.x < 0:
            self.x = self.screen_width
        elif self.x > self.screen_width:
            self.x = 0
        if self.y < 0:
            self.y = self.screen_height
        elif self.y > self.screen_height:
            self.y = 0

    def draw(self, screen):
        """Draw the particle as a circle on the screen."""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class ParticleSystem:
    """
    Manages a collection of particles.
    Handles updating, drawing, and interactions between particles.
    """
    def __init__(self, num_particles, screen_width, screen_height):
        self.particles = []
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.connection_distance = 100  # Max distance for drawing connections
        self.mouse_influence_distance = 150  # Distance for mouse interaction

        # Create particles at random positions
        for _ in range(num_particles):
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            self.particles.append(Particle(x, y, screen_width, screen_height))

    def apply_mouse_force(self, mouse_x, mouse_y):
        """Apply repulsive force from the mouse to nearby particles."""
        for particle in self.particles:
            dx = particle.x - mouse_x
            dy = particle.y - mouse_y
            distance = math.sqrt(dx**2 + dy**2)
            if distance < self.mouse_influence_distance and distance > 0:
                # Repel: force in the direction away from mouse
                force_strength = (self.mouse_influence_distance - distance) / self.mouse_influence_distance * 0.1
                fx = (dx / distance) * force_strength
                fy = (dy / distance) * force_strength
                particle.apply_force(fx, fy)

    def update(self):
        """Update all particles."""
        for particle in self.particles:
            # Add some random force for natural movement
            particle.apply_force(random.uniform(-0.01, 0.01), random.uniform(-0.01, 0.01))
            particle.update()

    def draw(self, screen):
        """Draw all particles and connections."""
        # Draw connections first (behind particles)
        for i, p1 in enumerate(self.particles):
            for p2 in self.particles[i+1:]:
                dx = p1.x - p2.x
                dy = p1.y - p2.y
                distance = math.sqrt(dx**2 + dy**2)
                if distance < self.connection_distance:
                    # Opacity based on distance
                    alpha = int((1 - distance / self.connection_distance) * 255)
                    color = (255, 255, 255, alpha)
                    pygame.draw.line(screen, color, (int(p1.x), int(p1.y)), (int(p2.x), int(p2.y)), 1)

        # Draw particles
        for particle in self.particles:
            particle.draw(screen)