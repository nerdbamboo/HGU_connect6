CXX = g++
CXXFLAGS = -std=c++17

all: play

AI_Algorithm_Code.o: AI_Algorithm_Code.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

Connect6_HGU.o: Connect6_HGU.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@ -I/Users/smcho/Downloads/json-develop/include/
	
play: Connect6_HGU.o AI_Algorithm_Code.o
	$(CXX) $^ -o $@

clean:
	rm -f AI_Algorithm_Code.o Connect6_HGU.o play
