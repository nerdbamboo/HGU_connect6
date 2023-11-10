//#include <Windows.h>
#include<bits/stdc++.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <ctype.h>
using namespace std;


#include "Connect6Algo.h"
#include <nlohmann/json.hpp>

unsigned s_time;
int terminateAI;
int width = 19, height = 19;
int cnt = 2;
int myColor;

#define BOARD_SIZE 20
int board[BOARD_SIZE][BOARD_SIZE];


void domymove(int x[], int y[], int cnt) {
		mymove(x, y, cnt);
}

int showBoard(int x, int y) {
	return board[x][y];
}

void printBoard(){ // 바둑판 출력
    // for(int i = -2; i < width + 1; i++){
    //     if(i <= 0) printf(" ");
    //     else if(i < 10) printf("%d ", i);
    //     else printf("%d", i);
    // }
    // printf("\n   ---------------------------------------\n");
    for (int i = 0; i < width; i++) {
        // if(i < 9)
        //     printf("%d |", i+1);
        // else
        //     printf("%d|", i+1);
		for (int j = 0; j < height; j++) {
		    printf("%d ", board[i][j]);
		}
        printf("\n");
	}
}

int main() {
    //init();

	nlohmann::json input, moveX, moveY, selfMoveX, selfMoveY;
    cin >> input >> moveX >> moveY >> selfMoveX >> selfMoveY;

	//int prev[BOARD_SIZE][BOARD_SIZE];
	int x[2], y[2], mx[2], my[2];
	//int cmp = 0;
	for(int i = 0; i < 19; i++) {
		for(int j = 0; j < 19; j++) {
			//prev[i][j] = board[i][j];
			board[i][j] = input[i][j].get<int>();
			// if(prev[i][j] != board[i][j] && board[i][j] == 2) {
			// 	if(cmp < 2) {
			// 		x[cmp] = i;
			// 		y[cmp] = j;
			// 	}
			// 	cmp++;
			// }
		}
	}
	for(int i = 0; i < 2; i++){
		x[i] = moveX[i];
		y[i] = moveY[i];
		mx[i] = selfMoveX[i];
		my[i] = selfMoveY[i];
	}
	//cout <<"x:" << x[0] << " " << x[1] << "\ny:" << y[0] << " " << y[1] << endl; 
 	opmove(x, y, 2);
	RenewalMytMoves(mx[0], mx[1], my[0], my[1]);
	int gameEnd = myturn(cnt);

	return 0;
}

int isFree(int x, int y)
{
	return x >= 0 && y >= 0 && x < width && y < height && board[x][y] == 0;
}

void init() {	
	for (int i = 0; i < width; i++) {
		for (int j = 0; j < height; j++) {
			board[i][j] = 0;
		}
	}
}

void mymove(int x[], int y[], int cnt) {
	for (int i = 0; i < cnt; i++) {
		if (isFree(x[i], y[i])) {
			board[x[i]][y[i]] = 1;
            printf("%d %d\n", x[i] + 1, y[i] + 1);
		}
		else {
            printf("ERROR 이미 돌이 있는 위치입니다. MY[%d, %d]", x[i], y[i]);
		}
	}
}

void opmove(int x[], int y[], int cnt) {
	// for (int i = 0; i < cnt; i++) {
	// 	if (isFree(x[i], y[i])) {
	// 		board[x[i]][y[i]] = 2;
	// 	}
	// 	else {
    //         printf("ERROR 이미 돌이 있는 위치입니다. OP[%d, %d]", x[i], y[i]);
	// 	}
	// }
	if(cnt == 2) // 상대가 두 수를 착수했을 경우에만
		RenewalOpponentMoves(x[0], x[1], y[0], y[1]); // 상대방의 착수를 갱신
}

void block(int x, int y) {
	if (isFree(x, y)) {
		board[x][y] = 3;
	}
}
