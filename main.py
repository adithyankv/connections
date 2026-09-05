import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    running = True

    screen_mid_x = screen.get_width() // 2
    screen_mid_y = screen.get_height() // 2

    box_size = 96
    box_spacing = 10
    print(screen_mid_x, screen_mid_y)

    font = pygame.font.SysFont("NYTKarnakCondensed", 64)
    connections_text = font.render("Shannections", True, "#000000")

    description_font = pygame.font.SysFont(None, 22)
    description_text = description_font.render(
        "Create four groups of four", True, "#999999"
    )
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("#FFFFFF")
        screen.blit(connections_text, connections_text.get_rect(topleft=(32, 32)))
        screen.blit(description_text, description_text.get_rect(topleft=(32, 120)))
        pygame.draw.line(screen, "#000000", (0, 100), (screen.get_width(), 100))
        for row in range(-2, 2):
            for column in range(-2, 2):
                pygame.draw.circle(screen, "#FF0000", (screen_mid_x, screen_mid_y), 2)
                pygame.draw.rect(
                    screen,
                    "#EEEEE6",
                    pygame.Rect(
                        screen_mid_x + row * (box_size + box_spacing),
                        screen_mid_y + column * (box_size + box_spacing),
                        box_size,
                        box_size,
                    ),
                    border_radius=6,
                )
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
