import pygame


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
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("#FFFFFF")
        screen.blit(connections_text, connections_text.get_rect(topleft=(32, 32)))
        screen.blit(description_text, description_text.get_rect(topleft=(32, 120)))
        pygame.draw.line(screen, "#000000", (0, 100), (screen.get_width(), 100))
        grid.draw(
            screen,
            screen_mid_x - (grid.size[0] // 2),
            screen_mid_y - (grid.size[1] // 2),
        )
        pygame.display.flip()

    pygame.quit()


class Tile:
    def __init__(self) -> None:
        self.box_size = 96
        self.text = "TEXT"
        # color picked to match NYT connections
        self.tile_color = "#EEEEE6"

    def draw(self, surface, x: int, y: int) -> None:
        pygame.draw.rect(
            surface,
            self.tile_color,
            pygame.Rect(x, y, self.box_size, self.box_size),
            border_radius=6,
        )


class Grid:
    def __init__(self) -> None:
        self.tiles = [[Tile() for i in range(4)] for _ in range(4)]
        self.grid_spacing = 10
        self.size = (
            4 * (self.tiles[0][0].box_size + self.grid_spacing),
            4 * (self.tiles[0][0].box_size + self.grid_spacing),
        )

    def draw(self, surface, x, y):
        for row in range(0, 4):
            for column in range(0, 4):
                tile = self.tiles[row][column]
                tile.draw(
                    surface,
                    x + row * (tile.box_size + self.grid_spacing),
                    y + column * (tile.box_size + self.grid_spacing),
                )


if __name__ == "__main__":
    main()
