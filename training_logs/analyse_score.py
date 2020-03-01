import re
import matplotlib.pyplot as plt

epoch_nums = []
avg_scores = []
with open('canicula/types-oar-0.0001-0.8', 'r') as f:
    for line in f:
        epoch_test = re.match(r'epoch (\d+):', line)
        if epoch_test:
            epoch_nums.append(int(epoch_test.group(1)))
            continue
        score_test = re.match(r'Testing score per episode \(id: 0\) is (-?\d+\.\d+)', line)
        if score_test:
            avg_scores.append(float(score_test.group(1)))
            continue

plt.plot(epoch_nums, avg_scores)
plt.show()

ind = -1
max_score = -100
for i in range(len(epoch_nums)):
    if avg_scores[i] > max_score:
        max_score = avg_scores[i]
        ind = i

print("Best epoch :", epoch_nums[ind] , "with score", max_score)