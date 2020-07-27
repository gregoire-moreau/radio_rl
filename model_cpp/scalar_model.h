#ifndef RADIO_RL_SCALAR_MODEL_H
#define RADIO_RL_SCALAR_MODEL_H

#include <string>
#include "cell.h"
#include "grid.h"

class ScalarModel{
public:
    ScalarModel(char reward);
    ~ScalarModel();
    void reset();
    double act(int action);
    bool inTerminalState();
    char end_type;
private:
    char reward;
    CellList * cancer_cells;
    CellList * healthy_cells;
    int time;
    double glucose;
    double oxygen;
    int init_hcell_count;
    void cycle_cells();
    void fill_sources();
    void go(int i);
    void irradiate(int dose);
    double adjust_reward(int dose, int ccell_killed, int hcells_lost);
};

class TabularAgent{
public:
    TabularAgent(ScalarModel * env, int cancer_cell_stages, int healthy_cell_stages, int actions);
    ~TabularAgent();
    void train(int steps, double alpha, double epsilon);
    void test(int steps, bool verbose);
    void run(int n_epochs, int train_steps, int test_steps, double init_alpha, double alpha_mult, double init_epsilon, double end_epsilon);
    void save_Q(std::string name);
private:
    ScalarModel * env;
    int cancer_cell_stages;
    int healthy_cell_stages;
    int actions;
    double ** Q_values;
    double log_base_hcells;
    double log_base_ccells;
    int state();
    int choose_action(int state, double epsilon);
};

#endif
