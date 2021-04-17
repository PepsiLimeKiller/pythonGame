import pygame
import os
#################################################################################
# 기본 초기화 (반드시 해야 하는 것들)
pygame.init() # 초기화 (반드시 필요)

# 화면 크기 설정
screen_width = 640 # 가로 크기
screen_height = 480 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("마망의 괴물잡기") # 게임 이름

# FPS
clock = pygame.time.Clock()

#################################################################################

# 1. 사용자 게임 초기화 (배경화면, 게임 이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__) # 현재 파일의 위치
image_path = os.path.join(current_path, "image") # 이미지 폴더 위치 반환

# 배경 만들기
background = pygame.image.load(os.path.join(image_path, "background.png"))

# 스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] # 스테이지를 높이 위에 캐릭터는 두기 위해서

#캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height - stage_height

# 캐릭터 이동 방향 
character_to_x = 0

#캐릭터 이동 속도
character_speed = 5

# 공 만들기 (4개 크기에 대해 따로 처리)
ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))
]

# 공 크기에 따른 최초 스피드
ball_speed_y = [-18, -15, -12, -9] # index 0, 1, 2, 3 에 해당하는 값

# 공들
balls = []

# 최초 발생하는 큰 공 추가
balls.append({
    "pos_x" : 50, # 공의 x 좌표
    "pos_y" : 50,  # 공의 Y 좌표
    "img_idx" : 0, # 공의 이미지 인덱스
    "to_x" : 3, # x축 이동방향, -3이면 왼쪽, 3이면 오른쪽
    "to_y" : -6, # y축 이동방향, -6이면 위로, 6이면 아래로
    "init_spd_y": ball_speed_y[0] # y축 최초 속도
})

# 사라질 무기, 공 정보 저장 변수
weapon_to_remove = -1
ball_to_remove = -1

# 무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한 번에 여러 발 발사 가능
weapons = []

# 무기 이동속도
weapon_speed = 10

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
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_position = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_position = character_y_pos
                weapons.append([weapon_x_position, weapon_y_position])
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    # 3. 게임 캐릭터 위치 정의
    character_x_pos += character_to_x

    # 맵 밖으로 나갈 경우
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 무기가 맵 천장에 닿을 경우
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    # 무기 위치 조정
    # 100, 200 -> 180, 160, 140, ...
    # 500, 200 -> 180, 160, 140, ...
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons] # 무기 위치를 위로

    # 공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]
        
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width: # 공이 사이드에 부딪힌 경우
            ball_val["to_x"] *= -1
         
        if ball_pos_y > screen_height - stage_height - ball_height: # 공이 바닥에 닿는 경우
            ball_val["to_y"] = ball_val["init_spd_y"]
        else:
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]


    # 4. 충돌 처리

    # 캐릭터 rect 정보 저장
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_rect = ball_images[ball_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        #공과 캐릭터 충돌처리
        if pygame.Rect.colliderect(character_rect, ball_rect):
            print("죽음")
            running = False
            break

        # 공과 무기들 충돌 처리
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # 무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # 충돌 체크
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx # 해당 무기 없애기 위한 값 설정
                ball_to_remove = ball_idx
                # 가장 작은 크기의 공이 아니라면 다음 단계의 공으로 나눠주기
                if ball_img_idx < 3:
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # 나눠진 공 정보
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    balls.append({ # 왼쪽으로 가는 공
                        "pos_x" : ball_pos_x + ball_width / 2 - small_ball_width / 2, # 공의 x 좌표
                        "pos_y" : ball_pos_y + ball_height / 2 - small_ball_height / 2,  # 공의 Y 좌표
                        "img_idx" : ball_img_idx + 1, # 공의 이미지 인덱스
                        "to_x" : -3, # x축 이동방향, -3이면 왼쪽, 3이면 오른쪽
                        "to_y" : -6, # y축 이동방향, -6이면 위로, 6이면 아래로
                        "init_spd_y": ball_speed_y[ball_img_idx + 1] # y축 최초 속도
                    })
                    balls.append({ # 왼쪽으로 가는 공
                        "pos_x" : ball_pos_x + ball_width / 2 - small_ball_width / 2, # 공의 x 좌표
                        "pos_y" : ball_pos_y + ball_height / 2 - small_ball_height / 2,  # 공의 Y 좌표
                        "img_idx" : ball_img_idx + 1, # 공의 이미지 인덱스
                        "to_x" : 3, # x축 이동방향, -3이면 왼쪽, 3이면 오른쪽
                        "to_y" : -6, # y축 이동방향, -6이면 위로, 6이면 아래로
                        "init_spd_y": ball_speed_y[ball_img_idx + 1] # y축 최초 속도
                    })
                break
        
        # 충돌된 공 or 무기 없애기
        if ball_to_remove > -1:
            del balls[ball_to_remove]
            ball_to_remove = -1
        if weapon_to_remove > -1:
            del weapons[weapon_to_remove]
            weapon_to_remove = -1

    # 5. 화면에 그리기

    pygame.display.update() # 게임화면을 다시 그리기
    screen.blit(background, (0,0))

    for weapon_x_position, weapon_y_position in weapons:
        screen.blit(weapon, (weapon_x_position, weapon_y_position))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))
        
    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    

# pygame 종료
pygame.quit()