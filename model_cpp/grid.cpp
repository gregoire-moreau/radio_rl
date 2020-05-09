#include <algorithm>
#include "grid.h"
#include <assert.h> 
#include <math.h> 
#include <iostream>


/**
 * Constructor of CellList
 *
 * CellLists are linked lists of CellNodes that are on each pixel of the Grid
 *
 */
CellList::CellList():head(nullptr), tail(nullptr), size(0), oar_count(0), ccell_count(0) {}

/**
 * Destructor of CellList
 *
 */
CellList::~CellList() {
    CellNode * current = head;
    CellNode * next;
    while (current){ // Delete all the CellNodes and Cells in the CellList
        next = current -> next;
        delete current -> cell;
        delete current;
        current = next;
    }
}


/**
 * Add a CellNode containing a cell to the CellList
 *
 * It is added at the start of the list if it is contains a Cancer Cell and at the end otherwise
 *
 * @param newNode The CellNode containing the Cell that we want to add to the CellList
 * @param type The type of the Cell
 */
void CellList::add(CellNode * newNode, char type){
    assert(newNode);
    if (size == 0){
        head = newNode;
        tail = newNode;
        newNode -> next = nullptr;
    }
    else if (type == 'h' || type == 'o'){
        tail -> next = newNode;
        tail = newNode;
        newNode -> next = nullptr;
    } else if(type == 'c'){
        newNode -> next = head;
        head = newNode;
    }
    if (type == 'o')
        oar_count++;
    if (type == 'c')
        ccell_count++;
    size++;
}


/**
 * Create a CellNode container for the Cell and add it to the CellList
 *
 * @param cell The cell that we want to add to the CellList
 * @param type The type of the Cell
 */
void CellList::add(Cell *cell, char type) {
    CellNode * newNode = new CellNode;
    assert(cell);
    newNode -> cell = cell;
    newNode -> type = type;
    add(newNode, type);
}

/**
 * Create a CellNode container for the Cell and add it to the CellList, with the coordinates of the cell on the grid
 *
 * @param cell The cell that we want to add to the CellList
 * @param type The type of the Cell
 * @param x The x coordinate of the cell on the grid
 * @param y The y coordinate of the cell on the grid
 */
void CellList::add(Cell *cell, char type, int x, int y) {
    CellNode * newNode = new CellNode;
    assert(cell);
    newNode -> cell = cell;
    newNode -> type = type;
    newNode -> x = x;
    newNode -> y = y;
    add(newNode, type);
}


/**
 * Go through the CellList by deleting and removing cells that have been killed by lack or nutrients or radiation
 *
 * Ensures that the order of cells (cancer cells first) is kept and that the links stay sound to avoid segfaults
 */
void CellList::deleteDeadAndSort(){
    bool found_head = false; // Used to ensure that we have a head to the list at the end of traversal
    CellNode * current = head;
    CellNode ** previous_next_pointer;
    while(current){
        if (!(current -> cell -> alive)){
            delete current->cell;
            if (current -> type == 'o')
                oar_count--;
            if (current -> type == 'c')
                ccell_count--;
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
    if (!found_head){ // The list is now empty after the traversal
        assert(size == 0);
        head = nullptr;
        tail = nullptr;
    } else{
        tail -> next = nullptr;
    }
}
/**
 * Compute a weighted sum of the cells in this cell list
 *
 * Cancer cells have a weight of -1, healthy cells of 1 and OAR cells have a weight corresponding to the worth assigned
 * to them in the class OARCell
 *
 * @return The weighted sum
 */
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
        else if (current -> type == 'o')
            to_ret += OARCell::worth;
        current = current -> next;
    }
    return to_ret;
}


/**
 * Sets all the OARCells present in this list out of quiescence
 *
 */
void CellList::wake_oar(){
    if (oar_count == 0)
        return;
    CellNode * current = head;
    while(current){
        if (current -> type == 'o')
            current -> cell -> wake();
        current = current -> next;
    }
}


/**
 * Constructor of SourceList
 *
 * A SourceList is a linked list of Source (nutrient sources) objects, which ensures that they are easy to iterate and
 * that we can easily add or remove sources of nutrients to or from the simulation
 */
SourceList::SourceList():head(nullptr), tail(nullptr), size(0) {}


/**
 * Destructor of SourceList
 */
