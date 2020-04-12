from deer.experiment.base_controllers import Controller, EpsilonController
import numpy as np
import joblib
class GaussianNoiseController(EpsilonController):
    def __init__(self, initial_std_dev=1.0, n_decays=10000, final_std_dev=0.0, evaluate_on='action', periodicity=1, reset_every='none'):
        super().__init__(initial_e=initial_std_dev, e_decays=n_decays, e_min=final_std_dev,
                                             evaluate_on=evaluate_on, periodicity=periodicity, reset_every=reset_every)
    def _reset(self, agent):
        self._count = 0
        agent._train_policy.setStdDev(self._init_e)
        self._e = self._init_e

    def _update(self, agent):
        self._count += 1
        if self._periodicity <= 1 or self._count % self._periodicity == 0:
            agent._train_policy.setStdDev(self._e)
            self._e = max(self._e - self._e_decay, self._e_min)


class GridSearchController(Controller):

    def __init__(self, validationID=0, testID=None, unique_fname="nnet"):
        super(self.__class__, self).__init__()
        self.first_epoch = [0.001, 0.0001, 0.00001]
        self.multiplicator = [1, .75, .5]
        self._validationScores = []
        self._testScores = []
        self._epochNumbers = []
        self._trainingEpochCount = 0
        self._testID = testID
        self._validationID = validationID
        self._filename = unique_fname
        self._bestValidationScoreSoFar = -9999999

    def onEpochEnd(self, agent):
        if (self._active == False):
            return

        mode = agent.mode()
        if mode == self._validationID:
            score, _ = agent.totalRewardOverLastTest()
            self._validationScores.append(score)
            self._epochNumbers.append(self._trainingEpochCount)
            if score > self.best_cur_score:
                self.best_cur_score = score
                agent.dumpNetwork('cur_net')
            if score > self._bestValidationScoreSoFar:
                self._bestValidationScoreSoFar = score
                agent.dumpNetwork(self._filename)
                self.cur_best = self.cur_lr if self.adv_count == 0 else self.cur_lr * self.multiplicator[self.cur_count]
            self.cur_count += 1
            if self.cur_count == 3:
                agent.setNetwork('cur_net')
                agent.dumpNetwork('init_net')
                self.adv_count += 1
                self.cur_count = 0
                self.cur_lr = self.cur_best
                self.best_cur_score = -9999999
                print("Adv count :", self.adv_count, "LR :", self.cur_lr)
            else:
                agent.setNetwork('init_net')
                if self.adv_count == 0:
                    self.cur_lr = self.first_epoch[self.cur_count]
                    agent._learning_algo.setLearningRate(self.first_epoch[0])
                else:
                    agent._learning_algo.setLearningRate(self.cur_lr * self.multiplicator[self.cur_count])

        elif mode == self._testID:
            score, _ = agent.totalRewardOverLastTest()
            self._testScores.append(score)
        else:
            self._trainingEpochCount += 1

    def onStart(self, agent):
        if (self._active == False):
            return

        agent.dumpNetwork('init_net')
        self.cur_best = 0
        self.cur_count = 0
        self.adv_count = 0
        agent._learning_algo.setLearningRate(self.first_epoch[0])
        self.cur_lr = self.first_epoch[0]
        self.best_cur_score = -999999999

    def onEnd(self, agent):
        if (self._active == False):
            return

        bestIndex = np.argmax(self._validationScores)
        print("Best neural net obtained after {} epochs, with validation score {}".format(bestIndex + 1,
                                                                                          self._validationScores[
                                                                                              bestIndex]))
        if self._testID != None:
            print("Test score of this neural net: {}".format(self._testScores[bestIndex]))

        try:
            os.mkdir("scores")
        except Exception:
            pass
        basename = "scores/" + self._filename
        joblib.dump({"vs": self._validationScores, "ts": self._testScores}, basename + "_scores.jldump")
