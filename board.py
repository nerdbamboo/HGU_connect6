import pygame
import sys

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
size = 40
black_stone = pygame.transform.scale(black_stone, (size, size))
white_stone = pygame.transform.scale(white_stone, (size, size))
#상하좌우 여백 크기
margin = 20

board = [[0 for j in range(GRID_WIDTH)] for i in range(GRID_HEIGHT)]

def draw_board(screen):
    screen.fill(BROWN)
    
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (x, margin), (x, WINDOW_HEIGHT - margin), 2)
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (margin, y), (WINDOW_WIDTH - margin, y), 2)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("바둑판")
    is_black_turn = True
    running = True
    draw_board(screen)
    cnt = 2
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
                        print(f"클릭한 위치: 행 {row + 1}, 열 {col + 1}")
                        print(col + 1, row + 1)

                    # 돌 놓기 (검은 돌과 흰 돌 번갈아가며 놓기)
                        if is_black_turn:  # is_black_turn 변수를 정의해야 합니다.
                            screen.blit(black_stone, (row * GRID_SIZE - (size/2), col * GRID_SIZE - (size/2)))
                        else:
                            screen.blit(white_stone, (row * GRID_SIZE - (size/2), col * GRID_SIZE - (size/2)))
                        
                        board[row][col] = 1
                        if cnt == 2:
                            is_black_turn = not is_black_turn
                            cnt = 0
                        cnt += 1
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
