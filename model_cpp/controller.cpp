//
// Created by grego on 01/02/2020.
//

#include "controller.h"
#include <stdlib.h>
#include <iostream>

using namespace std;

Controller::Controller(Grid *grid, int hcells, int xsize, int ysize): grid(grid) {
    char stages[5] = {'1', 's', '2', 'm', 'q'};
    for (int i = 0; i < hcells; i++){
        Cell * new_cell = new HealthyCell(stages[rand() % 5]);
        grid -> addCell(rand() % xsize, rand() % ysize, new_cell);
    }
    grid -> addCell(xsize / 2, ysize / 2, new CancerCell(stages[rand() % 4]));
}

Controller::~Controller() {
    //delete grid;
}

void Controller::go() {
    grid -> fill_sources(100, 4500);
    grid -> cycle_cells();
    grid -> diffuse(0.2);
    tick++;
}



int main(){
    srand(42);
    Grid * grid = new Grid(50, 50, 50);
    Controller * controller = new Controller(grid, 50, 50, 1000);
    for (int i = 0; i < 2000; i++){
        controller->go();
        cout << "Tick : " << i << "HCells : " << HealthyCell::count << " CCells : " << CancerCell::count << endl;
    }
    delete controller;
    delete grid;
}