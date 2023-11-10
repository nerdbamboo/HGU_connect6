CXX = g++
CXXFLAGS = -std=c++17

all: play

AI_Algorithm_Code.o: AI_Algorithm_Code.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

Connect6_HGU.o: Connect6_HGU.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@ -I/Users/38a/Desktop/Handong/23-2/HGU_connect6/json-develop/include

play: Connect6_HGU.o AI_Algorithm_Code.o
	$(CXX) $^ -o $@

clean:
	rm -f AI_Algorithm_Code.o Connect6_HGU.o play
