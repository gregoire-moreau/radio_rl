import sys
import re
import matplotlib.pyplot as plt

epoch_nums = []
avg_scores = []
with open('training_logs/killed_ddpg/killed_ddpg/killed', 'r') as f:
    for line in f:
        epoch_test = re.match(r'epoch (\d+):', line)
        if epoch_test:
            epoch_nums.append(int(epoch_test.group(1)))
            continue
        score_test = re.match(r'Testing score per episode \(id: 0\) is (-?\d+\.\d+)', line)
        if score_test:
            avg_scores.append(float(score_test.group(1)))
            continue

ind = -1
max_score = -100
for i in range(len(epoch_nums)):
    if avg_scores[i] > max_score:
        max_score = avg_scores[i]
        ind = i

plt.xlabel('Epoch number')
plt.ylabel('Average score on test epoch')
plt.plot(epoch_nums, avg_scores, 'b')
plt.plot([epoch_nums[ind], epoch_nums[ind]], [min(avg_scores)-1, max(avg_scores) +1], 'r')
plt.plot([-1000, 1000], [max_score, max_score], 'r')
plt.xlim((min(epoch_nums), max(epoch_nums)))
plt.ylim((min(avg_scores)-0.1, max(avg_scores)+0.1))
plt.text(epoch_nums[ind] + 2, min(avg_scores) - 0.05, 'Epoch '+str(epoch_nums[ind]),  fontdict={'color':'red'})
plt.text(20, max(avg_scores)+0.02, "{:.3f}".format(max(avg_scores)),  fontdict={'color':'red'})
#plt.savefig('tmp/score_dose_dqn')
plt.show()



print("Best epoch :", epoch_nums[ind] , "with score", max_score)