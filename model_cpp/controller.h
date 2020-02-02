//
// Created by grego on 01/02/2020.
//

#ifndef RADIO_RL_CONTROLLER_H
#define RADIO_RL_CONTROLLER_H


#include "grid.h"

class Controller {
public:
    Controller(Grid * grid, int hcells, int xsize, int ysize);
    ~Controller();
    void go();
private:
    Grid * grid;
    int tick = 0;
};


#endif RADIO_RL_CONTROLLER_H
