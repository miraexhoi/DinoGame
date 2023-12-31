import pygame
import os
import random

# Pygame 초기화
pygame.init()

# 화면 크기 설정
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 게임 이미지 로드
RUNNING = [pygame.image.load(os.path.join("Assets/Animals", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Animals", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Animals", "RabbitJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Animals", "CatDuck1.png")),
           pygame.image.load(os.path.join("Assets/Animals", "CatDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))


class Dinosaur:
    X_POS = 80  # 공룡의 초기 x 좌표
    Y_POS = 310  # 공룡의 초기 y 좌표
    Y_POS_DUCK = 340  # 웅크린 공룡의 y 좌표
    JUMP_VEL = 8.5  # 토끼의 점프 속도

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.cat_duck = False  # 웅크린 상태 여부
        self.dino_run = True  # 달리는 상태 여부
        self.rabbit_jump = False  # 점프 상태 여부

        self.step_index = 0  # 이미지 스프라이트 인덱스
        self.jump_vel = self.JUMP_VEL  # 현재 점프 속도
        self.image = self.run_img[0]  # 현재 이미지
        self.dino_rect = self.image.get_rect()  # 공룡의 사각형 영역
        self.dino_rect.x = self.X_POS  # 공룡의 x 좌표
        self.dino_rect.y = self.Y_POS  # 공룡의 y 좌표

    def update(self, userInput):
        if self.cat_duck:
            self.duck()  # 현재 상태가 "절반 앉기"인 경우 애니메이션 업데이트
        if self.dino_run:
            self.run()  # 현재 상태가 "달리기"인 경우 달리기 애니메이션 업데이트
        if self.rabbit_jump:
            self.jump()  # 현재 상태가 "점프"인 경우 점프 애니메이션 업데이트

        if self.step_index >= 10:
            self.step_index = 0  # 스텝 인덱스가 10 이상인 경우 0으로 재설정.

        if userInput[pygame.K_UP] and not self.rabbit_jump:
            self.cat_duck = False
            self.dino_run = False
            self.rabbit_jump = True
        elif userInput[pygame.K_DOWN] and not self.rabbit_jump:
            self.cat_duck = True
            self.dino_run = False
            self.rabbit_jump = False
        elif not (self.rabbit_jump or userInput[pygame.K_DOWN]):
            self.cat_duck = False
            self.dino_run = True
            self.rabbit_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]  # 이미지 스프라이트 변경
        self.dino_rect = self.image.get_rect()  # 사각형 영역 업데이트
        self.dino_rect.x = self.X_POS  # x 좌표 업데이트
        self.dino_rect.y = self.Y_POS_DUCK  # y 좌표 업데이트
        self.step_index += 1
        if self.step_index >= 10:
            self.step_index = 0

    def run(self):
        self.image = self.run_img[self.step_index // 5]  # 이미지 스프라이트 변경
        self.dino_rect = self.image.get_rect()  # 사각형 영역 업데이트
        self.dino_rect.x = self.X_POS  # x 좌표 업데이트
        self.dino_rect.y = self.Y_POS  # y 좌표 업데이트
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.rabbit_jump:  # 점프 중인 경우
            self.dino_rect.y -= self.jump_vel * 4  # 공룡의 y 좌표 조정
            self.jump_vel -= 0.8  # 점프 속도 감소
        if self.jump_vel < -self.JUMP_VEL:  # 최대 점프 높이에 도달한 경우
            self.rabbit_jump = False  # 점프 상태 종료
            self.jump_vel = self.JUMP_VEL  # 점프 속도 초기화

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)  # 구름의 초기 x 좌표 설정
        self.y = random.randint(50, 100)  # 구름의 초기 y 좌표 설정
        self.image = CLOUD  # 구름 이미지 (위 두 줄로 랜덤한 위치에 구름 생성)
        self.width = self.image.get_width()  # 구름 이미지의 너비

    def update(self):
        self.x -= game_speed  # 구름을 왼쪽으로 이동
        if self.x < - self.width:  # 구름이 화면 왼쪽을 벗어나면
            self.x = SCREEN_WIDTH + random.randint(2600, 3000)  # 새로운 위치에 재배치
            self.y = random.randint(50, 100)  # 새로운 높이로 재설정

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image  # 장애물 이미지 리스트
        self.type = type  # 장애물 종류
        self.rect = self.image[self.type].get_rect()  # 장애물 충돌 박스(rect) 생성
        self.rect.x = SCREEN_WIDTH  # 장애물 초기 x 좌표 설정

    def update(self):
        self.rect.x -= game_speed  # 장애물을 왼쪽으로 이동
        if self.rect.x < -self.rect.width:  # 장애물이 화면 왼쪽을 벗어나면
            obstacles.pop()  # 리스트의 마지막 요소를 반환하고 제거

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)  # 장애물 이미지 그리기

class SmallCactus(Obstacle): # Obstacle 클래스를 상속받는 SmallCactus 클래스
    def __init__(self, image):
        self.type = random.randint(0, 2)  # 장애물 종류 랜덤 설정
        super().__init__(image, self.type)  # 부모 클래스의 초기화 메서드 호출
        self.rect.y = 325  # 장애물의 y 좌표 설정

class LargeCactus(Obstacle): # Obstacle 클래스를 상속받는 LargeCactus 클래스
    def __init__(self, image):
        self.type = random.randint(0, 2)  # 장애물 종류 랜덤 설정
        super().__init__(image, self.type)  # 부모 클래스의 초기화 메서드 호출
        self.rect.y = 300  # 장애물의 y 좌표 설정

class Bird(Obstacle): # Obstacle 클래스를 상속받는 Bird 클래스
    def __init__(self, image):
        self.type = 0  # 장애물 종류 설정
        super().__init__(image, self.type)  # 부모 클래스의 초기화 메서드 호출
        self.rect.y = 250  # 장애물의 y 좌표 설정
        self.index = 0  # 애니메이션 인덱스 설정

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)  # 이미지와 위치를 화면에 그림
        self.index += 1  # 애니메이션 인덱스 증가


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles  # 전역 변수 선언
    run = True  # 실행 상태를 나타내는 변수를 True로 설정
    clock = pygame.time.Clock()  # 프레임 속도를 제어하기 위해 Clock 객체 생성
    player = Dinosaur()  # Dinosaur 객체 생성
    cloud = Cloud()  # Cloud 객체 생성
    game_speed = 14  # 초기 게임 속도 설정
    x_pos_bg = 0  # 배경의 초기 x 좌표 설정
    y_pos_bg = 380  # 배경의 초기 y 좌표 설정
    points = 0  # 초기 점수를 설정
    font = pygame.font.Font('freesansbold.ttf', 20)  # 텍스트를 렌더링하기 위한 폰트 객체 생성
    obstacles = []  # 장애물을 저장하기 위한 빈 리스트 생성
    death_count = 0  # 초기 사망 횟수를 설정

    def score():
        global points, game_speed  # 전역 변수에 접근하기 위해 global 키워드를 사용
        points += 1  # 점수를 1 증가
        if points % 100 == 0:  # 점수가 100의 배수인 경우
            game_speed += 1  # 게임 속도를 1 증가

        text = font.render("Scores: " + str(points), True, (0, 0, 0))  # 텍스트를 렌더링
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg  # 전역 변수에 접근하기 위해 global 키워드를 사용
        image_width = BG.get_width()  # 배경 이미지의 너비를 가져옴
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))  # 배경 이미지를 그림
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))  # 배경 이미지를 다시 그림
        if x_pos_bg <= -image_width:  # 배경 이미지가 왼쪽으로 완전히 사라진 경우
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))  # 배경 이미지를 다시 그림
            x_pos_bg = 0  # 배경의 x 좌표를 초기화
        x_pos_bg -= game_speed  # 배경의 x 좌표를 게임 속도에 따라 이동

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  # 종료 이벤트가 발생하면 실행 상태를 False로 변경

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()  # 사용자 입력을 userInput에 받음

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:  # 장애물이 없는 경우
            if random.randint(0, 2) == 0:  # 랜덤하게 장애물 생성
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):  # 플레이어와 장애물이 충돌한 경우
                pygame.time.delay(2000)  # 2초 동안 일시 정지
                death_count += 1
                menu(death_count)  # 메뉴를 호출하여 게임을 재시작

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)  # 프레임 속도를 30으로 제한
        pygame.display.update()

def menu(death_count: object) -> object:
    global points  # 전역 변수에 접근하기 위해 global 키워드를 사용
    run = True  # 메뉴 실행 상태를 나타내는 변수를 True로 설정
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)  # 폰트 객체를 생성

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))  # 시작 메시지를 렌더링
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))  # 재시작 메시지를 렌더링
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))  # 점수를 렌더링
            scoreRect = score.get_rect()  # 점수의 사각 영역을 가져옴
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)  # 점수의 중심 좌표를 설정
            SCREEN.blit(score, scoreRect)

        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # 스페이스바를 눌렀을 때
                    main()  # 게임을 재실행하는 함수 호출

menu(death_count=0)