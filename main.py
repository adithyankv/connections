import pygame
import random


def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    running = True

    screen_mid_x = screen.get_width() // 2
    screen_mid_y = screen.get_height() // 2

    font = pygame.font.SysFont("NYTKarnakCondensed", 64)
    connections_text = font.render("Shannections", True, "#000000")

    description_font = pygame.font.SysFont(None, 22)
    description_text = description_font.render(
        "Create four groups of four", True, "#999999"
    )
    grid = Grid()
    shuffle_button = Button("Shuffle")
    deselect_button = Button("Deselect All")
    submit_button = Button("Submit")

    buttons = [shuffle_button, deselect_button, submit_button]

    def shuffle_tiles():
        random.shuffle(grid.tiles)

    def deselect_all():
        for tile in grid.tiles:
            tile.selected = False

    def submit():
        submitted_tiles = [tile.text for tile in grid.tiles if tile.selected]
        if len(submitted_tiles) == 4:
            print(f"submitted {submitted_tiles}")

    shuffle_button.connect(shuffle_tiles)
    deselect_button.connect(deselect_all)
    submit_button.connect(submit)

    while running:
        selected_tiles_count = 0
        for tile in grid.tiles:
            if tile.selected:
                selected_tiles_count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for tile in grid.tiles:
                    if tile.rect.collidepoint(pygame.mouse.get_pos()):
                        if not tile.selected and selected_tiles_count < 4:
                            tile.selected = True
                        elif tile.selected:
                            tile.selected = False
                for button in buttons:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        button.callback()

        for tile in grid.tiles:
            tile.hovered = tile.rect.collidepoint(pygame.mouse.get_pos())
        for button in buttons:
            button.hovered = button.rect.collidepoint(pygame.mouse.get_pos())

        screen.fill("#FFFFFF")
        screen.blit(connections_text, connections_text.get_rect(topleft=(32, 32)))
        screen.blit(description_text, description_text.get_rect(topleft=(32, 120)))
        pygame.draw.line(screen, "#000000", (0, 100), (screen.get_width(), 100))
        grid.draw(
            screen,
            screen_mid_x - (grid.size[0] // 2),
            screen_mid_y - (grid.size[1] // 2),
        )
        shuffle_button.draw(screen, 400, 600)
        deselect_button.draw(screen, 600, 600)
        submit_button.draw(screen, 800, 600)

        pygame.display.flip()

    pygame.quit()


class Tile:
    def __init__(self, text) -> None:
        self.box_size = 96
        self.text = text
        # color picked to match NYT connections
        self.hovered_color = "#DDDDD6"
        self.base_color = "#EEEEE6"
        self.selected_color = "#5A584E"

        self.color = self.base_color
        self.rect = pygame.Rect()
        self.selected = False
        self.hovered = False
        self.callback = None

    def draw(self, surface, x: int, y: int) -> None:
        self.rect = pygame.Rect(x, y, self.box_size, self.box_size)
        if self.hovered and not self.selected:
            self.color = self.hovered_color
        elif self.selected:
            self.color = self.selected_color
        else:
            self.color = self.base_color

        pygame.draw.rect(
            surface,
            self.color,
            self.rect,
            border_radius=6,
        )

        font = pygame.font.SysFont(None, 20)
        text_color = "#FFFFFF" if self.selected else "#000000"
        self.text_surface = font.render(self.text, True, text_color)
        text_width, text_height = (
            self.text_surface.get_width(),
            self.text_surface.get_height(),
        )
        surface.blit(
            self.text_surface,
            (
                x + (self.box_size - text_width) // 2,
                y + (self.box_size - text_height) // 2,
            ),
        )


class Button:
    def __init__(self, text) -> None:
        self.text = text
        self.height = 40
        self.width = 120
        self.rect = pygame.Rect()
        self.hovered = False
        self.dark = "#000000"
        self.light = "#FFFFFF"
        self.color = self.dark

    def draw(self, surface, x, y):
        self.rect = pygame.Rect(x, y, self.width, self.height)
        font = pygame.font.SysFont(None, 20)
        text_color = self.light if self.hovered else self.dark
        pygame.draw.rect(
            surface,
            self.color,
            self.rect,
            border_radius=20,
            width=0 if self.hovered else 2,
        )
        text = font.render(self.text, True, text_color)
        surface.blit(
            text,
            (
                x + (self.width - text.get_width()) // 2,
                y + (self.height - text.get_height()) // 2,
            ),
        )

    def connect(self, callback: callable):
        self.callback = callback


class Grid:
    def __init__(self) -> None:
        self.tiles = [Tile(f"TEXT {i}") for i in range(16)]
        self.grid_spacing = 10
        self.size = (
            4 * (self.tiles[0].box_size + self.grid_spacing),
            4 * (self.tiles[0].box_size + self.grid_spacing),
        )

    def draw(self, surface, x, y):
        for row in range(0, 4):
            for column in range(0, 4):
                tile = self.tiles[row * 4 + column]
                tile.draw(
                    surface,
                    x + row * (tile.box_size + self.grid_spacing),
                    y + column * (tile.box_size + self.grid_spacing),
                )


if __name__ == "__main__":
    main()
