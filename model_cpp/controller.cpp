//
// Created by grego on 01/02/2020.
//

#include "controller.h"
#include <stdlib.h>
#include <iostream>

using namespace std;

Controller::Controller(Grid *grid, int hcells, int xsize, int ysize): xsize(xsize), ysize(ysize),  tick(0), self_grid(false), grid(grid)  {
    HealthyCell::count = 0;
    CancerCell::count = 0;
    char stages[5] = {'1', 's', '2', 'm', 'q'};
    for (int i = 0; i < hcells; i++){
        Cell * new_cell = new HealthyCell(stages[rand() % 5]);
        grid -> addCell(rand() % xsize, rand() % ysize, new_cell, 'h');
    }
    grid -> addCell(xsize / 2, ysize / 2, new CancerCell(stages[rand() % 4]), 'c');
}

Controller::Controller(int hcells, int xsize, int ysize, int sources_num): xsize(xsize), ysize(ysize), tick(0), self_grid(true) {
    HealthyCell::count = 0;
    CancerCell::count = 0;
    grid = new Grid(xsize, ysize, sources_num);
    char stages[5] = {'1', 's', '2', 'm', 'q'};
    for (int i = 0; i < hcells; i++){
        Cell * new_cell = new HealthyCell(stages[rand() % 5]);
        grid -> addCell(rand() % xsize, rand() % ysize, new_cell, 'h');
    }
    grid -> addCell(xsize / 2, ysize / 2, new CancerCell(stages[rand() % 4]), 'c');
}

Controller::~Controller() {
    if (self_grid)
        delete grid;
}

void Controller::go() {
    grid -> fill_sources(100, 4500);
    grid -> cycle_cells();
    grid -> diffuse(0.2);
    tick++;
}

void Controller::irradiate(double dose){
    grid -> irradiate(dose);
}

int Controller::cell_types(int x, int y){
    return grid->cell_types(x, y);
}

double ** Controller::currentGlucose(){
    return grid->currentGlucose();
}

double ** Controller::currentOxygen(){
    return grid->currentOxygen();
}

int main(){
    srand(42);
    Grid * grid = new Grid(50, 50, 50);
    Controller * controller = new Controller(grid, 1000, 50, 50);
    cout << "Tick : " << 0 << " HCells : " << HealthyCell::count << " CCells : " << CancerCell::count << endl;
    for (int i = 1; i <= 2000; i++){
        controller->go();
        if (i > 400 && i % 24 == 0)
            grid -> irradiate(2.0);
        cout << "Tick : " << i << " HCells : " << HealthyCell::count << " CCells : " << CancerCell::count << endl;
    }
    delete controller;
    delete grid;
}
