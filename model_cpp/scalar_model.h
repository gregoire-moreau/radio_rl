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
    void go(int hours);
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
    void irradiate(int dose);
    double adjust_reward(int dose, int ccell_killed, int hcells_lost);
};

class TabularAgent{
public:
    TabularAgent(ScalarModel * env, int cancer_cell_stages, int healthy_cell_stages, int actions, char state_type);
    ~TabularAgent();
    void train(int steps, double alpha, double epsilon, double disc_factor);
    void test(int episodes, bool verbose, double disc_factor, bool eval);
    void run(int n_epochs, int train_steps, int test_steps, double init_alpha, double alpha_mult, double init_epsilon, double end_epsilon, double disc_factor);
    void save_Q(std::string name);
    void load_Q(std::string name);
    void treatment_var(int count);
    void change_val(int state, int action, double val);
private:
    ScalarModel * env;
    int cancer_cell_stages;
    int healthy_cell_stages;
    int actions;
    char state_type;
    double ** Q_values;
    double state_helper_hcells;
    double state_helper_ccells;
    int state();
    int choose_action(int state, double epsilon);
};

#endif
