import os
import re
import matplotlib.pyplot as plt

PATH = "calr/calr"
filter = r'head-dose-(.*)'


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
                    if epoch_nums[-1] == 5:
                        break
                    continue

        epochs.append(epoch_nums)
        scores.append(avg_scores)

score_1 = (1111111, -1)
score_2 = (1111111, -1)
score_4 = (1111111, -1)

for i in range(len(names)):
    if(scores[i][0] < score_1[0]):
        score_1 = (scores[i][0], names[i])
    if (scores[i][1] < score_2[0]):
        score_2 = (scores[i][1], names[i])
    if (scores[i][3] < score_4[0]):
        score_4 = (scores[i][3], names[i])
    plt.plot(epochs[i], scores[i], label=names[i])
#plt.yscale("log")
plt.legend()
plt.show()



print(score_1)
print(score_2)
print(score_4)