SourceList::~SourceList() {
    Source * current = head;
    Source * next;
    while (current){
        next = current -> next;
        delete current;
        current = next;
    }
}

/**
 * Add a source of nutrients to the SourceList with coordinates (x, y) on the grid
 *
 * @param x The x coordinate of the Source on the grid
 * @param y The y coordinate of the Source on the grid
 */
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

/**
 * Constructor of Grid without an OAR zone
 *
 * The grid is the base of the simulation, it is made out of 3 superimposed 2D layers : one contains the CellLists for
 * each pixel, one contains the glucose amount on each pixel and one contains the oxygen amount on each pixel.
 *
 * @param xsize The number of rows of the grid
 * @param ysize The number of columns of the grid
 * @param sources_num The number of nutrient sources that should be added to the grid
 */
Grid::Grid(int xsize, int ysize, int sources_num):xsize(xsize), ysize(ysize), oar(nullptr){
    cells = new CellList*[xsize];
    glucose = new double*[xsize];
    glucose_helper = new double*[xsize]; // glucose_helper and oxygen_helper are useful to speed up diffusion
    oxygen = new double*[xsize];
    oxygen_helper = new double*[xsize];
    neigh_counts = new int*[xsize];
    for(int i = 0; i < xsize; i++) {
        cells[i] = new CellList[ysize];
        glucose[i] = new double[ysize];
        glucose_helper[i] = new double[ysize];
        std::fill_n(glucose[i], ysize, 100.0); // 1E-6 mg O'Neil
        oxygen[i] = new double[ysize];
        oxygen_helper[i] = new double[ysize];
        std::fill_n(oxygen[i], ysize, 1000.0); // 1 E-6 ml Jalalimanesh
        neigh_counts[i] = new int[ysize]();
    }
    for(int i = 0; i < xsize; i++){
        neigh_counts[i][0] += 3;
        neigh_counts[i][ysize - 1] += 3;
    }
    for(int i = 0; i < ysize; i++){
        neigh_counts[0][i] += 3;
        neigh_counts[xsize - 1][i] += 3;
    }
    neigh_counts[0][0] -= 1;
    neigh_counts[0][ysize -1] -= 1;
    neigh_counts[xsize - 1][0] -= 1;
    neigh_counts[xsize - 1][ysize - 1] -= 1;
    sources = new SourceList();
    for (int i = 0; i < sources_num; i++){
        sources->add(rand() % xsize, rand() % ysize); // Set the sources at random locations on the grid
    }
}


/**
 * Constructor of Grid with an OAR zone
 *
 * The grid is the base of the simulation, it is made out of 3 superimposed 2D layers : one contains the CellLists for
 * each pixel, one contains the glucose amount on each pixel and one contains the oxygen amount on each pixel.
 * The OAR zone is represented by 2 coordinates that thus form a rectangle on the Grid. Every pixel in that rectangle
 * will contain an OARCell
 *
 * @param xsize The number of rows of the grid
 * @param ysize The number of columns of the grid
 * @param sources_num The number of nutrient sources that should be added to the grid
 * @param oar_zone The OARZone object that contains the rectangle's coordinates
 */
Grid::Grid(int xsize, int ysize, int sources_num, OARZone * oar_zone):Grid(xsize, ysize, sources_num){
    oar = oar_zone;
}

/**
 * Destructor of Grid
 *
 */
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

/**
 * Add val to the current "neighbor count" of the pixel at coordinates (x, y) on the grid
 *
 * Neighbor counts are the number of cells on neighbouring pixels, for each pixel. They are useful to check if Healthy
 * Cells need to stay in or enter quiescence, which happens once a certain density has been reached.
 *
 * @param x The x coordinate of the pixel
 * @param y The y coordinate of the pixel
 * @param val The amount that we add to the neighbor count
 */
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

/**
 * Add a cell to a position on the grid
 *
 * @param x The x coordinate where we want to add the cell
 * @param y The y coordinate where we want to add the cell
 * @param ysize The number of columns of the grid
 * @param sources_num The number of nutrient sources that should be added to the grid
 */
void Grid::addCell(int x, int y, Cell *cell, char type) {
    cells[x][y].add(cell, type,x, y);
    change_neigh_counts(x, y, 1);
}

