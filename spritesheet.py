import pygame

class SpriteSheet():
    def __init__(self, image_path, frame_count, frame_width, frame_height, scale, color):
        self.sheet =  pygame.image.load(image_path).convert_alpha()
        self.frame_count = frame_count
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.scale = scale
        self.color = color
        self.frames = self.load_frames()
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 100

    def load_frames(self):
        frames = []
        for frame_num in range(self.frame_count):
            frame = pygame.Surface((self.frame_width, self.frame_height)).convert_alpha()
            frame.blit(self.sheet, (0, 0), (frame_num * self.frame_width, 0, self.frame_width, self.frame_height))
            frame = pygame.transform.scale(frame, (self.frame_width * self.scale, self.frame_height * self.scale))
            frame.set_colorkey(self.color)
            frames.append(frame)
        return frames

    def get_frame(self):
        now = pygame.time.get_ticks()
        if now - self.last_update >= self.animation_cooldown:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
        return self.frames[self.current_frame]
    
    def get_base_image(self):
        return self.frames[0]
