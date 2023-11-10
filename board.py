import pygame
import sys
import subprocess
import json

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
#상하좌우 여백 크기
margin = 20

board = [[0 for j in range(GRID_WIDTH)] for i in range(GRID_HEIGHT)]

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
                            print("Black Win!!")
                        else:
                            print("White Win!!")
                        return False
    return True

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("바둑판")
    is_black_turn = False
    running = True
    draw_board(screen)
    cnt = 1
    
    # Setting blokcing location
    red_cnt = 0
    while True:
        if(red_cnt == 4):
            # Setting first black_stone
            row = 10
            col = 10
            screen.blit(black_stone, (row * GRID_SIZE - (size/2), col * GRID_SIZE - (size/2)))
            board[col-1][row-1] = 1
            pygame.display.flip()
            break
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if margin < x < WINDOW_WIDTH - margin and margin < y < WINDOW_HEIGHT - margin:
                    row = round(x / GRID_SIZE)
                    col = round(y / GRID_SIZE)
                    screen.blit(red_stone, (row * GRID_SIZE - (size/2), col * GRID_SIZE - (size/2)))
                    board[col][row] = 3
                    red_cnt += 1
        pygame.display.flip()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos

                # 클릭한 위치가 여백 안에 있는 경우에만 처리
                if margin < x < WINDOW_WIDTH - margin and margin < y < WINDOW_HEIGHT - margin:
                    row = round(x / GRID_SIZE)
                    col = round(y / GRID_SIZE)
                    if board[row][col] == 0:
                        # 돌 놓기 (검은 돌과 흰 돌 번갈아가며 놓기)
                        if is_black_turn:  # is_black_turn 변수를 정의해야 합니다.
                            input_data = json.dumps(board) # 배열을 JSON 문자열로 변환
                            result = subprocess.run(['./play'], input=input_data.encode(), stdout=subprocess.PIPE)
                            output = result.stdout.decode()
                            print("C++ 프로그램의 출력 결과:", output)
                            output = result.stdout.decode().strip().split()
                            row = float(output[0])
                            col = float(output[1])
                            print(int(row))
                            print(int(col))
                            screen.blit(black_stone, (col * GRID_SIZE - (size/2), row * GRID_SIZE - (size/2)))
                            board[int(row)-1][int(col)-1] = 1
                            
                            row = float(output[2])
                            col = float(output[3])
                            print(int(row))
                            print(int(col))
                            screen.blit(black_stone, (col * GRID_SIZE - (size/2), row * GRID_SIZE - (size/2)))
                            board[int(row)-1][int(col)-1] = 1
                            
                            # check debugging
                            for i in range(19):
                                for j in range(19):
                                    print(board[i][j], end = " ")
                                print()
                        else:
                            print(f"클릭한 위치: Row {col}, Col {row}")
                            screen.blit(white_stone, (row * GRID_SIZE - (size/2), col * GRID_SIZE - (size/2)))
                            board[col-1][row-1] = 2
                            
                            # check debugging
                            for i in range(19):
                                for j in range(19):
                                    print(board[i][j], end = " ")
                                print()
                        
                        if cnt == 2:
                            is_black_turn = not is_black_turn
                            cnt = 0
                        if is_black_turn:
                            cnt += 2
                        else:
                            cnt += 1
                
        
        running = check_connect6(board)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
