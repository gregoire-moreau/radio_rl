//
// Created by grego on 18/01/2020.
//

#ifndef RADIO_RL_GRID_H
#define RADIO_RL_GRID_H


#include "cell.h"
//https://www.codementor.io/@codementorteam/a-comprehensive-guide-to-implementation-of-singly-linked-list-using-c_plus_plus-ondlm5azr
struct CellNode
{
    int x, y;
    Cell * cell;
    CellNode *next;
    char type;
};

struct OARZone{
    int x1, x2, y1, y2;
};


class CellList
{
public:
    CellNode *head, *tail;
    int size;
    int oar_count;
    int ccell_count;
    CellList();
    ~CellList();
    void add(Cell * cell, char type);
    void deleteDeadAndSort();
    int CellTypeSum();
    void wake_oar();
    void add(Cell *cell, char type, int x, int y);
    void add(CellNode * toAdd, char type);
};

struct Source{
    int x, y;
    Source * next;
};

class SourceList{
public:
    Source *head, *tail;
    int size;
    SourceList();
    ~SourceList();
    void add(int x, int y);
};

class Grid {
public:
    Grid(int xsize, int ysize, int sources_num);
    Grid(int xsize, int ysize, int sources_num, OARZone * oar);
    ~Grid();
    void addCell(int x, int y, Cell * cell, char type);
    void fill_sources(double glu, double oxy);
    void cycle_cells();
    void diffuse(double diff_factor);
    void irradiate(double dose);
    void irradiate(double dose, double radius);
    void irradiate(double dose, double radius, double center_x, double center_y);
    int cell_types(int x, int y);
    int type_head(int x, int y);
    double ** currentGlucose();
    double ** currentOxygen();
    double tumor_radius(int center_x, int center_y);
    void compute_center();
private:
    void change_neigh_counts(int x, int y, int val);
    int rand_min(int x, int y, int max);
    int rand_adj(int x, int y);
    int find_missing_oar(int x, int y);
    
    void min_helper(int x, int y, int& curr_min, int * pos, int& counter);
    void adj_helper(int x, int y, int * pos, int& counter);
    void missing_oar_helper(int x, int y, int&  curr_min, int * pos, int& counter);
    void wake_surrounding_oar(int x, int y);
    void wake_helper(int x, int y);
    int rand_cycle(int num);
    void addToGrid(CellList * newCells);
    int sourceMove(int x, int y);
    int xsize;
    int ysize;
    CellList ** cells;
    double ** glucose;
    double ** oxygen;
    double ** glucose_helper;
    double ** oxygen_helper;
    int ** neigh_counts;
    SourceList * sources;
    OARZone * oar;
    double center_x;
    double center_y;
    int * rand_helper;
};


#endif //RADIO_RL_GRID_H
