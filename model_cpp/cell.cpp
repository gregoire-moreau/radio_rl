#include "cell.h"
#include <random>
#include <iostream>
#include <math.h>

using namespace std;

static float quiescent_glucose_level = 17.28; // 1.728 E-7 mg/cell O'Neil
//static float max_glucose_absorption = .72; //
static float average_glucose_absorption = .36; // 3.6E-9 mg/cell/hour O'Neil
static float average_cancer_glucose_absorption = .54; // 5.4 E-9 mg/cell/hour O'Neil
static int critical_neighbors = 9; // Density to get one cell per pixel, O'Neil
static float critical_glucose_level = 6.48; //6.48 E-8 mg/cell O'Neil
static float alpha_tumor = 0.3; // Powathil
static float beta_tumor = 0.03; // Powathil
static float alpha_norm_tissue = 0.15;
static float beta_norm_tissue = 0.03;
static float alpha_oar = 0.03;
static float beta_oar = 0.009;
static int repair_time = 9;
static float average_oxygen_consumption = 20.0; // 2.16 E-9 ml/cell/hour Jalalimanesh
//static float max_oxygen_consumption = 40.0; // 4.32 E-9 ml/cell/hour Jalalimanesh
static float critical_oxygen_level = 360.0; // 3.88 E-8 ml/cell/hour Jalalimanesh
static float quiescent_oxygen_level = 960.0; // 10.37 E-8 ml/cell/hour Jalalimanesh

default_random_engine generator(5);
normal_distribution<double> norm_distribution (1.0, 0.3333333);
uniform_real_distribution<double> uni_distribution(0.0, 1.0);

int HealthyCell::count = 0;
int CancerCell::count  = 0;
int OARCell::count     = 0;
int OARCell::worth     = 5;


/**
 * Constructor of the abstract class Cell
 *
 * @param stage Current stage of the cell in the cell cycle
 */
Cell::Cell(char stage):age(0), stage(stage), alive(true), repair(0)  {}

/**
 * Sets a cell's stage to "quiescent" and resets its time counter
 */
void Cell::sleep(){
    stage = 'q';
    age = 0;
}


/**
 * Sets a cell's stage to Gap 1 and resets its time counter
 */
void Cell::wake(){
    if (stage == 'q'){
        stage = '1';
        age = 0;
    }
}

/**
 * Constructor of the class HealthyCell, representing normal tissue in the tumor proliferation model
 *
 * @param stage Current stage of the cell in the cell cycle
 */
HealthyCell::HealthyCell(char stage): Cell(stage) {
    count++;
    double factor = max(min(norm_distribution(generator), 2.0), 0.0);
    glu_efficiency = factor * average_glucose_absorption;
    oxy_efficiency = factor * average_oxygen_consumption;
    alive = true;
}


/**
 * Constructor of the class CancerCell, representing tumoral tissue in the tumor proliferation model
 *
 * @param stage Current stage of the cell in the cell cycle
 */
CancerCell::CancerCell(char stage): Cell(stage) {
    count++;
    alive = true;
}

/**
 * Constructor of the class OARCell, representing an Organ At Risk in the tumor proliferation model
 *
 * @param stage Current stage of the cell in the cell cycle
 */
OARCell::OARCell(char stage) : Cell(stage) {
    count++;
    double factor = max(min(norm_distribution(generator), 2.0), 0.0);
    glu_efficiency = factor * average_glucose_absorption;
    oxy_efficiency = factor * average_oxygen_consumption;
    alive = true;
}


/**
 * Simulates one hour of the cell cycle for a healthy cell
 *
 * Verifies that the cell has enough nutrients (otherwise it dies), and advances the cell one hour in the cycle,
 * changing its stage if necessary.
 *
 * @param glucose Amount of glucose available to the cell
 * @param oxygen Amount of oxygen available to the cell
 * @param neigh_count Number of cells in neigbouring pixels on the grid
 * @return A cell_cycle_res object that contains the amount of glucose and oxygen consumed as well as a character that
 *         indicates if a new healthy cell has to be created and its type.
 */