/**
 * Add an amount of glucose and oxygen to each source's pixel, and potentially move them by one pixel
 *
 * The movement only happens on average once a day, and is useful to mimick angiogenesis
 *
 * @param glu The glucose amount that we add to the pixel corresponding to each source
 * @param oxy The oxygen amount that we add to the pixel corresponding to each source
 */
void Grid::fill_sources(double glu, double oxy) {
    Source * current = sources -> head;
    while(current){ // We go through all sources
        glucose[current->x][current->y] += glu;
        oxygen[current->x][current->y] += oxy;
        if ((rand() % 24) < 1){ // The source moves on average once a day
            int newPos = sourceMove(current->x, current->y);
            current -> x = newPos / ysize;
            current -> y = newPos % ysize;
        }
        current = current -> next;
    }
}

/**
 * Find a new position for the source adjacent to its current pixel
 *
 * @param x The current x coordinate of the source
 * @param y The current y coordinate of the source
 * @return An integer corresponding to the new position (ysize * x + y)
 */
int Grid::sourceMove(int x, int y){
    if (rand() % 50000 < CancerCell::count){ // Move towards tumour center
        if (x < center_x)
            x++;
        else if (x > center_x)
            x--;
        if (y < center_y)
            y++;
        else if(y > center_y)
            y--; 
        return x * ysize + y;
    } else{ // Move in random direction
        return rand_adj(x, y);
    }
}


/**
 * Go through all cells on the grid and advance them by one hour in their cycle
 *
 */
void Grid::cycle_cells() { 
    CellList * toAdd = new CellList();
    for (int x = 0; x < xsize * ysize; x++){
        int i = x / ysize; // Coordinates of the pixel
        int j = x % ysize;
        CellNode * current = cells[i][j].head;
        while(current){ // Go through all cells on this pixel
            cell_cycle_res result = current->cell->cycle(glucose[i][j], oxygen[i][j], neigh_counts[i][j] + cells[i][j].size);
            glucose[i][j] -= result.glucose;
            oxygen[i][j] -= result.oxygen;
            if (result.new_cell == 'h'){ //New healthy cell
                int downhill = rand_min(i, j, 5);
                if(downhill >= 0)
                    toAdd -> add(new HealthyCell('1'), 'h', downhill / ysize, downhill % ysize);
                else
                    current -> cell -> sleep();
            }
            if (result.new_cell == 'c'){ // New cancer cell
                int downhill = rand_adj(i, j);
                if(downhill >= 0)
                    toAdd -> add(new CancerCell('1'), 'c', downhill / ysize, downhill % ysize);
            }
            if (result.new_cell == 'o'){ // New oar cell
                int downhill = find_missing_oar(i, j);
                if (downhill >= 0){
                    toAdd -> add(new OARCell('1'), 'o', downhill / ysize, downhill % ysize);
                } else{
                    current -> cell -> sleep();
                }
            }
            if (result.new_cell == 'w'){ // The current cell died because of a lack of nutrients
               wake_surrounding_oar(i, j);
            }
            current = current -> next;
        }
        int init_count = cells[i][j].size; // Number of cells before we check how many died
        cells[i][j].deleteDeadAndSort();
        change_neigh_counts(i, j, cells[i][j].size - init_count);
    }
    addToGrid(toAdd); //Add all new cells to the grid
}

/**
 * Add all the cells in newCells to their pixel's CellList
 *
 * @param newCells The CellList of new cells that we want to add to the grid
 */
void Grid::addToGrid(CellList * newCells){
    CellNode * current = newCells -> head;
    while(current){
        CellNode * next = current -> next;
        cells[current -> x][current -> y].add(current, current -> type);
        current = next;
    }
    newCells -> head = nullptr;
    newCells -> tail = nullptr;
    newCells -> size = 0;
    delete newCells;
}

/**
 * Find neigbouring pixels of lowest cell density and return one of them randomly
 *
 * @param x The x of the pixel around which we are searching
 * @param y The y of the pixel around which we are searching
 * @return An integer corresponding to the pixel coordinates found (ysize * x + y)
 */
int Grid::rand_min(int x, int y, int max){
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

    if (curr_min < max)
        return pos[rand() % counter];
    else
        return -1;
}

/**
 * Helper for rand_min
 *
 * Checks that the coordinates are within the grid's bounds, and adds it to the list of potential positions if it has a
 * cell density lower or equal to the current minimum
 */
