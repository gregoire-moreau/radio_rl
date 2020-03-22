//
// Created by grego on 01/02/2020.
//

#include "controller.h"
#include <stdlib.h>
#include <iostream>

using namespace std;

Controller::Controller(Grid *grid, int hcells, int xsize, int ysize): xsize(xsize), ysize(ysize),  tick(0), self_grid(false), grid(grid), oar(nullptr)  {
    HealthyCell::count = 0;
    CancerCell::count = 0;
    char stages[5] = {'1', 's', '2', 'm', 'q'};
    for (int i = 0; i < hcells; i++){
        Cell * new_cell = new HealthyCell(stages[rand() % 5]);
        grid -> addCell(rand() % xsize, rand() % ysize, new_cell, 'h');
    }
    grid -> addCell(xsize / 2, ysize / 2, new CancerCell(stages[rand() % 4]), 'c');
}

Controller::Controller(int hcells, int xsize, int ysize, int sources_num): xsize(xsize), ysize(ysize), tick(0), self_grid(true), oar(nullptr) {
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

Controller::Controller(int hcells, int xsize, int ysize, int sources_num, int x1, int x2, int y1, int y2):xsize(xsize), ysize(ysize), tick(0), self_grid(true){
    HealthyCell::count = 0;
    CancerCell::count = 0;
    OARCell::count = 0;
    if(x1 > x2){
        int temp = x1;
        x1 = x2;
        x2 = temp;
    }
    if(y1 > y2){
        int temp = y1;
        y1 = y2;
        y2 = temp;
    }
    oar = new OARZone;
    oar -> x1 = x1;
    oar -> x2 = x2;
    oar -> y1 = y1;
    oar -> y2 = y2;
    grid = new Grid(xsize, ysize, sources_num, oar);
    char stages[5] = {'1', 's', '2', 'm', 'q'};
    for(int x = x1; x < x2; x++){
        for(int y = y1; y < y2; y++){
            Cell * new_cell = new OARCell('q');
            grid -> addCell(x, y, new_cell, 'o');
        }
    }
    for (int i = 0; i < hcells; i++){
        int x = rand() % xsize;
        int y = rand() % ysize;
        if (!(x >= x1 && x < x2 && y >= y1 && y < y2)){
            Cell * new_cell = new HealthyCell(stages[rand() % 5]);
            grid -> addCell(x, y, new_cell, 'h');
        }
    }
    grid -> addCell(xsize / 2, ysize / 2, new CancerCell(stages[rand() % 4]), 'c');

}

Controller::~Controller() {
    if (self_grid)
        delete grid;
    if(oar)
        delete oar;
}

void Controller::go() {
    grid -> fill_sources(100, 4500);
    grid -> cycle_cells();
    grid -> diffuse(0.2);
    tick++;
    if(tick % 30 == 0)
        grid -> compute_center();
}

void Controller::irradiate(double dose){
    grid -> irradiate(dose);
}

int Controller::cell_types(int x, int y){
    return grid->cell_types(x, y);
}

int Controller::type_head(int x, int y){
    return grid -> type_head(x, y);
}

double ** Controller::currentGlucose(){
    return grid->currentGlucose();
}

double ** Controller::currentOxygen(){
    return grid->currentOxygen();
}

double Controller::tumor_radius(){
    return grid -> tumor_radius(xsize / 2, ysize /2);
}

int main(){
    srand(42);
    Controller * controller = new Controller(1000, 50, 50, 50, 5, 15, 5, 15);
    cout << "Tick : " << 0 << " HCells : " << HealthyCell::count << " CCells : " << CancerCell::count << " OARCells : " << OARCell::count << endl;
    for (int i = 1; i <= 2000; i++){
        controller->go();
        if (i > 400 && i % 24 == 0)
            controller -> irradiate(2.0);
        cout << "Tick : " << i << " HCells : " << HealthyCell::count << " CCells : " << CancerCell::count  << " OARCells : " << OARCell::count << endl;
    }
    delete controller;
}
