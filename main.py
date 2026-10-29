from pygame import *

wiwi, hehe = 700, 500
PADDLE_HEIGHT = 150
WINNING_SCORE = 5

init()
screen = display.set_mode((wiwi, hehe))
display.set_caption("Ping-Pong")
background = transform.scale(image.load("background.webp"), (wiwi, hehe))
score_font = font.SysFont(None, 56)
message_font = font.SysFont(None, 36)


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect(topleft=(player_x, player_y))

    def reset(self):
        screen.blit(self.image, self.rect)


class Player(GameSprite):
    def move(self, up_key, down_key):
        keys = key.get_pressed()
        if keys[up_key]:
            self.rect.y -= self.speed
        if keys[down_key]:
            self.rect.y += self.speed
        self.rect.y = max(5, min(self.rect.y, hehe - self.rect.height - 5))


class Ball(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__(player_image, player_x, player_y, player_speed, width, height)
        self.start_x = player_x
        self.start_y = player_y
        self.speed_x = 4
        self.speed_y = 4

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0:
            self.rect.top = 0
            self.speed_y = abs(self.speed_y)
        elif self.rect.bottom >= hehe:
            self.rect.bottom = hehe
            self.speed_y = -abs(self.speed_y)

    def serve(self, direction):
        self.rect.center = (wiwi // 2, hehe // 2)
        self.speed_x = 4 * direction
        self.speed_y = 4


def draw_scores(left_score, right_score):
    left_text = score_font.render(str(left_score), True, (255, 255, 255))
    right_text = score_font.render(str(right_score), True, (255, 255, 255))
    screen.blit(left_text, (wiwi // 2 - 70, 20))
    screen.blit(right_text, (wiwi // 2 + 40, 20))


FPS = 60
clock = time.Clock()
player1 = Player("leftplayer.png", 5, 200, 5, 50, PADDLE_HEIGHT)
player2 = Player("rightplayer.png", 645, 200, 5, 50, PADDLE_HEIGHT)
ball = Ball("ball.png", 350, 250, 4, 50, 50)
left_score = 0
right_score = 0
game = True
game_over = False
winner = ""

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                game = False
            elif game_over and e.key == K_r:
                left_score = 0
                right_score = 0
                winner = ""
                game_over = False
                player1.rect.y = 200
                player2.rect.y = 200
                ball.serve(1)

    screen.blit(background, (0, 0))

    if not game_over:
        player1.move(K_w, K_s)
        player2.move(K_UP, K_DOWN)
        ball.update()

        if ball.speed_x < 0 and ball.rect.colliderect(player1.rect):
            ball.rect.left = player1.rect.right
            ball.speed_x = abs(ball.speed_x)
        elif ball.speed_x > 0 and ball.rect.colliderect(player2.rect):
            ball.rect.right = player2.rect.left
            ball.speed_x = -abs(ball.speed_x)

        if ball.rect.right < 0:
            right_score += 1
            ball.serve(-1)
        elif ball.rect.left > wiwi:
            left_score += 1
            ball.serve(1)

        if left_score >= WINNING_SCORE:
            winner = "Left player wins!"
            game_over = True
        elif right_score >= WINNING_SCORE:
            winner = "Right player wins!"
            game_over = True

    player1.reset()
    player2.reset()
    ball.reset()
    draw_scores(left_score, right_score)

    if game_over:
        result = message_font.render(winner, True, (200, 150, 150))
        restart = message_font.render("Press R to play again", True, (200, 150, 150))
        screen.blit(result, result.get_rect(center=(wiwi // 2, hehe // 2 - 20)))
        screen.blit(restart, restart.get_rect(center=(wiwi // 2, hehe // 2 + 25)))

    display.update()
    clock.tick(FPS)

quit()