//
// Created by grego on 18/01/2020.
//

#ifndef RADIO_RL_GRID_H
#define RADIO_RL_GRID_H


#include "cell.h"
//https://www.codementor.io/@codementorteam/a-comprehensive-guide-to-implementation-of-singly-linked-list-using-c_plus_plus-ondlm5azr
struct CellNode
{
    Cell * cell;
    CellNode *next;
    char type;
};



class CellList
{
public:
    CellNode *head, *tail;
    int size;
    CellList();
    ~CellList();
    void add(Cell * cell, char type);
    void deleteDeadAndSort();
    int CellTypeSum();
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
    ~Grid();
    void addCell(int x, int y, Cell * cell, char type);
    void fill_sources(double glu, double oxy);
    void cycle_cells();
    void diffuse(double diff_factor);
    void irradiate(double dose);
    int cell_types(int x, int y);
private:
    void change_neigh_counts(int x, int y, int val);
    int rand_min(int x, int y);
    void min_helper(int x, int y, int& curr_min, int * pos, int& counter);
    int xsize;
    int ysize;
    CellList ** cells;
    double ** glucose;
    double ** oxygen;
    double ** glucose_helper;
    double ** oxygen_helper;
    int ** neigh_counts;
    SourceList * sources;
    double tumor_radius(int center_x, int center_y);
};


#endif //RADIO_RL_GRID_H
