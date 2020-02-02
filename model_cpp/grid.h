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
};



class CellList
{
public:
     CellNode *head, *tail;
     int size;
    CellList();
    ~CellList();
    void add(Cell * cell);
    void sort();
    void deleteDead();
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
    void addCell(int x, int y, Cell * cell);
    void fill_sources(double glu, double oxy);
    void cycle_cells();
    void diffuse(double diff_factor);
private:
    void change_neigh_counts(int x, int y, int val);
    int xsize;
    int ysize;
    CellList ** cells;
    double ** glucose;
    double ** oxygen;
    int ** neigh_counts;
    SourceList * sources;
};


#endif //RADIO_RL_GRID_H
