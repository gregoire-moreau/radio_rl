//
// Created by grego on 18/01/2020.
//

#include <algorithm>
#include "grid.h"
#include <assert.h> 
#include <math.h> 
#include <iostream>

CellList::CellList():head(nullptr), tail(nullptr), size(0) {}
CellList::~CellList() {
    CellNode * current = head;
    CellNode * next;
    while (current){
        next = current -> next;
        delete current -> cell;
        delete current;
        current = next;
    }
}

void CellList::add(Cell *cell, char type) {
    CellNode * newNode = new CellNode;
    assert(cell);
    newNode -> cell = cell;
    newNode -> type = type;
    if (size == 0){
        head = newNode;
        tail = newNode;
        newNode -> next = nullptr;
    }
    else if (type == 'h'){
        tail -> next = newNode;
        tail = newNode;
        newNode -> next = nullptr;
        
    } else if(type == 'c'){
        newNode -> next = head;
        head = newNode;
    }
    size++;
}

void CellList::deleteDeadAndSort(){
    bool found_head = false;
    CellNode * current = head;
    CellNode ** previous_next_pointer;
    while(current){
        if (!(current -> cell -> alive)){
            delete current->cell;
            CellNode * toDel = current;
            current = current -> next;
            delete toDel;
            size--;
        } else if (!found_head){
            head = current;
            tail = current;
            previous_next_pointer = & (current -> next);
            current = current -> next;
            found_head = true;
        }
        else{
            tail = current;
            *previous_next_pointer = current;
            previous_next_pointer = & (current -> next);
            current = current -> next;
        }
    }
    if (!found_head){
        assert(size == 0);
        head = nullptr;
        tail = nullptr;
    } else{
        tail -> next = nullptr;
    }
}

int CellList::CellTypeSum(){
    if (size == 0)
        return 0;
    int to_ret = 0;
    CellNode * current = head;
    while(current){
        if (current -> type == 'h')
            to_ret++;
        else if (current -> type == 'c')
            to_ret--;
        current = current -> next;
    }
    return to_ret;
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
    if (size == 0){
        head = newNode;
    } else{
        tail -> next = newNode;   
    }
    tail = newNode;
    size++;
}


Grid::Grid(int xsize, int ysize, int sources_num):xsize(xsize), ysize(ysize){
    cells = new CellList*[xsize];
    glucose = new double*[xsize];
    glucose_helper = new double*[xsize];
    oxygen = new double*[xsize];
    oxygen_helper = new double*[xsize];
    neigh_counts = new int*[xsize];
    for(int i = 0; i < xsize; i++) {
        cells[i] = new CellList[ysize];
        glucose[i] = new double[ysize];
        glucose_helper[i] = new double[ysize];
        std::fill_n(glucose[i], ysize, 100.0);
        oxygen[i] = new double[ysize];
        oxygen_helper[i] = new double[ysize];
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
        delete[] cells[i];
        delete[] glucose[i];
        delete[] oxygen[i];
        delete[] glucose_helper[i];
        delete[] oxygen_helper[i];
        delete[] neigh_counts[i];
    }
    delete[] cells;
    delete[] glucose;
    delete[] oxygen;
    delete sources;
    delete[] oxygen_helper;
    delete[] glucose_helper;
    delete[] neigh_counts;
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


void Grid::addCell(int x, int y, Cell *cell, char type) {
    cells[x][y].add(cell, type);
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
                    int downhill = rand_min(i, j);
                    addCell(downhill / ysize, downhill % ysize, new HealthyCell('1'), 'h');
                }
                if (result.new_cell == 'c'){
                    int downhill = rand_adj(i, j);
                    addCell(downhill / ysize, downhill % ysize, new CancerCell('1'), 'c');
                }
                current = current -> next;
            }
            int init_count = cells[i][j].size;
            cells[i][j].deleteDeadAndSort();
            change_neigh_counts(i, j, cells[i][j].size - init_count);
        }
    }
}



int Grid::rand_min(int x, int y){
    int counter = 0;
    int curr_min = 100000;
    int pos[8];

    min_helper(x-1, y-1, curr_min, pos, counter);
    min_helper(x-1, y, curr_min, pos, counter);
    min_helper(x-1, y+1, curr_min, pos, counter);
    min_helper(x, y-1, curr_min, pos, counter);
    min_helper(x, y+1, curr_min, pos, counter);
    min_helper(x+1, y-1, curr_min, pos, counter);
    min_helper(x+1, y, curr_min, pos, counter);
    min_helper(x+1, y+1, curr_min, pos, counter);

    return pos[rand() % counter];
}

void Grid::min_helper(int x, int y, int&  curr_min, int * pos, int& counter){
    if (x >= 0 && x < xsize && y >= 0 && y < ysize){
        if (cells[x][y].size < curr_min){
            pos[0] = x*ysize+y;
            counter = 1;
            curr_min = cells[x][y].size;
        } else if(cells[x][y].size == curr_min){
            pos[counter] = x*ysize+y;
            counter++;
        }
    }
}

