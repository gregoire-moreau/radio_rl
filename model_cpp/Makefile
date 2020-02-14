CXX = g++
CXXFLAGS = -Wall -std=gnu++11

main: controller.o cell.o grid.o
	$(CXX) $(CXXFLAGS) -o main controller.o cell.o grid.o

controller.o: controller.cpp controller.h grid.h cell.h
	$(CXX) $(CXXFLAGS) -c controller.cpp

cell.o: cell.h grid.h

grid.o: grid.h cell.h

.PHONY : clean
clean :
	rm -f *.o
	rm -f main
	rm -rf build


condense:
	cat cell.h grid.h controller.h > condensed.h
	echo "#include \"condensed.h\"" > condensed.cpp
	cat cell.cpp grid.cpp controller.cpp >> condensed.cpp
