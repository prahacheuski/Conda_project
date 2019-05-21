import pickle
import time

import matplotlib.pyplot as plt
from matplotlib import gridspec
from pathlib2 import Path

from utils.convnet import *

# Hyperparameters
NUM_OUTPUT = 10
LEARNING_RATE = 0.01  # learning rate
IMG_WIDTH = 28
IMG_DEPTH = 1
FILTER_SIZE = 5
NUM_FILT1 = 8
NUM_FILT2 = 8
BATCH_SIZE = 20
NUM_EPOCHS = 2  # number of iterations
MU = 0.95
PICKLE_FILE = 'output.pickle'
MNIST_DIR_PATH = Path(__file__).parents[1] / 'MNIST'


def print_time(time_remain):
    hrs = int(time_remain) / 3600
    mins = int((time_remain / 60 - hrs * 60))
    secs = int(time_remain - mins * 60 - hrs * 3600)
    print('{}Hrs {}Mins {}Secs remaining'.format(hrs, mins, secs))


# Data extracting
m = 10000
X = extract_data(str(MNIST_DIR_PATH / 't10k-images-idx3-ubyte.gz'), m, IMG_WIDTH)
y_dash = extract_labels(str(MNIST_DIR_PATH / 't10k-labels-idx1-ubyte.gz'), m).reshape(m, 1)
X -= int(np.mean(X))
X /= int(np.std(X))
test_data = np.hstack((X, y_dash))

m = 50000
X = extract_data(str(MNIST_DIR_PATH / 'train-images-idx3-ubyte.gz'), m, IMG_WIDTH)
y_dash = extract_labels(str(MNIST_DIR_PATH / 'train-labels-idx1-ubyte.gz'), m).reshape(m, 1)
print(np.mean(X), np.std(X))
X -= int(np.mean(X))
X /= int(np.std(X))
train_data = np.hstack((X, y_dash))

np.random.shuffle(train_data)

NUM_IMAGES = train_data.shape[0]

# Initializing all the parameters
filt1 = {}
filt2 = {}
bias1 = {}
bias2 = {}

for i in range(0, NUM_FILT1):
    filt1[i] = initialise_param_lecun_normal(FILTER_SIZE, IMG_DEPTH, scale=1.0)
    bias1[i] = 0

for i in range(0, NUM_FILT2):
    filt2[i] = initialise_param_lecun_normal(FILTER_SIZE, NUM_FILT1, scale=1.0)
    bias2[i] = 0

w1 = IMG_WIDTH - FILTER_SIZE + 1
w2 = w1 - FILTER_SIZE + 1
theta3 = initialize_theta(NUM_OUTPUT, (w2 / 2) * (w2 / 2) * NUM_FILT2)

bias3 = np.zeros((NUM_OUTPUT, 1))
cost = []
acc = []

print("Learning Rate: {}, Batch Size: {}".format(LEARNING_RATE, BATCH_SIZE))

# Training start here
for epoch in range(0, NUM_EPOCHS):
    np.random.shuffle(train_data)
    batches = [train_data[k:k + BATCH_SIZE] for k in range(0, NUM_IMAGES, BATCH_SIZE)]
    x = 0
    for batch in batches:
        stime = time.time()
        out = momentumGradDescent(batch, LEARNING_RATE, IMG_WIDTH, IMG_DEPTH, MU, filt1, filt2, bias1, bias2, theta3,
                                  bias3, cost, acc)
        filt1, filt2, bias1, bias2, theta3, bias3, cost, acc = out
        epoch_acc = np.round(np.sum(acc[epoch * NUM_IMAGES / BATCH_SIZE:]) / (x + 1), 2)

        per = float(x + 1) / len(batches) * 100
        print("Epoch:" + str(round(per, 2)) + "% Of " + str(epoch + 1) + "/" + str(NUM_EPOCHS) + ", Cost:" + str(
            cost[-1]) + ", B.Acc:" + str(acc[-1] * 100) + ", E.Acc:" + str(epoch_acc))

        deltime = time.time() - stime
        remtime = (len(batches) - x - 1) * deltime + deltime * len(batches) * (NUM_EPOCHS - epoch - 1)
        print_time(remtime)
        x += 1

# saving the trained model parameters
with open(PICKLE_FILE, 'wb') as file:
    pickle.dump((filt1, filt2, bias1, bias2, theta3, bias3, cost, acc), file)

# Opening the saved model parameter
with open(PICKLE_FILE, 'rb') as f:
    filt1, filt2, bias1, bias2, theta3, bias3, cost, acc = pickle.load(f)

    # Plotting the cost and accuracy over different background
    gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1])
    ax0 = plt.subplot(gs[0])
    line0, = ax0.plot(cost, color='b')
    ax1 = plt.subplot(gs[1], sharex=ax0)
    line1, = ax1.plot(acc, color='r', linestyle='--')
    plt.setp(ax0.get_xticklabels(), visible=False)
    ax0.legend((line0, line1), ('Loss', 'Accuracy'), loc='upper right')

    # remove vertical gap between subplots
    plt.subplots_adjust(hspace=.0)
    plt.show(block=False)

    # Computing Test accuracy
    X = test_data[:, 0:-1]
    X = X.reshape(len(test_data), IMG_DEPTH, IMG_WIDTH, IMG_WIDTH)
    y = test_data[:, -1]
    corr = 0
    print("Computing accuracy over test set:")
    for i in range(0, len(test_data)):
        image = X[i]
        digit, prob = predict(image, filt1, filt2, bias1, bias2, theta3, bias3)
        print(digit, y[i])
        if digit == y[i]:
            corr += 1
        if (i + 1) % int(0.01 * len(test_data)) == 0:
            print(str(float(i + 1) / len(test_data) * 100) + "% Completed")
    print("Test Set Accuracy: {}".format(float(corr) / len(test_data) * 100))
