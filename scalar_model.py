import math
import matplotlib.pyplot as plt


alpha_tumor = 0.3
beta_tumor = 0.03
alpha_norm_tissue = 0.15
beta_norm_tissue = 0.03

INIT_COUNT = 100000000

class ScalarModel:

    def __init__(self):
        self.hcells = INIT_COUNT
        self.ccells = INIT_COUNT
        self.time = 0
        self.ticks = [self.time]
        self.ccell_counts = [self.ccells]
        self.hcell_counts = [self.hcells]

    def go(self):
        self.time += 1

        #effect from ccells on hcells
        self.hcells -= int(round(self.hcells * 0.01 * self.ccells / INIT_COUNT))

        #proliferation
        self.ccells += int(round(self.ccells * 1 / 50))
        if self.ccells + self.hcells < 2 * INIT_COUNT:
            self.hcells += int(round(self.hcells * 1 / 50 * (2 * INIT_COUNT - self.hcells - self.ccells) / (2 * INIT_COUNT)))

        #graph
        self.ticks.append(self.time)
        self.ccell_counts.append(self.ccells)
        self.hcell_counts.append(self.hcells)

    def act(self, dose):
        self.ccells = int(round(math.exp((-alpha_tumor * dose - beta_tumor * (dose ** 2))) * self.ccells))
        self.hcells = int(round(math.exp((-alpha_norm_tissue * dose - beta_norm_tissue * (dose ** 2))) * self.hcells))
        for i in range(24):
            self.go()

    def draw(self):
        plt.plot(self.ticks, self.ccell_counts, 'r')
        plt.plot(self.ticks, self.hcell_counts, 'b')
        plt.yscale('log')
        plt.title('Single dose')
        plt.savefig('dose')


'''
grays = 0
surviving = 1
while surviving > 0:
    grays += 1
    model = ScalarModel()
    model.send_dose(grays)
    surviving = model.ccells

print(grays)
'''
avg = 0
model = ScalarModel()
k = 0
ticks = [0]
ccells = [model.ccells]
hcells = [model.hcells]

while model.ccells > 0 and k < 100:
    k += 1
    model.act(22)

model.draw()
