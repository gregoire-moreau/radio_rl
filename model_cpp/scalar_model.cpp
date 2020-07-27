#include "scalar_model.h"
#include <stdlib.h>
#include <math.h>
#include <iostream>
#include <fstream>
#include <string>
#include <random>

using namespace std;
default_random_engine generator2(5);
uniform_real_distribution<double> uni_distribution2(0.0, 1.0);

ScalarModel::ScalarModel(char reward): reward(reward), cancer_cells(nullptr), healthy_cells(nullptr), time(0), glucose(0.0), oxygen(0.0), end_type('0'), init_hcell_count(0){
}

ScalarModel::~ScalarModel(){
    delete cancer_cells;
    delete healthy_cells;
}

void ScalarModel::reset(){
    delete cancer_cells;
    delete healthy_cells;
    HealthyCell::count = 0;
    CancerCell::count = 0;
    time = 0;
    glucose = 250000.0;
    oxygen = 2500000.0;
    healthy_cells = new CellList();
    cancer_cells = new CellList();
    for(int i = 0; i < 1000; i++)
        healthy_cells -> add(new HealthyCell('1'), 'h');
    cancer_cells -> add(new CancerCell('1'), 'c');
    go(350);
    init_hcell_count = HealthyCell::count;
}

void ScalarModel::cycle_cells(){
    int hcell_count = HealthyCell::count;
    int ccell_count = CancerCell::count;
    int count = hcell_count + ccell_count;
    CellNode * current_h = healthy_cells -> head;
    CellNode * current_c = cancer_cells -> head;
    CellNode * current;
    while(hcell_count > 0 || ccell_count > 0){
        if (rand() % (hcell_count + ccell_count) < ccell_count){
            ccell_count--;
            current = current_c;
            current_c = current_c -> next;
        } else {
            hcell_count--;
            current = current_h;
            current_h = current_h -> next;
        }
        cell_cycle_res result = current->cell->cycle(glucose, oxygen, count / 278);
        glucose -= result.glucose;
        oxygen -= result.oxygen;
        if (result.new_cell == 'h') //New healthy cell
            healthy_cells -> add(new HealthyCell('1'), 'h');
        else if (result.new_cell == 'c') // New cancer cell
            cancer_cells -> add(new CancerCell('1'), 'c');
    }
    healthy_cells -> deleteDeadAndSort();
    cancer_cells -> deleteDeadAndSort();
}

void ScalarModel::fill_sources(){
    glucose += 13000.0;
    oxygen += 450000.0;
}

void ScalarModel::go(int i){
    for(int x = 0; x < i; x++){
        time++;
        fill_sources();
        cycle_cells();
    }
}

void ScalarModel::irradiate(int dose){
    CellNode * current_h = healthy_cells -> head;
    while(current_h){
        current_h -> cell -> radiate(dose);
        current_h = current_h -> next;
    }
    healthy_cells -> deleteDeadAndSort();
    CellNode * current_c = cancer_cells -> head;
    while(current_c){
        current_c -> cell -> radiate(dose);
        current_c = current_c -> next;
    }
    cancer_cells -> deleteDeadAndSort();
}

double ScalarModel::act(int action){
    int dose = action + 1;
    int pre_hcell = HealthyCell::count;
    int pre_ccell = CancerCell::count;
    irradiate(dose);
    int m_hcell = HealthyCell::count;
    int m_ccell = CancerCell::count;
    go(24);
    int post_hcell = HealthyCell::count;
    int post_ccell = CancerCell::count;
    return adjust_reward(dose, pre_ccell - post_ccell, pre_hcell-min(post_hcell, m_hcell));
}

double ScalarModel::adjust_reward(int dose, int ccell_killed, int hcells_lost){
    if (inTerminalState()){
        if (end_type == 'L' || end_type == 'T'){
            return -1.0;
        } else{
            if (reward == 'd')
                return - (double) dose / 400.0 + 0.5 - (double) (init_hcell_count - HealthyCell::count) / 3000.0;
            else
                return 0.5 - (double) (init_hcell_count - HealthyCell::count) / 3000.0;
        }
    } else {
        if (reward == 'd')
            return - (double) dose / 400.0 + (double) (ccell_killed - 5 * hcells_lost)/100000.0;
        else if (reward == 'k')
            return (double) (ccell_killed - 5 * hcells_lost)/100000.0;
    }
}

bool ScalarModel::inTerminalState(){
    if (CancerCell::count <= 0){
        end_type = 'W';
        return true;
    } else if (HealthyCell::count < 10){
        end_type = 'L';
        return true;
    } else if (time > 1550){
        end_type = 'T';
        return true;
    } else {
        return false;
    }
}

