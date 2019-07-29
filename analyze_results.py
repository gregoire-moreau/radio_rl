import sys
import matplotlib.pyplot as plt
f = open(sys.argv[1])
count_steps = 0
count_eps = 0
count_losses = 0
count = 0
train = True
x = []
y = []
for line in f:
    if "Radiation dose : " in line:
        count += 1
        if train:
            count_steps += 1
    if "No more cancer" in line or "Cancer wins" in line:
        count_eps += 1
    if "Average (on the epoch) training loss" in line:
        count_losses += 1
        loss = line.split(": ")[1].rstrip()
        x.append(count_steps)
        y.append(float(loss))
    if count == 500 and not train:
        train = True
        count = 0
    if count == 1000 and train:
        train = False
        count = 0
count_eps /= 2
print("Number of steps :", count_steps)
print("Number of episodes played :" , count_eps)
f.close()
plt.plot(x, y)
plt.yscale("log")
plt.ylabel("Erreur : échelle logarithmique")
plt.xlabel("Time steps : Doses envoyées")
plt.title("Evolution de l'erreur pour :"+ sys.argv[2])
plt.show()