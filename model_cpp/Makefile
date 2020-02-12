CXX = g++
CXXFLAGS = -Wall -std=gnu++11

main: controller.o cell.o grid.o
	$(CXX) $(CXXFLAGS) -o main controller.o cell.o grid.o

controller.o: controller.cpp controller.h grid.h cell.h
	$(CXX) $(CXXFLAGS) -c controller.cpp

cell.o: cell.h grid.h

grid.o: grid.h cell.h
