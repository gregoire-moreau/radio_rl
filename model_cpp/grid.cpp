//
// Created by grego on 18/01/2020.
//

#include <algorithm>
#include "grid.h"

CellList::CellList():head(nullptr), tail(nullptr), size(0) {}
CellList::~CellList() {
    CellNode * current = head;
    CellNode * next;
    while (current){
        next = current -> next;
        delete current;
        current = next;
    }
}

void CellList::add(Cell *cell) {
    CellNode * newNode = new CellNode;
    newNode -> cell = cell;
    newNode -> next = nullptr;
    tail -> next = newNode;
    tail = newNode;
    size++;
}

SourceList::SourceList():head(nullptr), tail(nullptr), size(0) {}
SourceList::~SourceList() {
    Source * current = head;
    Source * next;
    while (current){
        next = current -> next;
        delete current;
        current = next;
    }
}

void SourceList::add(int x, int y) {
    Source * newNode = new Source;
    newNode -> x = x;
    newNode -> y = y;
    newNode -> next = nullptr;
    tail -> next = newNode;
    tail = newNode;
    size++;
}

void CellList::deleteDead(){
    bool found_head = false;
    CellNode * current = head;
    while(current){
        if (!current -> cell -> alive){
            delete current->cell;

        }
    }
}
void CellList::sort(){}




Grid::Grid(int xsize, int ysize, int sources_num):xsize(xsize), ysize(ysize){
    cells = new CellList*[xsize];
    glucose = new double*[xsize];
    oxygen = new double*[xsize];
    neigh_counts = new int*[xsize];
    for(int i = 0; i < xsize; i++) {
        cells[i] = new CellList[ysize];
        glucose[i] = new double[ysize];
        std::fill_n(glucose[i], ysize, 100.0);
        oxygen[i] = new double[ysize];
        std::fill_n(oxygen[i], ysize, 10000.0);
        neigh_counts[i] = new int[ysize]();
    }
    sources = new SourceList();
    for (int i = 0; i < sources_num; i++){
        sources->add(rand() % xsize, rand() % ysize);
    }
}

Grid::~Grid() {
    for (int i = 0; i < xsize; i++){
        delete[] cells[i]; // Do I have to?
        delete[] glucose[i];
        delete[] oxygen[i];
    }
    delete[] cells;
    delete[] glucose;
    delete[] oxygen;
    delete sources;
}

void Grid::change_neigh_counts(int x, int y, int val) {
    bool up = (x > 0);
    bool down = (x < xsize-1);
    bool left = (y > 0);
    bool right = (y < ysize -1);
    if (up){
        neigh_counts[x-1][y] += val;
        if (left)
            neigh_counts[x-1][y-1] += val;
        if (right)
            neigh_counts[x-1][y+1] += val;
    }
    if (down){
        neigh_counts[x+1][y] += val;
        if (left)
            neigh_counts[x+1][y-1] += val;
        if (right)
            neigh_counts[x+1][y+1] += val;
    }
    if (left)
        neigh_counts[x][y-1] += val;
    if (right)
        neigh_counts[x][y+1] += val;
}


void Grid::addCell(int x, int y, Cell *cell) {
    cells[x][y].add(cell);
    change_neigh_counts(x, y, 1);
}

void Grid::fill_sources(double glu, double oxy) {
    Source * current = sources -> head;
    while(current){
        glucose[current->x][current->y] += glu;
        oxygen[current->x][current->y] += oxy;
        current = current -> next;
    }
}

void Grid::cycle_cells() {
    for (int i = 0; i < xsize; i++){
        for (int j = 0; j < ysize; j++){
            CellNode * current = cells[i][j].head;
            while(current){
                cell_cycle_res result = current->cell->cycle(glucose[i][j], oxygen[i][j], neigh_counts[i][j]);
                glucose[i][j] -= result.glucose;
                oxygen[i][j] -= result.oxygen;
                if (result.new_cell == 'h'){
                }
                if (result.new_cell == 'c'){

                }
                current = current -> next;
            }
            int init_count = cells[i][j].size;
            cells[i][j].deleteDead();
            change_neigh_counts(i, j, cells[i][j].size - init_count);
        }
    }
}

void Grid::diffuse(double diff_factor) {

}