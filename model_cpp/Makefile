CXX = g++
CXXFLAGS = -Wall -std=gnu++11 -g

main: scalar_model.o cell.o grid.o
	$(CXX) $(CXXFLAGS) -o main scalar_model.o cell.o grid.o

scalar_model.o: scalar_model.cpp scalar_model.h grid.h cell.h
	$(CXX) $(CXXFLAGS) -c scalar_model.cpp

cell.o: cell.h grid.h

grid.o: grid.h cell.h

.PHONY : clean
clean :
	rm -f *.o
	rm -f main
	rm -rf build

