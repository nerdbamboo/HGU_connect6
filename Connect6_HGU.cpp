// Samsung Go Tournament Form C Connect6Algo (g++-4.8.3)

// <--------------- 이 Code를 수정하면  작동하지 않을 수 있습니다 ------------------>

//#include <Windows.h>
#include<bits/stdc++.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <ctype.h>
using namespace std;

// #include </Users/38a/anaconda3/include/python3.10/Python.h>

#include "Connect6Algo.h"
#include <nlohmann/json.hpp>

unsigned s_time;
int terminateAI;
int width = 19, height = 19;
int cnt = 2;
int myColor;

static char cmd[256];
//static HANDLE event1, event2;
#define BOARD_SIZE 20
int board[BOARD_SIZE][BOARD_SIZE];

static void getLine() {
	int c, bytes;

	bytes = 0;
	do {
		c = getchar();
		if (c == EOF) exit(0);
		if (bytes < sizeof(cmd)) cmd[bytes++] = (char)c;
	} while (c != '\n');
	cmd[bytes - 1] = 0;
	if (cmd[bytes - 2] == '\r') cmd[bytes - 2] = 0;
}

int setLine(char *fmt, ...) {
	int i;
	va_list va;
	va_start(va, fmt);
	i = vprintf(fmt, va);
	putchar('\n');
	fflush(stdout);
	va_end(va);
	return i;
}

static const char *getParam(const char *command, const char *input) {
	int n1, n2;
	n1 = (int)strlen(command);
	n2 = (int)strlen(input);
	//if (n1 > n2 || _strnicmp(command, input, n1)) return NULL;
	input += strlen(command);
	while (isspace(input[0])) input++;	
	return input;
}


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
    init();

	nlohmann::json input;
    cin >> input;

	for(int i=0; i<BOARD_SIZE; i++) 
		for(int j=0; j<BOARD_SIZE; j++)
			board[i][j] = input[i][j].get<int>();

	int gameEnd = myturn(1);

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
	for (int i = 0; i < cnt; i++) {
		if (isFree(x[i], y[i])) {
			board[x[i]][y[i]] = 2;
		}
		else {
            printf("ERROR 이미 돌이 있는 위치입니다. OP[%d, %d]", x[i], y[i]);
		}
	}
	if(cnt == 2) // 상대가 두 수를 착수했을 경우에만
		RenewalOpponentMoves(x[0], x[1], y[0], y[1]); // 상대방의 착수를 갱신
}

void block(int x, int y) {
	if (isFree(x, y)) {
		board[x][y] = 3;
	}
}
