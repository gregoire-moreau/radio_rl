import random
import math


quiescent_glucose_level = 17.28
average_glucose_absorption = .36
average_cancer_glucose_absorption = .54
critical_neighbors = 9
critical_glucose_level = 6.48
alpha_tumor = 0.3
beta_tumor = 0.03
alpha_norm_tissue = 0.15
beta_norm_tissue = 0.03
repair_time = 9
average_oxygen_consumption = 20
critical_oxygen_level = 360
quiescent_oxygen_level = 960

radiosensitivities = [1, .75, 1.25, 1.25, .75]


class Cell:
    """Superclass of the different types of cells in the model."""

    def __init__(self, stage):
        """Constructor of Cell."""
        self.age = 0
        self.stage = stage
        self.alive = True
        self.efficiency = 0
        self.oxy_efficiency = 0
        self.repair = 0

    def __lt__(self, other):
        """Used to allow sorting of Cell lists"""
        return -self.cell_type() < -other.cell_type()


class HealthyCell(Cell):
    """HealthyCells are cells representing healthy tissue in the model."""
    cell_count = 0

    def __init__(self, stage):
        """Constructor of a HealthyCell."""
        Cell.__init__(self, stage)
        HealthyCell.cell_count += 1
        factor = random.normalvariate(1, 1/3)
        factor = max(0, min(2, factor))
        self.efficiency = average_glucose_absorption * factor
        self.oxy_efficiency = average_oxygen_consumption * factor

    def cycle(self, glucose, count, oxygen):
        """Simulate an hour of the cell cycle."""
        if glucose < critical_glucose_level or oxygen < critical_oxygen_level:
            self.alive = False
            HealthyCell.cell_count -= 1
            return 0, 0
        if self.repair == 0:
            self.age += 1
        else:
            self.repair -= 1
        if self.stage == 4:  # Quiescent
            if glucose > quiescent_glucose_level and count < critical_neighbors and oxygen > quiescent_oxygen_level:
                self.age = 0
                self.stage = 0
            return self.efficiency * .75, self.oxy_efficiency * .75
        elif self.stage == 3:  # Mitosis
            if self.age == 1:
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
        """Irradiate this cell with a specific dose"""
        survival_probability = math.exp(radiosensitivities[self.stage] * (-alpha_norm_tissue*dose - beta_norm_tissue * (dose ** 2)))
        if random.uniform(0, 1) > survival_probability:
            self.alive = False
            HealthyCell.cell_count -= 1
        elif dose > 0.5:
            self.repair += int(round(random.uniform(0, 2) * repair_time))

    def cell_color(self):
        """RGB for the cell's color"""
        return 0, 102, 204

    def cell_type(self):
        """Return 1, the type of the cell to sort cell lists and compare them"""
        return 1


class CancerCell(Cell):
    """CancerCells are cells representing tumoral tissue in the model."""
    cell_count = 0

    def __init__(self, stage):
        """Constructor of CancerCell."""
        Cell.__init__(self, stage)
        CancerCell.cell_count += 1

    def radiate(self, dose):
        """Irradiate this cell with a specific dose."""
        survival_probability = math.exp(radiosensitivities[self.stage] * (-alpha_tumor*dose - beta_tumor * (dose ** 2)))
        if random.random() > survival_probability:
            self.alive = False
            CancerCell.cell_count -= 1
        elif dose > 0.5:
            self.repair += int(round(random.uniform(0, 2) * repair_time))

    def cycle(self, glucose, count, oxygen):
        """Simulate one hour of the cell's cycle"""
        if glucose < critical_glucose_level or oxygen < critical_oxygen_level:
            self.alive = False
            CancerCell.cell_count -= 1
            return 0, 0
        factor = random.normalvariate(1, 1 / 3)
        factor = max(0, min(2, factor))
        self.efficiency = average_glucose_absorption * factor
        self.oxy_efficiency = average_oxygen_consumption * factor
        if self.repair == 0:
            self.age += 1
        else:
            self.repair -= 1
        if self.stage == 3:  # Mitosis
            if self.age == 1:
                self.stage = 0
                self.age = 0
                return self.efficiency, self.oxy_efficiency, 1
            return self.efficiency, self.oxy_efficiency
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
        """RGB for the cell's color"""
        return 104, 24, 24

    def cell_type(self):
        """Return -1, the type of the cell to sort cell lists and compare them"""
        return -1


class OARCell(Cell):
    """OARCells are cells representing an organ at risk in the model."""
    cell_count = 0
    worth = 5

    def __init__(self, stage, worth):
        """Constructor of OARCell"""
        OARCell.cell_count += 1
        Cell.__init__(self, stage)
        OARCell.worth = worth

    def cycle(self, glucose, count, oxygen):
        """Simulate one hour of the cell's cycle"""
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
        """RGB for the cell's color"""
        return 255, 255, 153

    def cell_type(self):
        """Return the OARCell's worth, the type of the cell to sort cell lists and compare them"""
        return OARCell.worth

    def radiate(self, dose):
        """Irradiate this cell with a specific dose."""
        survival_probability = math.exp(radiosensitivities[self.stage] * (-alpha_norm_tissue*dose - beta_norm_tissue * (dose ** 2)))
        if random.random() > survival_probability:
            self.alive = False
            OARCell.cell_count -= 1
