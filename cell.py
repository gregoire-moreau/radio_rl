import util
import random
from deer.base_classes import Environment


quiescent_glucose_level = 17.28
max_glucose_absorption = .72
average_glucose_absorption = .36
average_cancer_glucose_absorption = .54
critical_neighbors = 9
critical_glucose_level = 6.48

class Cell:
    def __init__(self, stage):
        self.age = 0
        self.stage = stage
        self.alive = True
        self.energy = 0
        self.efficiency = 0
        self.transition = 0


class HealthyCell(Cell):
    cell_count = 0

    def __init__(self, stage):
        Cell.__init__(self, stage)
        HealthyCell.cell_count += 1
        self.efficiency = random.normalvariate(average_glucose_absorption, average_glucose_absorption/3)
        self.efficiency = self.efficiency if self.efficiency <= max_glucose_absorption else max_glucose_absorption
        self.transition = random.normalvariate(average_glucose_absorption*11, average_glucose_absorption*(11/3))

    def cycle(self, glucose, count):
        if self.stage == 4:  # Quiescent
            if self.age > 3000:
                self.alive = False
                HealthyCell.cell_count -= 1
                return 0
            else:
                if glucose < critical_glucose_level:
                    self.alive = False
                    HealthyCell.cell_count -= 1
                    return 0
                else:
                    if glucose > quiescent_glucose_level and count < critical_neighbors:
                        self.age = 0
                        self.energy = 0
                        self.stage = 0
                        return self.efficiency * .75
                    else:
                        self.age += 1
                        self.energy += self.efficiency*.75
                        return self.efficiency * .75
        elif self.stage == 3:  # Mitosis
            if glucose < critical_glucose_level:
                self.alive = False
                HealthyCell.cell_count -= 1
                return 0
            else:
                self.energy += self.efficiency
                self.stage = 0
                return self.efficiency, 0
        elif self.stage == 2:  # Gap 2
            if glucose < critical_glucose_level:
                self.alive = False
                HealthyCell.cell_count -= 1
                return 0
            elif self.age == 4:
                self.age = 0
                self.energy = 0
                self.stage = 3
                return self.efficiency
            else:
                self.age += 1
                self.energy += self.efficiency
                return self.efficiency
        elif self.stage == 1:  # Synthesis
            if glucose < critical_glucose_level:
                self.alive = False
                HealthyCell.cell_count -= 1
                return 0
            elif self.age == 8:
                self.age = 0
                self.energy = 0
                self.stage = 2
                return self.efficiency
            else:
                self.age += 1
                self.energy += self.efficiency
                return self.efficiency
        elif self.stage == 0:  # Gap 1
            if self.age == 13 or glucose < critical_glucose_level:
                self.alive = False
                HealthyCell.cell_count -= 1
                return 0
            elif glucose < quiescent_glucose_level or count > critical_neighbors:
                self.age = 0
                self.stage = 4
                self.energy = 0
                return self.efficiency
            else:
                self.energy += self.efficiency
                if self.energy >= self.transition:
                    self.age = 0
                    self.energy = 0
                    self.stage = 1
                else:
                    self.age += 1
                return self.efficiency


class CancerCell(Cell):
    cell_count = 0

    def __init__(self, stage):
        Cell.__init__(self, stage)
        CancerCell.cell_count += 1
        self.efficiency = random.normalvariate(average_cancer_glucose_absorption, average_cancer_glucose_absorption/3)
        self.efficiency = self.efficiency if self.efficiency <= max_glucose_absorption else max_glucose_absorption
        self.transition = random.normalvariate(average_glucose_absorption*11, average_glucose_absorption*(11/3))

    def cycle(self, glucose, count):
        if self.stage == 3:  # Mitosis
            if glucose < critical_glucose_level:
                self.alive = False
                CancerCell.cell_count -= 1
                return 0
            else:
                self.energy += self.efficiency
                self.stage = 0
                return self.efficiency, 1
        elif self.stage == 2:  # Gap 2
            if glucose < critical_glucose_level:
                self.alive = False
                CancerCell.cell_count -= 1
                return 0
            elif self.age == 4:
                self.age = 0
                self.energy = 0
                self.stage = 3
                return self.efficiency
            else:
                self.age += 1
                self.energy += self.efficiency
                return self.efficiency
        elif self.stage == 1:  # Synthesis
            if glucose < critical_glucose_level:
                self.alive = False
                CancerCell.cell_count -= 1
                return 0
            elif self.age == 8:
                self.age = 0
                self.energy = 0
                self.stage = 2
                return self.efficiency
            else:
                self.age += 1
                self.energy += self.efficiency
                return self.efficiency
        elif self.stage == 0:  # Gap 1
            if self.age == 13 or glucose < critical_glucose_level:
                self.alive = False
                CancerCell.cell_count -= 1
                return 0
            else:
                self.energy += self.efficiency
                if self.energy >= self.transition:
                    self.age = 0
                    self.energy = 0
                    self.stage = 1
                else:
                    self.age += 1
                return self.efficiency