cell_cycle_res HealthyCell::cycle(double glucose, double oxygen, int neigh_count) {
    cell_cycle_res result = {.0,.0,'\0'};
    if(repair == 0)
        age++;
    else
        repair--;
    if (glucose < critical_glucose_level || oxygen < critical_oxygen_level) { //Check if the cell will survive this hour
        alive = false;
        count--;
        return result;
    }
    switch(stage){
        case 'q': //Quiescence
            result.glucose = glu_efficiency * .75;
            result.oxygen  = oxy_efficiency * .75;
            if (glucose > quiescent_glucose_level && neigh_count < critical_neighbors && oxygen > quiescent_oxygen_level){
                age = 0;
                stage = '1'; // gap 1
            }
            break;
        case 'm': //Mitosis
            if (age == 1){
                stage = '1';
                age = 0;
                result.new_cell = 'h';
            }
            result.glucose = glu_efficiency;
            result.oxygen = oxy_efficiency;
            break;
        case '2': //Gap 2
            result.glucose = glu_efficiency;
            result.oxygen = oxy_efficiency;
            if (age == 4){
                age = 0;
                stage = 'm';
            }
            break;
        case 's': //Synthesis
            result.glucose = glu_efficiency;
            result.oxygen = oxy_efficiency;
            if (age == 8){
                age = 0;
                stage = '2';
            }
            break;
        case '1': //Gap 1
            result.glucose = glu_efficiency;
            result.oxygen = oxy_efficiency;
            if (glucose < quiescent_glucose_level || neigh_count >= critical_neighbors || oxygen < quiescent_oxygen_level){
                age = 0;
                stage = 'q';
            } else if(age >= 11) {
                age = 0;
                stage = 's';
            }
            break;
        default:
            cout << "INCORRECT CELL STAGE " << stage << endl;
            break;
    }
    return result;
}

/**
 * Simulates the effect of radiation on a  HealthyCell
 *
 * Uses a modified LQ model to probabilistically decide if the cell survives or not to the radiation
 *
 * @param dose Radiation dose in grays
 */
void HealthyCell::radiate(double dose) {
    float radio_gamma = 0.0;
    switch (stage){
        case '2':
            radio_gamma = 1.25;
            break;
        case 'm':
            radio_gamma = 1.25;
            break;
        case '1':
            radio_gamma = 1.0;
            break;
        case 'q':
            radio_gamma = 0.75;
            break;
        case 's':
            radio_gamma = 0.75;
            break;
        default:
            radio_gamma = 1.0;
            break;
    }
    double survival_probability = exp(radio_gamma * ( - (alpha_norm_tissue * dose) - (beta_norm_tissue * dose * dose)));
    if (uni_distribution(generator) > survival_probability){
        alive = false;
        count--;
    } else if (dose > 0.5){
        repair += (int) round(2.0 * uni_distribution(generator) * (double) repair_time );
    }
}


/**
 * Simulates the effect of radiation on a CancerCell
 *
 * Uses a modified LQ model to probabilistically decide if the cell survives or not to the radiation
 *
 * @param dose Radiation dose in grays
 */
void CancerCell::radiate(double dose) {
    float radio_gamma = 0.0;
    switch (stage){
        case '2':
            radio_gamma = 1.25;
            break;
        case 'm':
            radio_gamma = 1.25;
            break;
        case '1':
            radio_gamma = 1.0;
            break;
        case 's':
            radio_gamma = 0.75;
            break;
        default:
            radio_gamma = 1.0;
            break;
    }
    double survival_probability = exp(radio_gamma *  (- (alpha_tumor * dose) - (beta_tumor * dose * dose)));
    if (uni_distribution(generator) > survival_probability){
        alive = false;
        count--;
    } else if (dose > 0.5){
        repair += (int) round(2.0 * uni_distribution(generator) * (double) repair_time );
    }
}


/**
 * Simulates one hour of the cell cycle for a cancer cell
 *
 * Verifies that the cell has enough nutrients (otherwise it dies), and advances the cell one hour in the cycle,
 * changing its stage if necessary.
 *
 * @param glucose Amount of glucose available to the cell
 * @param oxygen Amount of oxygen available to the cell
 * @param neigh_count Number of cells in neigbouring pixels on the grid
 * @return A cell_cycle_res object that contains the amount of glucose and oxygen consumed as well as a character that
 *         indicates if a new cancer cell has to be created
 */