void Grid::min_helper(int x, int y, int&  curr_min, int * pos, int& counter){
    if (oar && x >= oar->x1 && x < oar->x2 && y >= oar -> y1 && y < oar -> y2)
        return;
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


/**
 * Find a random neighbouring pixel
 *
 * @param x The x of the pixel around which we are searching
 * @param y The y of the pixel around which we are searching
 * @return An integer corresponding to the pixel coordinates found (ysize * x + y)
 */
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


/**
 * Helper for rand_adj
 *
 * Checks that the coordinates are within the grid's bounds, and adds it to the list of potential positions if it is.
 */
void Grid::adj_helper(int x, int y, int * pos, int& counter){
    if (x >= 0 && x < xsize && y >= 0 && y < ysize){
        pos[counter++] = x*ysize + y;
    }
}

/**
 * Find a random neighbouring pixel that should containt an OARCell but doesn't
 *
 * @param x The x of the pixel around which we are searching
 * @param y The y of the pixel around which we are searching
 * @return An integer corresponding to the pixel coordinates found (ysize * x + y)
 */
int Grid::find_missing_oar(int x, int y){
    int counter = 0;
    int curr_min = 100000;
    int pos[8];

    missing_oar_helper(x-1, y-1, curr_min, pos, counter);
    missing_oar_helper(x-1, y, curr_min, pos, counter);
    missing_oar_helper(x-1, y+1, curr_min, pos, counter);
    missing_oar_helper(x, y-1, curr_min, pos, counter);
    missing_oar_helper(x, y+1, curr_min, pos, counter);
    missing_oar_helper(x+1, y-1, curr_min, pos, counter);
    missing_oar_helper(x+1, y, curr_min, pos, counter);
    missing_oar_helper(x+1, y+1, curr_min, pos, counter);

    return (counter > 0)? pos[rand() % counter] : -1;
}

/**
 * Helper for find_missing_oar
 *
 * Checks that the coordinates are within the OAR zone's bounds, and adds it to the list of potential positions if it
 * doesn't contain an OARCell.
 */
void Grid::missing_oar_helper(int x, int y, int&  curr_min, int * pos, int& counter){
    if (oar && x >= oar->x1 && x < oar->x2 && y >= oar -> y1 && y < oar -> y2  && cells[x][y].oar_count == 0){
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

/**
 * Wake all the OARCells on neighbouring pixels from quiescence
 *
 * @param x The x of the pixel around which we are searching
 * @param y The y of the pixel around which we are searching
 */
void Grid::wake_surrounding_oar(int x, int y){
    wake_helper(x-1, y-1);
    wake_helper(x-1, y);
    wake_helper(x-1, y+1);
    wake_helper(x, y-1);
    wake_helper(x, y+1);
    wake_helper(x+1, y-1);
    wake_helper(x+1, y);
    wake_helper(x+1, y+1);
}

/**
 * Helper for wake_surrounding_oar
 *
 * @param x The x of the pixel on which we want to wake OARCells
 * @param y The y of the pixel on which we want to wake OARCells
 */
void Grid::wake_helper(int x, int y){
    if (oar && x >= oar->x1 && x < oar-> x2 && y >= oar->y1 && y < oar -> y2)
        cells[x][y].wake_oar();
}


/**
 * Helper for diffuse
 *
 * Spreads the float amount of each entry in a 2D array to the neighbouring entries with a factor of diff_factor
 *
 * @param src The 2D array with the initial amounts
 * @param dest The 2D array in which the diffusion will have occurred
 * @param xsize The number of rows of the arrays
 * @param ysize The number of columns of the arrays
 * @param diff_factor The share of each entry's float amount that should be spread to neighbouring pixels
 */
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


/**
 * Diffuse oxygen and glucose on the grid
 *
 * @param diff_factor The share of each pixel's glucose and oxygen that should be spread to neighbouring pixels
 */
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


/**
 * Computes the Euclidean distance between two points
 *
 * @param x1, y1 Coordinates of the first point
 * @param x2, y2 Coordinates of the second point
 * @return The Euclidean distance between the two points
 */
double distance(int x1, int y1, double x2, double y2){
    int dist_x = x1 - x2;
    int dist_y = y1 - y2;
    return sqrt(dist_x * dist_x + dist_y * dist_y);
}


/**
 * Computes the dose depending on the distance to the tumor's center
 *
 * @param rad Radius of the radiation (95 % of the full dose at 1 radius from the center)
 * @param x Distance from the center
 * @return The Euclidean distance between the two points
 */
double conv(double rad, double x){
    double denom = 5.6568;//sqrt(2) * 4
    return erf((rad - x)/denom) - erf((-rad - x) / denom);
}

/**
 * Irradiate cells around a center with a specific dose and radius
 *
 * @param dose The dose of radiation (in grays)
 * @param radius Radius of the radiation (95 % of the full dose at 1 radius from the center)
 * @param center_x The x coordinate of the center of radiation
 * @param center_y The y coordinate of the center of radiation
 */
void Grid::irradiate(double dose, double radius, double center_x, double center_y){
    if (dose == 0) // A dose of 0 is sometimes sent here to signify that the agent has chosen not to irradiate,
        return;
    double multiplicator = dose/conv(radius, 0); // Ensures that we have a max amplitude of dose
    double oer_m = 3.0;
    double k_m = 3.0;
    for (int i = 0; i < xsize; i++){
        for (int j = 0; j < ysize; j++){
            double dist = distance(i, j, center_x, center_y); //Distance of the pixel from the center
            if (dist <= 2*radius && cells[i][j].size){ //If we are more than two radii away, the radiation is negligible
                CellNode * current = cells[i][j].head;
                bool oar_dead = false;
                while (current){
                    double omf = (oxygen[i][j] / 100.0 * oer_m + k_m) / (oxygen[i][j] / 100.0 + k_m) / oer_m; // Include the effect of hypoxia, Powathil formula
                    current -> cell -> radiate(conv(radius, dist) * multiplicator * omf);
                    if (!(current -> cell ->alive) && current->type == 'o'){
                        oar_dead = true;
                    }
                    current = current -> next;
                }
                if(oar_dead) // If an oarcell was killed we pull neighbouring cells out of quiescence to replace it
                    wake_surrounding_oar(i, j);
                int init_count = cells[i][j].size;
                cells[i][j].deleteDeadAndSort();
                change_neigh_counts(i, j, cells[i][j].size - init_count);
            }
        }
    }
}

/**
 * Find the cancer cell most distant from the given center, and return its distance from this center
 *
 * @param center_x The x coordinate of the tumor from which we want to compute the radius
 * @param center_y The y coordinate of the tumor from which we want to compute the radius
 * @return The distance from the cell furthest away from the center to the center
 */
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
    if (dist < 3.0)
        dist = 3.0;
    return 1.1 * dist;
}

/**
 * Compute the weighted sum of cell types for the CellList on position x, y
 */
int Grid::cell_types(int x, int y){
    return cells[x][y].CellTypeSum();
}

/**
 * Returns the type of the first cell on the given position
 *
 * @return 0 if there are no cells on this position, -1 if there is a cancer cell, 1 for a healthy cell and 2 for an OAR cell
 */
int Grid::type_head(int x, int y){
    if (cells[x][y].head){
        char t = cells[x][y].head -> type;
        if (t == 'c'){
            return -1; 
        } else if (t == 'h'){
            return 1;
        } else {
            return 2;
        }
    } else {
        return 0;
    }
}

/**
 * Return the current glucose array
 */
double ** Grid::currentGlucose(){
    return glucose;
}

/**
 * Return the current oxygen array
 */
double ** Grid::currentOxygen(){
    return oxygen;
}

/**
 * Irradiate the tumor present on the grid with the given dose
 */
void Grid::irradiate(double dose){
    compute_center();
    double radius = tumor_radius(center_x, center_y);
    irradiate(dose, radius, center_x, center_y);
}

/**
 * Irradiate the tumor present on the grid with the given dose and radius
 */
void Grid::irradiate(double dose, double radius){
    compute_center();
    irradiate(dose, radius, center_x, center_y);
}

/**
 * Compute the average position of cancer cells on the grid
 */
void Grid::compute_center(){
    int count = 0;
    center_x = 0.0;
    center_y = 0.0;
    for (int i = 0; i < xsize; i++){
        for (int j = 0; j < ysize; j++){
            count += cells[i][j].ccell_count;
            center_x += cells[i][j].ccell_count * i;
            center_y += cells[i][j].ccell_count * j;
        }
    }
    center_x /= count;
    center_y /= count;
}
