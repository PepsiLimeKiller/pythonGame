import pygame
import random
#################################################################################
# 기본 초기화 (반드시 해야 하는 것들)
pygame.init() # 초기화 (반드시 필요)

# 화면 크기 설정
screen_width = 640 # 가로 크기
screen_height = 480 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("마망 피하기") # 게임 이름

# FPS
clock = pygame.time.Clock()

#################################################################################

# 1. 사용자 게임 초기화 (배경화면, 게임 이미지, 좌표, 속도, 시간, 폰트 등)

# 배경화면과 게임 캐릭터 이미지를 로드
background = pygame.image.load("/Users/heesulee/Desktop/pythonGame/pygame_basic/background.png")
character = pygame.image.load("/Users/heesulee/Desktop/pythonGame/pygame_basic/character.png")
enemy = pygame.image.load("/Users/heesulee/Desktop/pythonGame/pygame_basic/enemy.png")

#캐릭터 이미지의 각각 가로, 세로 정보
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height

enemy_size = enemy.get_rect().size
enemy_width = enemy_size[0]
enemy_height = enemy_size[1]
enemy_x_pos = screen_width / 2 - enemy_width / 2
enemy_y_pos = 0



# 캐릭터의 이동(속도)
to_x = 0
to_y = 0
character_speed = 0.3
enemy_speed = 0.5

# 게임 폰트
game_font = pygame.font.Font(None, 40)

#시간 설정
start_time = pygame.time.get_ticks()

# 이벤트 루프
running = True # 게임이 진행중인가?
while running:
    dt = clock.tick(30) # 게임 화면 초당 프레임 수를 설정

# 캐릭터가 100만큼 이동을 해야함
# 10 fps : 1초 동안에 10번 동작 -> 1번에 몇 만큼 이동? 10만큼! 10 * 10 = 100
# 20 fps : 1초 동안에 20번 동작 -> 1번에 몇 만큼 이동? 20만큼! 5 * 20 = 100

    # 2. 이벤트 처리 (키보드 ,마우스 등)
    for event in pygame.event.get(): # 어떤 이벤트가 발생 하였는가?
        if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생 하였는가?
             running = False # 게임이 진행중이 아님
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                to_x += character_speed

        if event.type == pygame.KEYUP:
            to_x = 0

    # 3. 게임 캐릭터 위치 정의
    
    # 3-1. 캬루의 x좌표 이동방향변화
    character_x_pos += to_x * dt
    
    # 3-2. 마망의 낙하속도(고정)
    enemy_y_pos += enemy_speed * dt

    # 만약에 캐릭터들이 화면을 넘어가는 경우
    # 1. 캬루가 넘어가는 경우
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
    
    # 2. 마망이 넘어가는 경우
    if enemy_y_pos > screen_height:
        enemy_y_pos = - enemy_height
        enemy_x_pos = random.uniform(0, screen_width - enemy_width)

    # 4. 충돌 처리

    # 충돌에 관한 두 캐릭터의 정보
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    # 만약 마망과 캬루가 충돌하였을 경우 부딪쳤다는 문장 출력 후 프로그램 종료
    if pygame.Rect.colliderect(character_rect, enemy_rect):
        print("마망과 캬루가 충돌하였습니다. 프로그램을 종료합니다.")
        running = False

    # 5. 화면에 그리기
    elapsed_time = pygame.time.get_ticks()
    timer = game_font.render(str(int((elapsed_time - start_time) / 1000)), True, (255,255,255))

    screen.blit(background, (0,0))
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))
    screen.blit(timer, (10,10))
    pygame.display.update() # 게임화면을 다시 그리기

# 종료 딜레이
# pygame.time.delay(2000)

# pygame 종료
pygame.quit()