int Grid::rand_adj(int x,  int y){
    int counter = 0;
    int pos[8];

    adj_helper(x-1, y-1, pos, counter);
    adj_helper(x-1, y,  pos, counter);
    adj_helper(x-1, y+1, pos, counter);
    adj_helper(x, y-1,  pos, counter);
    adj_helper(x, y+1, pos, counter);
    adj_helper(x+1, y-1, pos, counter);
    adj_helper(x+1, y, pos, counter);
    adj_helper(x+1, y+1,  pos, counter);

    return pos[rand() % counter];
}

void Grid::adj_helper(int x, int y, int * pos, int& counter){
    if (x >= 0 && x < xsize && y >= 0 && y < ysize){
        pos[counter++] = x*ysize + y;
    }
}

void diffuse_helper(double** src, double** dest, int xsize, int ysize, double diff_factor){
    for (int i = 0; i < xsize; i++){
        for (int j = 0; j < ysize; j++)
            dest[i][j] = (1.0- diff_factor) * src[i][j]; //initial
        for (int j = 1; j < ysize; j++)
            dest[i][j] += 0.125 * diff_factor * src[i][j-1]; // shift right
        for (int j = 0 ;  j< ysize-1; j++)
            dest[i][j] += 0.125 * diff_factor *src[i][j+1]; // shift left
    }
    for (int i = 1; i < xsize; i++){
        for (int j = 0; j < ysize; j++)
            dest[i][j] += 0.125 * diff_factor * src[i-1][j]; // shift down
    }
    for (int i = 0; i < ysize-1 ; i++){
        for (int j = 0; j < ysize ; j++)
            dest[i][j] += 0.125 * diff_factor * src[i+1][j]; // shift up
    }
    for (int i = 0; i < xsize -1; i++){
        for(int j = 0; j < ysize-1; j++){
            dest[i][j] += 0.125 * diff_factor * src[i+1][j+1]; // up left
        }
    }
    for (int i = 1; i < xsize; i++){
        for(int j = 1; j < ysize; j++){
            dest[i][j] += 0.125 * diff_factor * src[i-1][j-1]; // down right
        }
    }
    for (int i = 0; i < xsize - 1; i++){
        for(int j = 1; j < ysize; j++){
            dest[i][j] += 0.125 * diff_factor * src[i+1][j-1]; // up right
        }
    }
    for (int i = 1; i < xsize; i++){
        for(int j = 0; j < ysize -1; j++){
            dest[i][j] += 0.125 * diff_factor * src[i-1][j+1]; // down left
        }
    }
}

void Grid::diffuse(double diff_factor) {
    diffuse_helper(glucose, glucose_helper, xsize, ysize, diff_factor);
    double ** temp = glucose;
    glucose = glucose_helper;
    glucose_helper = temp;
    diffuse_helper(oxygen, oxygen_helper, xsize, ysize, diff_factor);
    temp = oxygen;
    oxygen = oxygen_helper;
    oxygen_helper = temp;
}

double distance(int x1, int y1, int x2, int y2){
    int dist_x = x1 - x2;
    int dist_y = y1 - y2;
    return sqrt(dist_x * dist_x + dist_y * dist_y);
}

double conv(double rad, double x){
    double denom = 3.39411;//sqrt(2) * 2.4
    return erf((rad - x)/denom) - erf((-rad - x) / denom);
}


void Grid::irradiate(double dose){
    if (dose == 0)
        return;
    double radius = tumor_radius(xsize / 2, ysize / 2);
    double multiplicator = dose/conv(radius, 0);
    for (int i = 0; i < xsize; i++){
        for (int j = 0; j < ysize; j++){
            double dist = distance(i, j, xsize / 2, ysize / 2);
            if (dist <= 2*radius && cells[i][j].size){
                CellNode * current = cells[i][j].head;
                while (current){
                    current -> cell -> radiate(conv(radius, dist) * multiplicator);
                    current = current -> next;
                }
                int init_count = cells[i][j].size;
                cells[i][j].deleteDeadAndSort();
                change_neigh_counts(i, j, cells[i][j].size - init_count);
            }
        }
    }
}


double Grid::tumor_radius(int center_x, int center_y){
    if (CancerCell::count == 0){
        return -1.0;
    }
    double dist = -1.0;
    for (int i = 0; i < xsize; i++){
        for (int j = 0; j < ysize; j++){
            if (cells[i][j].size > 0 && cells[i][j].head -> type == 'c'){
                int dist_x = i - center_x;
                int dist_y = j - center_y;
                dist = std::max(dist, (double) sqrt(dist_x * dist_x + dist_y * dist_y));
            }
        }
    }
    return dist;
}

int Grid::cell_types(int x, int y){
    return cells[x][y].CellTypeSum();
}

double ** Grid::currentGlucose(){
    return glucose;
}

double ** Grid::currentOxygen(){
    return oxygen;
}