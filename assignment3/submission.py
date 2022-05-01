# student ID: 20180438, Name: Jeongwon Choi
#!/usr/bin/python

import random
import collections
import math
import sys
from collections import Counter
from util import *


############################################################
# Problem 1: hinge loss
############################################################


def problem_1a():
    """
    return a dictionary that contains the following words as keys:
        pretty, good, bad, plot, not, scenery
    """
    # BEGIN_YOUR_ANSWER (our solution is 1 lines of code, but don't worry if you deviate from this)
    # raise NotImplementedError
    return {"pretty": 1, "good": 0, "bad": -1, "plot": -1, "not": -1, "scenery": 0}
    # END_YOUR_ANSWER


############################################################
# Problem 2: binary classification
############################################################

############################################################
# Problem 2a: feature extraction


def extractWordFeatures(x):
    """
    Extract word features for a string x. Words are delimited by
    whitespace characters only.
    @param string x:
    @return dict: feature vector representation of x.
    Example: "I am what I am" --> {'I': 2, 'am': 2, 'what': 1}
    """
    # BEGIN_YOUR_ANSWER (our solution is 6 lines of code, but don't worry if you deviate from this)
    feature = {}
    for word in x.split():
        if word not in feature:
            feature[word] = 1
        else:
            feature[word] += 1
    return feature
    # END_YOUR_ANSWER


############################################################
# Problem 2b: stochastic gradient descent


def learnPredictor(trainExamples, testExamples, featureExtractor, numIters, eta):
    """
    Given |trainExamples| and |testExamples| (each one is a list of (x,y)
    pairs), a |featureExtractor| to apply to x, and the number of iterations to
    train |numIters|, the step size |eta|, return the weight vector (sparse
    feature vector) learned.

    You should implement stochastic gradient descent.

    Note:
    1. only use the trainExamples for training!
    You can call evaluatePredictor() on both trainExamples and testExamples
    to see how you're doing as you learn after each iteration.
    2. don't shuffle trainExamples and use them in the original order to update weights.
    3. don't use any mini-batch whose size is more than 1
    """
    weights = {}  # feature => weight

    def sigmoid(n):
        return 1 / (1 + math.exp(-n))

    # BEGIN_YOUR_ANSWER (our solution is 14 lines of code, but don't worry if you deviate from this)

    def linearPredict(x):
        if dotProduct(weights, featureExtractor(x)) > 0:
            return 1
        else:
            return -1

    for iter in range(numIters):
        for x, y in trainExamples:
            feature = featureExtractor(x)
            prediction = dotProduct(weights, feature) * y
            if prediction < 1:
                for f, v in list(feature.items()):
                    if y == 1:
                        feature[f] = sigmoid(weights.get(f, 0) * v) * v
                    else:
                        feature[f] = sigmoid(-weights.get(f, 0) * v) * v * math.exp(weights.get(f, 0) * v)
                increment(weights, eta*y, feature)
        # print(f'iteration: {iter}, training error: {evaluatePredictor(trainExamples, linearPredict)}, test error: {evaluatePredictor(testExamples, linearPredict)}')
    # END_YOUR_ANSWER
    return weights


############################################################
# Problem 2c: bigram features


def extractBigramFeatures(x):
    """
    Extract unigram and bigram features for a string x, where bigram feature is a tuple of two consecutive words. In addition, you should consider special words '<s>' and '</s>' which represent the start and the end of sentence respectively. You can exploit extractWordFeatures to extract unigram features.

    For example:
    >>> extractBigramFeatures("I am what I am")
    {('am', 'what'): 1, 'what': 1, ('I', 'am'): 2, 'I': 2, ('what', 'I'): 1, 'am': 2, ('<s>', 'I'): 1, ('am', '</s>'): 1}
    """
    # BEGIN_YOUR_ANSWER (our solution is 5 lines of code, but don't worry if you deviate from this)
    feature = collections.defaultdict(int)
    wordSet = x.split()
    for i in range(len(wordSet)):
        if i == 0:
            feature[('<s>', wordSet[i])] += 1
            feature[(wordSet[i], wordSet[i + 1])] += 1
        elif i == len(wordSet) - 1:
            feature[(wordSet[i], '</s>')] += 1
        else:
            feature[(wordSet[i], wordSet[i+1])] += 1
        feature[wordSet[i]] += 1
    return feature
    # END_YOUR_ANSWER
    return phi
