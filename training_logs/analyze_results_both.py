import sys
import matplotlib.pyplot as plt
import pickle
f = open(sys.argv[1])
count_steps_dose = 0
count_steps_hour = 0
count_eps = 0
count_losses = 0
count = 0
train = True
mode_dose = True
x_dose = []
x_hour = []
y_dose = []
y_hour = []
for line in f:
    if "Radiation dose : " in line:
        count += 1
        if mode_dose and train:
            count_steps_dose += 1
        elif train:
            count_steps_hour += 1
    if "No more cancer" in line or "Cancer wins" in line:
        count_eps += 1
    if "Average (on the epoch) training loss" in line:
        count_losses += 1
        loss = line.split(": ")[1].rstrip()
        if mode_dose and train:
            x_dose.append(count_steps_dose*2)
            y_dose.append(float(loss))
        elif train:
            x_hour.append(count_steps_hour*2)
            y_hour.append(float(loss))
    if "epoch 1:" in line:
        train = False
    if "START DOSE" in line:
        mode_dose = True
        train = True
    if "START HOUR" in line:
        mode_dose = False
        train = True
count_eps /= 2
#print("Number of steps :", count_steps)
#print("Number of episodes played :" , count_eps)
f.close()
plt.plot(x_dose, y_dose, 'b')
plt.yscale("log")
plt.ylabel("Erreur : échelle logarithmique")
plt.xlabel("Time steps : Doses envoyées")
plt.title("Evolution de l'erreur pour : le dose agent")
plt.show()
input("Press Enter to continue...")
plt.plot(x_hour, y_hour)
plt.yscale("log")
plt.ylabel("Erreur : échelle logarithmique")
plt.xlabel("Time steps : Doses envoyées")
plt.title("Evolution de l'erreur pour : le hour agent")
plt.show()
input("Press Enter to continue...")
plt.plot(x_dose, y_dose, 'b')
plt.plot(x_hour, y_hour, 'r')
plt.yscale("log")
plt.ylabel("Erreur : échelle logarithmique")
plt.xlabel("Time steps : Doses envoyées")
plt.title("Evolution de l'erreur pour : le hour agent")
plt.show()
'''
f = open('end_dose', 'wb')
pickle.dump((x_dose, y_dose), f)
f.close()

f = open('end_hour', 'wb')
pickle.dump((x_hour, y_hour), f)
f.close()
'''