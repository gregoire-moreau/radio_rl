#ifndef RADIO_RL_CELL_H
#define RADIO_RL_CELL_H

typedef struct {
    double glucose;
    double oxygen;
    char new_cell;
} cell_cycle_res;

class Cell {
protected:
    short age;
    short repair;
    char stage;
public:
    bool alive;
    Cell(char stage);
    virtual ~Cell()=default;
    virtual cell_cycle_res cycle(double glucose, double oxygen, int count) = 0;
    virtual void radiate(double dose) = 0;
    void sleep();
    void wake();
};

class HealthyCell : public Cell{
public:
    static int count;
    HealthyCell(char stage);
    //~HealthyCell();
    cell_cycle_res cycle(double glucose, double oxygen, int neigh_count) override;
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
    cell_cycle_res cycle(double glucose, double oxygen, int neigh_count) override;
    void radiate(double dose) override;
};

class OARCell : public Cell{
public:
    static int count;
    static int worth;
    OARCell(char stage);
    //~CancerCell();
    cell_cycle_res cycle(double glucose, double oxygen, int neigh_count) override;
    void radiate(double dose) override;
private:
    double glu_efficiency;
    double oxy_efficiency;
};

#endif //RADIO_RL_CELL_H
