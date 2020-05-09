#include "controller.h"
#include <stdlib.h>
#include <iostream>

using namespace std;

/**
 * Constructor of a Controller with the Grid already constructed
 *
 * Will randomly set hcells HealthyCells on the provided grid, and a CancerCell in the center
 *
 * @param grid The provided grid
 * @param hcells The number of HealthyCells to set randomly on the grid
 * @param xsize The number of rows of the grid
 * @param ysize The number of columns of the grid
 */
Controller::Controller(Grid *grid, int hcells, int xsize, int ysize): xsize(xsize), ysize(ysize),  tick(0), self_grid(false), grid(grid), oar(nullptr)  {
    HealthyCell::count = 0;
    CancerCell::count = 0;
    char stages[5] = {'1', 's', '2', 'm', 'q'};
    for (int i = 0; i < hcells; i++){
        Cell * new_cell = new HealthyCell(stages[rand() % 5]); //We create a new cell and put it in a random stage
        grid -> addCell(rand() % xsize, rand() % ysize, new_cell, 'h'); //We add that cell on a random pixel of the grid
    }
    grid -> addCell(xsize / 2, ysize / 2, new CancerCell(stages[rand() % 4]), 'c'); //We add the unique cancer cell in the center
}

/**
 * Constructor of a Controller
 *
 * Will first create the grid, then randomly set hcells HealthyCells on the provided grid, and a CancerCell in the center
 *
 * @param hcells The number of HealthyCells to set randomly on the grid
 * @param xsize The number of rows of the grid
 * @param ysize The number of columns of the grid
 * @param sources_num The number of nutrient sources to put on the grid
 */
Controller::Controller(int hcells, int xsize, int ysize, int sources_num): xsize(xsize), ysize(ysize), tick(0), self_grid(true), oar(nullptr) {
    HealthyCell::count = 0;
    CancerCell::count = 0;
    grid = new Grid(xsize, ysize, sources_num);
    char stages[5] = {'1', 's', '2', 'm', 'q'};
    float prob = 100.0 * (float) hcells / (xsize * ysize);
    for (int i = 0; i < xsize; i++){
        for(int j = 0; j < ysize; j++){
            if (rand() % 100 < prob){
                Cell * new_cell = new HealthyCell(stages[rand() % 5]);
                grid -> addCell(i, j, new_cell, 'h');
            }
        }
    }
    grid -> addCell(xsize / 2, ysize / 2, new CancerCell(stages[rand() % 4]), 'c');

}


/**
 * Constructor of a Controller with an Organ-at-Risk zone
 *
 * Will first create the grid, then randomly set hcells HealthyCells on the provided grid, and a CancerCell in the center
 * The OAR zone is a rectangle defined by coordinates (x1, y1) and (x2, y2)
 *
 * @param hcells The number of HealthyCells to set randomly on the grid
 * @param xsize The number of rows of the grid
 * @param ysize The number of columns of the grid
 * @param sources_num The number of nutrient sources to put on the grid
 * @param x1, y1 The first corner of the OARZone rectangle
 * @param x2, y2 The opposite corner of the OARZone rectangle
 */
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
/**
 * Destructor of the controller
 */
Controller::~Controller() {
    if (self_grid)
        delete grid;
    if(oar)
        delete oar;
}

/**
 * Simulate one hour
 *
 * Refill the sources, cycle all the cells, diffuse the nutrients on the grid
 */
void Controller::go() {
    grid -> fill_sources(130, 4500); //O'Neil, Jalalimanesh
    grid -> cycle_cells();
    grid -> diffuse(0.5);
    tick++;
    if(tick % 24 == 0){ // Once a day, recompute the current center of the tumor (used for angiogenesis)
        grid -> compute_center();
    }
}

/**
 * Irradiate the tumor with a certain dose
 *
 * @param dose The dose of radiation in grays
 */
void Controller::irradiate(double dose){
    grid -> irradiate(dose);
}

/**
 * Irradiate the tumor with a certain dose and radius
 *
 * @param dose The dose of radiation in grays
 * @param radius The radius of irradiation
 */
void Controller::irradiate(double dose, double radius){
    grid -> irradiate(dose, radius);
}

/**
 * Irradiate the tumor with a certain dose and radius around the center of the grid
 *
 * @param dose The dose of radiation in grays
 * @param radius The radius of irradiation
 */
void Controller::irradiate_center(double dose, double radius){
    grid -> irradiate(dose, radius, xsize / 2, ysize / 2);
}

/**
 * Irradiate the tumor with a certain dose around the center of the grid
 *
 * @param dose The dose of radiation in grays
 */
void Controller::irradiate_center(double dose){
    double radius = grid -> tumor_radius(xsize / 2, ysize / 2);
    grid -> irradiate(dose, radius, xsize / 2, ysize / 2);
}


/**
 * Return a weighted sum of the types of cells at a certain position
 *
 * @param x The x coordinate of the pixel
 * @param y The y coordinate of the pixel
 * @return The weighted sum
 */
int Controller::cell_types(int x, int y){
    return grid->cell_types(x, y);
}

/**
 * Return a the type of the first cell at a position
 *
 * @param x The x coordinate of the pixel
 * @param y The y coordinate of the pixel
 * @return An integer representing the type
 */
int Controller::type_head(int x, int y){
    return grid -> type_head(x, y);
}

/**
 * Return the current glucose array
 */
double ** Controller::currentGlucose(){
    return grid->currentGlucose();
}

/**
 * Return the current oxygen array
 */
double ** Controller::currentOxygen(){
    return grid->currentOxygen();
}

/**
 * Return the current tumor's radius
 */
double Controller::tumor_radius(){
    return grid -> tumor_radius(xsize / 2, ysize /2);
}

/**
 * Simulate a basic treatment to ensure that there are no obvious bugs/crashes
 */
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
