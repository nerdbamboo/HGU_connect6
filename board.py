import pygame
import sys
import subprocess
import json
import tkinter as tk
from tkinter import messagebox
import time

GRID_SIZE = 40
STONE_SIZE = 36

GRID_WIDTH = 20
GRID_HEIGHT = 20

WINDOW_WIDTH = GRID_WIDTH * GRID_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * GRID_SIZE

BLACK = (0, 0, 0)
BROWN = (213, 175, 52)
WHITE = (255, 255, 255)

# 검은 돌과 흰 돌 이미지
black_stone = pygame.image.load("black_stone.png")
white_stone = pygame.image.load("white_stone.png")
red_stone = pygame.image.load("red_stone.png")

size = 40
black_stone = pygame.transform.scale(black_stone, (size, size))
white_stone = pygame.transform.scale(white_stone, (size, size))
red_stone = pygame.transform.scale(red_stone, (size, size))

stone_list = []
stone_list.append(red_stone)
stone_list.append(black_stone)
stone_list.append(white_stone)

#상하좌우 여백 크기
margin = 20
board = [[0 for j in range(19)] for i in range(19)]

def get_turn():
    result = {'value': None}  # 딕셔너리를 이용하여 결과를 저장

    def on_button_click(WB):
        # 버튼 클릭 시 선택한 플레이어 값을 저장하고 창을 닫음
        result['value'] = WB
        custom_box.destroy()

    # 커스텀 대화 상자 생성
    custom_box = tk.Toplevel()
    custom_box.title("흑, 백 선택")

    # 메시지 텍스트 레이블 추가
    label = tk.Label(custom_box, text="흑돌로 시작할지 백돌로 시작할지 정하시오")
    label.pack(padx=30, pady=20)

    # "Black" 버튼과 "White" 버튼 추가
    black_button = tk.Button(custom_box, text="흑돌", command=lambda: on_button_click(1))
    black_button.pack(side="left", padx=10)

    white_button = tk.Button(custom_box, text="백돌", command=lambda: on_button_click(2))
    white_button.pack(side="right", padx=10)

    custom_box.wait_window()  # 창이 닫힐 때까지 대기

    return result['value']

def get_block_num():
    result = {'value': None}  # 딕셔너리를 이용하여 결과를 저장

    def on_button_click(block_num):
        # 버튼 클릭 시 선택한 블럭 개수를 저장하고 창을 닫음
        result['value'] = block_num
        custom_box.destroy()

    # 커스텀 대화 상자 생성
    custom_box = tk.Toplevel()
    custom_box.title("블럭 개수 설정")

    # 메시지 텍스트 레이블 추가
    label = tk.Label(custom_box, text="블럭의 개수를 설정하세요")
    label.pack(padx=30, pady=20)

    # 1에서 4까지의 버튼 추가
    for block_num in range(0, 5):
        button = tk.Button(custom_box, text=str(block_num), command=lambda b=block_num: on_button_click(b))
        button.pack(side="left", padx=10)

    custom_box.wait_window()  # 창이 닫힐 때까지 대기

    return result['value']

def draw_board(screen):
    screen.fill(BROWN)
    
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (x, margin), (x, WINDOW_HEIGHT - margin), 2)
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (margin, y), (WINDOW_WIDTH - margin, y), 2)
        
def check_connect6(board):
    # 바둑판의 크기
    width = len(board)
    height = len(board[0])

    # 가로, 세로, 대각선 방향 (우상향, 우하향)을 정의
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for x in range(width):
        for y in range(height):

            if board[x][y] == 1 or board[x][y] == 2:
                for dx, dy in directions:
                    count = 0
                    for i in range(6):
                        nx, ny = x + i * dx, y + i * dy
                        if 0 <= nx < width and 0 <= ny < height and board[nx][ny] == board[x][y]:
                            count += 1
                        else:
                            break
                    if count == 6:
                        if(board[x][y] == 1):
                            print("MY AI WIN!!")
                        else:
                            print("OP AI WIN!!")
                        return False
    return True

def main():

    me = get_turn()
    global MY_AI, OP_AI

    MY_AI = me
    OP_AI = 3 - me

    opMoveX = []
    opMoveY = []

    selfMoveX = [-1, -1]
    selfMoveY = [-1, -1]

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("바둑판")
    is_my_ai_turn = False
    running = True
    draw_board(screen)
    cnt = 0
    # Setting blokcing location
    red_cnt = 0
    red_cnt_num = get_block_num()

    while True:
        if(red_cnt >= red_cnt_num):
            # Setting first black_stone
            row = 10
            col = 10
            screen.blit(black_stone, (row * GRID_SIZE - (size/2), col * GRID_SIZE - (size/2)))
            if MY_AI == 1:
                board[col-1][row-1] = 1
                selfMoveX = [9, -1]
                selfMoveY = [9, -1]
            else:
                board[col-1][row-1] = 2
                opMoveX = [9, -1]
                opMoveY = [9, -1]
                is_my_ai_turn = True
            
            pygame.display.flip()
            break
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if margin < x < WINDOW_WIDTH - margin and margin < y < WINDOW_HEIGHT - margin:
                    row = round(x / GRID_SIZE)
                    col = round(y / GRID_SIZE)
                    screen.blit(red_stone, (row * GRID_SIZE - (size/2), col * GRID_SIZE - (size/2)))
                    # print(col-1, row-1)
                    board[col-1][row-1] = 3
                    red_cnt += 1
        pygame.display.flip()

    while running:
        
        # Turn for AI    
        if is_my_ai_turn:
            
            input_data = json.dumps(board) # 배열을 JSON 문자열로 변환
            input_data += f'\n{opMoveX}\n{opMoveY}\n{selfMoveX}\n{selfMoveY}'
            #print(input_data)
            opMoveX.clear()
            opMoveY.clear()
            selfMoveX.clear()
            selfMoveY.clear()

            result = subprocess.run(['./play'], input=input_data.encode(), stdout=subprocess.PIPE)

            output = result.stdout.decode().strip().split()
            print(output)
            
            row = float(output[0])
            col = float(output[1])
            selfMoveX.append(int(row)-1)
            selfMoveY.append(int(col)-1)
            screen.blit(stone_list[MY_AI], (col * GRID_SIZE - (size/2), row * GRID_SIZE - (size/2)))
            board[int(row)-1][int(col)-1] = 1
            
            row = float(output[2])
            col = float(output[3])
            selfMoveX.append(int(row)-1)
            selfMoveY.append(int(col)-1)
            screen.blit(stone_list[MY_AI], (col * GRID_SIZE - (size/2), row * GRID_SIZE - (size/2)))
            board[int(row)-1][int(col)-1] = 1
            
            cnt += 2

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos

                    # 클릭한 위치가 여백 안에 있는 경우에만 처리
                    if margin < x < WINDOW_WIDTH - margin and margin < y < WINDOW_HEIGHT - margin:
                        row = round(x / GRID_SIZE)
                        col = round(y / GRID_SIZE)
                        if board[col-1][row-1] == 0:
                            # Turn for human
                            
                            screen.blit(stone_list[OP_AI], (row * GRID_SIZE - (size/2), col * GRID_SIZE - (size/2)))
                            board[col-1][row-1] = 2
                            opMoveX.append(col-1)
                            opMoveY.append(row-1)
                            cnt += 1

        if cnt == 2:
            is_my_ai_turn = not is_my_ai_turn
            cnt = 0
        
        running = check_connect6(board)
        pygame.display.flip()

    time.sleep(5)  # 5초 동안 프로그램 실행을 중지
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
