import os
import re
import matplotlib.pyplot as plt

PATH = "stlra/stlra"
filter = r'types-dose-0.005-(.*)'


names = []
epochs = []
scores = []

for file in os.listdir(PATH):
    test = re.match(filter, file)
    if test:
        epoch_nums = []
        avg_scores = []
        names.append(test.group(1))
        with open(PATH+'/'+file, 'r') as f:
            loss = 0.0
            for line in f:
                epoch_test = re.match(r'epoch (\d+):', line)
                if epoch_test:
                    epoch_nums.append(int(epoch_test.group(1)))
                    #avg_scores.append(loss)
                    #if epoch_nums[-1] == 5:
                     #   break
                    continue
                loss_test = re.match(r'Average \(on the epoch\) training loss: (-?\d+\.\d+)', line)
                if loss_test:
                    loss = float(loss_test.group(1))


                score_test = re.match(r'Testing score per episode \(id: 0\) is (-?\d+\.\d+)', line)
                if score_test:
                    avg_scores.append(float(score_test.group(1)))
                    continue

        epochs.append(epoch_nums)
        scores.append(avg_scores)

for i in range(len(names)):
    plt.plot(epochs[i], scores[i], label=names[i])
#plt.yscale("log")
plt.legend()
plt.show()

