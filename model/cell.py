import random
import math


quiescent_glucose_level = 17.28
max_glucose_absorption = .72
average_glucose_absorption = .36
average_cancer_glucose_absorption = .54
critical_neighbors = 9
critical_glucose_level = 6.48
alpha_tumor = 0.38
beta_tumor = 0.038
alpha_norm_tissue = 0.03
beta_norm_tissue = 0.009
repair = 0.1
bystander_rad = 0.05
bystander_survival_probability = 0.95
average_oxygen_consumption = 20
max_oxygen_consumption = 40
critical_oxygen_level = 360
quiescent_oxygen_level = 960

radiosensitivities = [0.5, 1, 1, 1, 0.25]

class Cell:
    def __init__(self, stage):
        self.age = 0
        self.stage = stage
        self.alive = True
        self.efficiency = 0
        self.oxy_efficiency = 0

    def __lt__(self, other):
        return -self.cell_type() < -other.cell_type()


class HealthyCell(Cell):
    cell_count = 0

    def __init__(self, stage):
        Cell.__init__(self, stage)
        HealthyCell.cell_count += 1
        factor = random.normalvariate(1, 1/3)
        factor = max(0, min(2, factor))
        self.efficiency = average_glucose_absorption * factor
        self.oxy_efficiency = average_oxygen_consumption * factor

    # Simulate an hour of the cell cycle
    def cycle(self, glucose, count, oxygen):
        self.age += 1
        if glucose < critical_glucose_level or oxygen < critical_oxygen_level:
            self.alive = False
            HealthyCell.cell_count -= 1
            return 0, 0
        elif self.stage == 4:  # Quiescent
            if glucose > quiescent_glucose_level and count < critical_neighbors and oxygen > quiescent_oxygen_level:
                self.age = 0
                self.stage = 0
            return self.efficiency * .75, self.oxy_efficiency * .75
        elif self.stage == 3:  # Mitosis
            self.stage = 0
            self.age = 0
            return self.efficiency, self.oxy_efficiency, 0
        elif self.stage == 2:  # Gap 2
            if self.age == 4:
                self.age = 0
                self.stage = 3
            return self.efficiency, self.oxy_efficiency
        elif self.stage == 1:  # Synthesis
            if self.age == 8:
                self.age = 0
                self.stage = 2
            return self.efficiency, self.oxy_efficiency
        elif self.stage == 0:  # Gap 1
            if glucose < quiescent_glucose_level or count > critical_neighbors or oxygen < quiescent_oxygen_level:
                self.age = 0
                self.stage = 4
            elif self.age == 11:
                    self.age = 0
                    self.stage = 1
            return self.efficiency, self.oxy_efficiency

    def radiate(self, dose):
        survival_probability = math.exp(radiosensitivities[self.stage] * (-alpha_norm_tissue*dose - beta_norm_tissue * (dose ** 2)))
        if random.random() > survival_probability:
            self.alive = False
            HealthyCell.cell_count -= 1

    def cell_color(self):
        return 0, 102, 204

    def cell_type(self):
        return -1


class CancerCell(Cell):
    cell_count = 0
    center = (0, 0)

    def __init__(self, stage, x, y):
        Cell.__init__(self, stage)
        CancerCell.cell_count += 1

    def radiate(self, dose):
        survival_probability = math.exp(radiosensitivities[self.stage] * (-alpha_tumor*dose - beta_tumor * (dose ** 2)))
        if random.random() > survival_probability:
            self.alive = False
            CancerCell.cell_count -= 1

    # Simulate an hour of the cell cycle
    def cycle(self, glucose, count, oxygen):
        if glucose < critical_glucose_level or oxygen < critical_oxygen_level:
            self.alive = False
            CancerCell.cell_count -= 1
            return 0, 0
        factor = random.normalvariate(1, 1 / 3)
        factor = 2 if factor > 2 else factor
        self.efficiency = average_cancer_glucose_absorption * factor
        self.oxy_efficiency = average_oxygen_consumption * factor
        self.age += 1
        if self.stage == 3:  # Mitosis
            self.stage = 0
            self.age = 0
            return self.efficiency, self.oxy_efficiency, 1
        elif self.stage == 2:  # Gap 2
            if self.age == 4:
                self.age = 0
                self.stage = 3
            return self.efficiency, self.oxy_efficiency
        elif self.stage == 1:  # Synthesis
            if self.age == 8:
                self.age = 0
                self.stage = 2
            return self.efficiency, self.oxy_efficiency
        elif self.stage == 0:  # Gap 1
            if self.age == 11:
                self.age = 0
                self.stage = 1
            return self.efficiency, self.oxy_efficiency

    def cell_color(self):
        return 104, 24, 24

    def cell_type(self):
        return 1


class OARCell(Cell):
    cell_count = 0
    worth = 5

    def __init__(self, stage, worth):
        OARCell.cell_count += 1
        Cell.__init__(self, stage)
        OARCell.worth = worth

    # One hour of cell cycle
    def cycle(self, glucose, count, oxygen):
        self.age += 1
        if glucose < critical_glucose_level or oxygen < critical_oxygen_level:
            self.alive = False
            OARCell.cell_count -= 1
            return 0, 0, 2
        elif self.stage == 4:  # Quiescent
            return self.efficiency * .75, self.oxy_efficiency * .75
        elif self.stage == 3:  # Mitosis
            self.stage = 0
            self.age = 0
            return self.efficiency, self.oxy_efficiency, 3
        elif self.stage == 2:  # Gap 2
            if self.age == 4:
                self.age = 0
                self.stage = 3
            return self.efficiency, self.oxy_efficiency
        elif self.stage == 1:  # Synthesis
            if self.age == 8:
                self.age = 0
                self.stage = 2
            return self.efficiency, self.oxy_efficiency
        elif self.stage == 0:  # Gap 1
            if glucose < quiescent_glucose_level or count > critical_neighbors or oxygen < quiescent_oxygen_level:
                self.age = 0
                self.stage = 4
            elif self.age == 11:
                self.age = 0
                self.stage = 1
            return self.efficiency, self.oxy_efficiency

    def cell_color(self):
        return 255, 255, 153

    def cell_type(self):
        return -OARCell.worth

    def radiate(self, dose):
        survival_probability = math.exp(radiosensitivities[self.stage] * (-alpha_norm_tissue*dose - beta_norm_tissue * (dose ** 2)))
        if random.random() > survival_probability:
            self.alive = False
            OARCell.cell_count -= 1
