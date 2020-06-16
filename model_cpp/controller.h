//
// Created by grego on 01/02/2020.
//

#ifndef RADIO_RL_CONTROLLER_H
#define RADIO_RL_CONTROLLER_H


#include "grid.h"
#include "cell.h"

class Controller {
public:
    Controller(Grid * grid, int hcells, int xsize, int ysize);
    Controller(int hcells, int xsize, int ysize, int sources_num);
    Controller(int hcells, int xsize, int ysize, int sources_num, int x1, int x2, int y1, int y2);
    ~Controller();
    void irradiate(double dose);
    void irradiate_center(double dose);
    void irradiate(double dose, double radius);
    void irradiate_center(double dose, double radius);
    void go();
    int pixel_density(int x, int y);
    int pixel_type(int x, int y);
    double ** currentGlucose();
    double ** currentOxygen();
    double tumor_radius();
    int xsize, ysize;
    int tick;
    double get_center_x();
    double get_center_y();
private:
    bool self_grid;
    Grid * grid;
    OARZone * oar;
};


#endif //RADIO_RL_CONTROLLER_H
