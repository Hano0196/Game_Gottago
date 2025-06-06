import pygame, sys
from pygame.locals import *
import random

# pygame 초기화
pygame.init()

# text 구현
font = pygame.font.Font('resource/온글잎 박다현체.ttf', 70)
explain_font = pygame.font.Font('resource/온글잎 박다현체.ttf', 40)
number_font = pygame.font.Font('resource/온글잎 박다현체.ttf', 30)

# text list
gottago = font.render('Gotta go', True, (255, 255, 255))
explain_yian_1 = explain_font.render('이안이는 신입생이라 놀고만 싶어요!', True, (255, 255, 255))
explain_yian_2 = explain_font.render('이안이가 공부하지 않고 놀 수 있게', True, (255, 255, 255))
explain_rule = explain_font.render('과탑 신해솔을 피해 달리세요!', True, (255, 255, 255))
explain_start = font.render('Space bar로 게임 시작', True, (255, 255, 255))
explain_end = font.render('Esc로 게임 종료', True, (255, 255, 255))
explain_retry = font.render('Space bar로 다시 시작', True, (255, 255, 255))

# 사운드 기능 추가
background_sound = pygame.mixer.Sound("resource/exploration-chiptune-rpg-adventure-theme-336428.mp3")
background_sound.play(-1)

# 색상 세팅(RGB)
red = (255, 0, 0)
orange = (255, 153, 51)
yellow = (255, 255, 0)
green = (0, 255, 0)
seagreen = (60, 179, 113)
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)
violet = (204, 153, 255)
pink = (255, 153, 153)
grey = (213, 213, 213)
light_grey = (246, 246, 246)
light_black = (76, 76, 76)

# 화면 생성(전체 화면, 928 x 793)
screen_width = 928
screen_height = 793
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gotta go")
clock = pygame.time.Clock()
color = (0, 255, 0)
background = pygame.image.load('resource/Background.png') # 배경 화면 추가

# 적 속성
enemy_speed = 7
enemy_x = 0
enemy_y = 0

#score reset 함수
score = 0
def reset():
    global score
    score = 0
    return score

class Player(pygame.sprite.Sprite):
    # player image loading and setting function
    def __init__(self):
        super().__init__()
        # 플레이어 사진 불러오기
        self.image = pygame.image.load('resource/문이안2.png')
        # 플레이어 크기 조정
        self.image = pygame.transform.scale(self.image, (110, 135))
        # 이미지 크기의 직사각형 모양 불러오기
        self.rect = self.image.get_rect()
        # rec 크기 축소(충돌판정 이미지에 맞추기 위함)
        self.rect = self.rect.inflate(-20,-20)
        # 이미지 시작 위치 설정
        self.rect.center = (818, 658)

    # 플레이어 키보드 움직임 설정 함수
    def move(self):
        keys = pygame.key.get_pressed()

        if keys[K_ESCAPE]:
            pygame.quit()
            sys.exit()

        if self.rect.left > 0:
            if keys[K_LEFT]:
                self.rect.move_ip(-7, 0)
                position_p = self.rect.center
                return position_p

        if self.rect.right < 928:
            if keys[K_RIGHT]:
                self.rect.move_ip(7, 0)
                position_p = self.rect.center
                return position_p

class Enemy(pygame.sprite.Sprite):
    # 적의 이미지 로딩 및 설정 함수
    def __init__(self):
        super().__init__()
        # 적 사진 불러오기
        self.image = pygame.image.load('resource/haesol(vertical)2.png')
        # 적 크기 조정
        self.image = pygame.transform.scale(self.image, (175, 355))
        # 이미지 크기의 직사각형 모양 불러오기
        self.rect = self.image.get_rect()
        # rec 크기 축소(충돌 판정 이미지에 맞추기 위함)
        self.rect = self.rect.inflate(-20, -30)
        # 이미지 시작 위치 설정
        self.rect.center = (random.randint(86, 842), 0)

    # 적의 움직임 설정 함수+ 플레이어 점수 측정
    def move(self):
        global score
        # 적을 10 픽셀 크기만큼 위에서 아래로 떨어지도록 설정
        self.rect.move_ip(0, enemy_speed)  # x,y좌표 설정
        # 이미지 가 화면 끝에 있으면(플레이어가 물체를 피하면) 다시 이미지 위치 세팅 + 1점 추가
        if self.rect.bottom > 803:
            score += 1
            self.rect.top = 0
            self.rect.center = (random.randint(86, 842), 0)
        return self.rect.center

# 시작(intro) 화면
def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # ESC == 종료 키
            keys = pygame.key.get_pressed()
            if keys[K_ESCAPE]:
                pygame.quit()
                sys.exit()
            if keys[K_SPACE]:
                return game()

        # 배경 화면
        screen.blit(background, (0, 0)) # 배경 화면 추가
        screen.blit(gottago, (335, 126.5))
        screen.blit(explain_rule, (281, 350.5))
        screen.blit(explain_yian_1, (245, 250.5))
        screen.blit(explain_yian_2, (253, 300.5))
        screen.blit(explain_start, (185, 636.5))
        screen.blit(explain_end, (275, 550.5))

        pygame.display.flip()
        clock.tick(60)

def game(speed = enemy_speed):

    p1 = Player()
    e1 = Enemy()

    # 신해솔(enemy) 객체 그룹화하기
    enemies = pygame.sprite.Group()
    enemies.add(e1)

    # 전체 그룹 묶기
    all_groups = pygame.sprite.Group()
    all_groups.add(p1)
    all_groups.add(e1)

    # 적 개체 1초(1000ms)마다 새로 생기는 이벤트 생성
    in_crease_speed = pygame.USEREVENT + 1
    pygame.time.set_timer(in_crease_speed, 1000)

    while True:
        for event in pygame.event.get():
            if event.type == in_crease_speed:
                speed += 0.5
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background, (0, 0)) # 배경 화면 추가
        scores = explain_font.render("score: " + str(score), True, white)
        # screen.blit(player, (player_x_pos, player_y_pos))
        screen.blit(scores, (10, 0))

        # 게임 내 물체 움직임 생성
        for i in all_groups:
            screen.blit(i.image, i.rect)
            i.move()
            # if str(i) == '<Player Sprite(in 1 groups)>':
            #     player_pos = i
            # else:
            #     enemy_pos = i

        for i in all_groups:
            screen.blit(i.image, i.rect)
            i.move()
            # if str(i) == '<Player Sprite(in 1 groups)>':
            #     player_pos = i
            # else:
            #     enemy_pos = i

        if pygame.sprite.spritecollideany(p1, enemies):
            for i in all_groups:
                i.kill()
            # go to outro
            pygame.display.update()
            game_outro()

        pygame.display.flip()
        clock.tick(60)

def game_outro():
    outro = True

    while outro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if keys[K_SPACE]:
            reset()
            return game()

        screen.blit(background, (0, 0))
        your_score = font.render("Your score: " + str(score), True, white)
        screen.blit(your_score, (279, 200))
        screen.blit(explain_retry, (185, 600.5))
        screen.blit(explain_end, (275, 520.5))

        pygame.display.flip()
        clock.tick(60)

game_intro()
