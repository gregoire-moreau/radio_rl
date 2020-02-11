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
    ~Controller();
    void irradiate(double dose);
    void go();
    int cell_types(int x, int y);
    double ** currentGlucose();
    double ** currentOxygen();
    int xsize, ysize;
    int tick;
private:
    bool self_grid;
    Grid * grid;
};


#endif //RADIO_RL_CONTROLLER_H
