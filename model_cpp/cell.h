//
// Created by grego on 08/01/2020.
//

#ifndef RADIO_RL_CELL_H
#define RADIO_RL_CELL_H

typedef struct {
    double glucose;
    double oxygen;
    char new_cell;
} cell_cycle_res;

class Cell {
public:
    bool alive;
    Cell(char stage);
    virtual ~Cell()=default;
    virtual cell_cycle_res cycle(double glucose, double oxygen, int count) = 0;
    virtual void radiate(double dose) = 0;

protected:
    short age;
    char stage;

};

class HealthyCell : public Cell{
public:
    static int count;
    HealthyCell(char stage);
    //~HealthyCell();
    cell_cycle_res cycle(double glucose, double oxygen, int count) override;
    void radiate(double dose) override;
private:
    double glu_efficiency;
    double oxy_efficiency;
};

class CancerCell : public Cell{
public:
    static int count;
    CancerCell(char stage);
    //~CancerCell();
    cell_cycle_res cycle(double glucose, double oxygen, int count) override;
    void radiate(double dose) override;
};

#endif //RADIO_RL_CELL_H