TabularAgent::TabularAgent(ScalarModel * env, int cancer_cell_stages, int healthy_cell_stages, int actions): env(env), cancer_cell_stages(cancer_cell_stages), healthy_cell_stages(healthy_cell_stages), actions(actions){
    Q_values = new double*[cancer_cell_stages * healthy_cell_stages];
    for(int i = 0; i < cancer_cell_stages * healthy_cell_stages; i++){
        Q_values[i] = new double[actions];
        fill_n(Q_values[i], actions, 0.0);
    }
    log_base_hcells = exp(log(4000.0) / ((double) healthy_cell_stages - 1.0));
    log_base_ccells = exp(log(40000.0) / ((double) cancer_cell_stages - 1.0));
}

TabularAgent::~TabularAgent(){
    for(int i = 0; i < cancer_cell_stages * healthy_cell_stages; i++){
        delete[] Q_values[i];
    }
    delete[] Q_values;
}

int TabularAgent::state(){
    int ccell_state = min(cancer_cell_stages - 1, (int) floor(log(CancerCell::count + 1) / log(log_base_ccells)));
    int hcell_state = min(healthy_cell_stages - 1, (int) floor(log(HealthyCell::count + 1) / log(log_base_hcells)));
    return ccell_state * cancer_cell_stages + hcell_state;
}

int TabularAgent::choose_action(int state, double epsilon){
    if(uni_distribution2(generator2) < epsilon) {
        return rand() % 4;
    } else {
        int max_ind = -1;
        double max_val = - 999999.0;
        for(int i = 0; i < actions; i++){
            if(max_val > Q_values[state][i]) {
                max_val = Q_values[state][i];
                max_ind = i;
            }
        }
        return max_ind;
    }
}

void TabularAgent::train(int steps, double alpha, double epsilon){
    env -> reset();
    while(steps > 0){
        while (!env->inTerminalState() && steps > 0){
            int obs = state();
            int action = choose_action(obs, epsilon);
            double r = env->act(action);
            int new_obs = state();
            double max_val = - 99999.0;
            for(int i = 0; i < actions; i++){
                if(Q_values[new_obs][i] > max_val)
                    max_val = Q_values[new_obs][i];
            }
            Q_values[obs][action] = (1.0 - alpha) * Q_values[obs][action] + alpha * (r + max_val);
            steps--;
        }
        if(steps > 0)
            env -> reset();
    }
}

void TabularAgent::test(int steps, bool verbose){
    double sum_r = 0.0;
    int count = steps;
    env -> reset();
    while(steps > 0){
        while (!env->inTerminalState() && steps > 0){
            int obs = state();
            int action = choose_action(obs, 0.0);
            if (verbose)
                cout << action + 1 << " grays" << endl;
            sum_r += env -> act(action);
            steps--;
        }
        if(steps > 0){
            if(verbose)
                cout << env -> end_type << endl;
            env -> reset();
        }
    }
    cout << "Average reward " << sum_r / (double) count << endl;
}

void TabularAgent::run(int n_epochs, int train_steps, int test_steps, double init_alpha, double alpha_mult, double init_epsilon, double end_epsilon){
    test(test_steps, false);
    double alpha = init_alpha;
    double epsilon = init_epsilon;
    double epsilon_change = (double) (init_epsilon - end_epsilon) / (double) (n_epochs - 1);
    for(int i = 0; i < n_epochs; i++){
        cout << "Epoch " << i + 1 << endl;
        train(train_steps, alpha, epsilon);
        test(test_steps, false);
        alpha *= alpha_mult;
        epsilon -= epsilon_change;
    }
}

void TabularAgent::save_Q(string name){
    ofstream myfile;
    myfile.open(name);
    myfile << cancer_cell_stages << " " << healthy_cell_stages << " " << actions << "\n";
    for(int i = 0; i < cancer_cell_stages * healthy_cell_stages; i++){
        for(int j = 0; j < actions; j++){
            myfile << Q_values[i][j] << ", ";
        }
        myfile << "\n";
    }
    myfile.close();
}

int main(int argc, char * argv[]){
    ScalarModel * model_killed = new ScalarModel('k');
    TabularAgent * agent_killed = new TabularAgent(model_killed, 50, 5, 4);
    agent_killed -> run(stoi(argv[1]), 2500, 500, 0.8, 0.5, 0.8, 0.01);
    agent_killed -> test(100, true);
    agent_killed -> save_Q("qvals_killed.csv");
    delete model_killed;
    delete agent_killed;

    ScalarModel * model_dose = new ScalarModel('d');
    TabularAgent * agent_dose = new TabularAgent(model_dose, 50, 5, 4);
    agent_dose -> run(stoi(argv[1]), 2500, 500, 0.8, 0.5, 0.8, 0.01);
    agent_dose -> test(100, true);
    agent_dose -> save_Q("qvals_dose.csv");
    delete model_dose;
    delete agent_dose;
}
