#include "cell.h"
#include <random>
#include <iostream>
#include <math.h>

using namespace std;

static float quiescent_glucose_level = 17.28;
static float max_glucose_absorption = .72;
static float average_glucose_absorption = .36;
static float average_cancer_glucose_absorption = .54;
static int critical_neighbors = 9;
static float critical_glucose_level = 6.48;
static float alpha_tumor = 0.38;
static float beta_tumor = 0.038;
static float alpha_norm_tissue = 0.03;
static float beta_norm_tissue = 0.009;
static float repair = 0.1;
static float bystander_rad = 0.05;
static float bystander_survival_probability = 0.95;
static float average_oxygen_consumption = 20.0;
static float max_oxygen_consumption = 40.0;
static float critical_oxygen_level = 360.0;
static float quiescent_oxygen_level = 960.0;

default_random_engine generator (19);
normal_distribution<double> norm_distribution (1.0, 0.3333333);
uniform_real_distribution<double> uni_distribution(0.0, 1.0);

int HealthyCell::count = 0;
int CancerCell::count  = 0;


Cell::Cell(char stage):age(0), stage(stage), alive(true)  {}

HealthyCell::HealthyCell(char stage): Cell(stage) {
    count++;
    double factor = max(min(norm_distribution(generator), 2.0), 0.0);
    glu_efficiency = factor * average_glucose_absorption;
    oxy_efficiency = factor * average_oxygen_consumption;
}

CancerCell::CancerCell(char stage): Cell(stage) {
    count++;
}

cell_cycle_res HealthyCell::cycle(double glucose, double oxygen, int count) {
    cell_cycle_res result = {.oxygen=.0, .glucose=.0, .new_cell='\0'};
    age++;
    if (glucose < critical_glucose_level || oxygen < critical_oxygen_level) {
        alive = false;
        count--;
        return result;
    }
    switch(stage){
        case 'q': //Quiescence
            result.glucose = glu_efficiency * .75;
            result.oxygen  = oxy_efficiency * .75;
            if (glucose > quiescent_glucose_level && count < critical_neighbors && oxygen > quiescent_oxygen_level){
                age = 0;
                stage = '1'; // gap 1
            }
            break;
        case 'm': //Mitosis
            stage = '1';
            age = 0;
            result.glucose = glu_efficiency;
            result.oxygen = oxy_efficiency;
            result.new_cell = 'h';
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
            if (glucose < quiescent_glucose_level || count > critical_neighbors || oxygen < quiescent_oxygen_level){
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

void HealthyCell::radiate(double dose) {
    double survival_probability = exp( - (alpha_norm_tissue * dose) - (beta_norm_tissue * dose * dose));
    if (uni_distribution(generator) < survival_probability){
        alive = false;
        count--;
    }
}

void CancerCell::radiate(double dose) {
    double survival_probability = exp( - (alpha_tumor * dose) - (beta_tumor * dose * dose));
    if (uni_distribution(generator) < survival_probability){
        alive = false;
        count--;
    }
}

cell_cycle_res CancerCell::cycle(double glucose, double oxygen, int count) {
    cell_cycle_res result = {.oxygen=.0, .glucose=.0, .new_cell='\0'};
    age++;
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
            stage = '1';
            age = 0;
            result.glucose = glu_efficiency;
            result.oxygen = oxy_efficiency;
            result.new_cell = 'c';
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