cell_cycle_res CancerCell::cycle(double glucose, double oxygen, int neigh_count) {
    cell_cycle_res result = {.0, .0, '\0'};
    if(repair == 0)
        age++;
    else
        repair--;
    if (glucose < critical_glucose_level || oxygen < critical_oxygen_level) {
        alive = false;
        count--;
        return result;
    }
    double factor = max(min(norm_distribution(generator), 2.0), 0.0);
    double glu_efficiency = factor * average_cancer_glucose_absorption;
    double oxy_efficiency = factor * average_oxygen_consumption;
    switch(stage){
        case 'm': //Mitosis
            if(age == 1){
                stage = '1';
                age = 0;
                result.new_cell = 'c';
            }
            result.glucose = glu_efficiency;
            result.oxygen = oxy_efficiency;
            break;
        case '2': //Gap 2
            result.glucose = glu_efficiency;
            result.oxygen = oxy_efficiency;
            if (age >= 4){
                age = 0;
                stage = 'm';
            }
            break;
        case 's': //Synthesis
            result.glucose = glu_efficiency;
            result.oxygen = oxy_efficiency;
            if (age >= 8){
                age = 0;
                stage = '2';
            }
            break;
        case '1': //Gap 1
            result.glucose = glu_efficiency;
            result.oxygen = oxy_efficiency;
            if(age >= 11) {
                age = 0;
                stage = 's';
            }
            break;
        default:
            cout << "INCORRECT CELL STAGE " << stage << endl;
            break;
    }
    return result;
}

/**
 * Simulates one hour of the cell cycle for an OAR cell
 *
 * Verifies that the cell has enough nutrients (otherwise it dies), and advances the cell one hour in the cycle,
 * changing its stage if necessary.
 *
 * @param glucose Amount of glucose available to the cell
 * @param oxygen Amount of oxygen available to the cell
 * @param neigh_count Number of cells in neigbouring pixels on the grid
 * @return A cell_cycle_res object that contains the amount of glucose and oxygen consumed as well as a character that
 *         indicates if a new OAR cell has to be created
 */
cell_cycle_res OARCell::cycle(double glucose, double oxygen, int neigh_count) {
    cell_cycle_res result = {.0,.0,'\0'};
    age++;
    if (glucose < critical_glucose_level || oxygen < critical_oxygen_level) {
        alive = false;
        count--;
        result.new_cell = 'w';
        return result;
    }
    switch(stage){
        case 'q': //Quiescence
            result.glucose = glu_efficiency * .75;
            result.oxygen  = oxy_efficiency * .75;
            break;
        case 'm': //Mitosis
            stage = '1';
            age = 0;
            result.glucose = glu_efficiency;
            result.oxygen = oxy_efficiency;
            result.new_cell = 'o';
            break;
        case '2': //Gap 2
            result.glucose = glu_efficiency;
            result.oxygen = oxy_efficiency;
            if (age == 4){
                age = 0;
                stage = 'm';
            }
            break;
        case 's': //Synthesis
            result.glucose = glu_efficiency;
            result.oxygen = oxy_efficiency;
            if (age == 8){
                age = 0;
                stage = '2';
            }
            break;
        case '1': //Gap 1
            result.glucose = glu_efficiency;
            result.oxygen = oxy_efficiency;
            if (glucose < quiescent_glucose_level || neigh_count > critical_neighbors || oxygen < quiescent_oxygen_level){
                age = 0;
                stage = 'q';
            } else if(age >= 11) {
                age = 0;
                stage = 's';
            }
            break;
        default:
            cout << "INCORRECT CELL STAGE " << stage << endl;
            break;
    }
    return result;
}

/**
 * Simulates the effect of radiation on a OARCell
 *
 * Uses a modified LQ model to probabilistically decide if the cell survives or not to the radiation
 *
 * @param dose Radiation dose in grays
 */
void OARCell::radiate(double dose) {
    float radio_gamma = 0.0;
    switch (stage){
        case '1':
            radio_gamma = 0.5;
            break;
        case 'q':
            radio_gamma = 0.25;
            break;
        default:
            radio_gamma = 1.0;
            break;
    }
    double survival_probability = exp(radio_gamma * ( - (alpha_norm_tissue * dose) - (beta_norm_tissue * dose * dose)));
    if (uni_distribution(generator) > survival_probability){
        alive = false;
        count--;
    }
}