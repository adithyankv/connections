import pygame
import random


def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    running = True

    word_groups = [
        WordGroup("_AP", ["CAP", "MAP", "LAP", "TAP"], "#A0C35A"),
        WordGroup("LETTER HOMOPHONES", ["BEE", "KAY", "JAY", "EYE"], "#BA81C5"),
        WordGroup("SHAPES", ["SQUARE", "TRIANGLE", "CIRCLE", "RECTANGLE"], "#F9DF6D"),
        WordGroup("COLORS", ["RED", "BLUE", "GREEN", "YELLOW"], "#B0C4EF"),
    ]
    game_state = GameState(word_groups)

    screen_mid_x = screen.get_width() // 2
    screen_mid_y = screen.get_height() // 2

    font = pygame.font.SysFont("NYTKarnakCondensed", 64)
    connections_text = font.render("Connections", True, "#000000")

    description_font = pygame.font.SysFont(None, 22)
    description_text = description_font.render(
        "Create four groups of four", True, "#999999"
    )
    grid = Grid(game_state)
    shuffle_button = Button("Shuffle")
    deselect_button = Button("Deselect All")
    submit_button = Button("Submit")

    buttons = [shuffle_button, deselect_button, submit_button]

    shuffle_button.connect(game_state.shuffle_words)
    deselect_button.connect(game_state.clear_selection)
    submit_button.connect(game_state.submit)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for tile in grid.tiles:
                    if tile.rect.collidepoint(pygame.mouse.get_pos()):
                        if (
                            tile.text not in game_state.selected_words
                            and game_state.num_selected_words() < 4
                        ):
                            game_state.selected_words.append(tile.text)
                        elif tile.text in game_state.selected_words:
                            game_state.selected_words.pop(
                                game_state.selected_words.index(tile.text)
                            )
                for button in buttons:
                    if not button.disabled:
                        if button.rect.collidepoint(pygame.mouse.get_pos()):
                            button.callback()

        for tile in grid.tiles:
            tile.hovered = tile.rect.collidepoint(pygame.mouse.get_pos())
        for button in buttons:
            button.hovered = button.rect.collidepoint(pygame.mouse.get_pos())

        deselect_button.disabled = game_state.num_selected_words() == 0
        submit_button.disabled = game_state.num_selected_words() < 4

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


class WordGroup:
    def __init__(self, name: str, words: list[str], color: str) -> None:
        self.name = name
        self.words = words
        self.color = color


class Tile:
    def __init__(self, text, size: int) -> None:
        self.box_size = size
        self.text = text
        # color picked to match NYT connections
        self.hovered_color = "#DDDDD6"
        self.base_color = "#EEEEE6"
        self.selected_color = "#5A584E"

        self.color = self.base_color
        self.rect = pygame.Rect()
        self.selected = False
        self.hovered = False

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


class GameState:
    def __init__(self, word_groups):
        self.unsolved_groups = word_groups
        self.solved_groups = []
        self.selected_words = []
        self.unsolved_words = []
        self.seed = random.random()

    def num_selected_words(self):
        return len(self.selected_words)

    def shuffle_words(self):
        self.seed += 1

    def get_all_unsolved_words(self):
        self.unsolved_words = []
        for group in self.unsolved_groups:
            for word in group.words:
                self.unsolved_words.append(word)
        # We rearrange the words to a random order. The seed is generated at
        # intialization of class randomly, so that we don't get same shuffles across
        # games. But we want the same shuffle across frames, unless explicitly shuffled.
        # So we keep shuffling with the same seed, until the seed is changed explicitly
        # by the player using the shuffle button
        random.Random(self.seed).shuffle(self.unsolved_words)
        return self.unsolved_words

    def clear_selection(self):
        self.selected_words = []

    def submit(self):
        if self.num_selected_words() == 4:
            print(f"submitted {self.selected_words}")
            for word_group in self.unsolved_groups:
                if set(self.selected_words) == set(word_group.words):
                    self.solved_groups.append(word_group)
                    self.unsolved_groups.pop(self.unsolved_groups.index(word_group))
                if (
                    len(set(self.selected_words).intersection(set(word_group.words)))
                    == 3
                ):
                    print("One away")
        self.clear_selection()


class SolvedGroup:
    def __init__(self, word_group: WordGroup, width: int, height: int) -> None:
        self.word_group = word_group
        self.width = width
        self.height = height
        self.spacing = 10

    def draw(self, surface, x, y):
        self.rect = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(surface, self.word_group.color, self.rect, border_radius=6)
        header_font = pygame.font.SysFont("freesansbold", 18)
        body_font = pygame.font.SysFont(None, 20)
        group_name = header_font.render(self.word_group.name, True, "#000000")
        words = body_font.render(",".join(self.word_group.words), True, "#000000")

        text_box_height = group_name.get_height() + words.get_height() + self.spacing
        surface.blit(
            group_name,
            (
                x + (self.width - group_name.get_width()) // 2,
                y + (self.height - text_box_height) // 2,
            ),
        )
        surface.blit(
            words,
            (
                x + (self.width - words.get_width()) // 2,
                y
                + (self.height - text_box_height) // 2
                + self.spacing
                + group_name.get_height(),
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
        self.disabled_color = "#999999"
        self.color = self.dark
        self.disabled = False

    def draw(self, surface, x, y):
        self.rect = pygame.Rect(x, y, self.width, self.height)
        font = pygame.font.SysFont(None, 20)
        if self.disabled:
            text_color = self.disabled_color
            self.color = self.disabled_color
        elif self.hovered:
            text_color = self.light
            self.color = self.dark
        else:
            text_color = self.dark
            self.color = self.dark
        pygame.draw.rect(
            surface,
            self.color,
            self.rect,
            border_radius=20,
            width=0 if (self.hovered and not self.disabled) else 2,
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
    def __init__(self, game_state) -> None:
        self.tile_size = 96
        self.grid_spacing = 10
        self.game_state = game_state
        self.size = (
            4 * (self.tile_size + self.grid_spacing),
            4 * (self.tile_size + self.grid_spacing),
        )
        self.tiles = [Tile("", self.tile_size) for _ in range(16)]

    def draw(self, surface, x, y):
        self.tiles = [
            Tile("", self.tile_size)
            for _ in range(len(self.game_state.get_all_unsolved_words()))
        ]
        solved_groups = self.game_state.solved_groups
        for i, group in enumerate(solved_groups):
            group_tile = SolvedGroup(group, self.size[1], self.tile_size)
            group_tile.draw(surface, x, y + i * (self.tile_size + self.grid_spacing))

        for row in range(4 - len(solved_groups)):
            for column in range(4):
                tile = self.tiles[row * 4 + column]
                tile.text = self.game_state.get_all_unsolved_words()[row * 4 + column]
                tile.selected = tile.text in self.game_state.selected_words
                tile.draw(
                    surface,
                    x + column * (tile.box_size + self.grid_spacing),
                    y
                    + (row + len(solved_groups)) * (tile.box_size + self.grid_spacing),
                )


if __name__ == "__main__":
    main()
