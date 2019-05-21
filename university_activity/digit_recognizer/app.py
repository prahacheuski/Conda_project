import pickle

from flask import Flask, jsonify, render_template, request

from utils.preprocessing import *
from utils.convnet import predict

PICKLE_FILE = 'MNIST/trained.pickle'
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/digit_process', methods=['POST'])
def digit_process():
    if request.method == 'POST':
        img = preprocess(request.get_json())

        with open(PICKLE_FILE, 'rb') as f:
            filt1, filt2, bias1, bias2, theta3, bias3, _, _ = pickle.load(f)
            digit, probability = predict(img, filt1, filt2, bias1, bias2, theta3, bias3)

            data = {'digit': str(digit), 'probability': np.round(probability, 3)}
            print(data)
            return jsonify(data)


if __name__ == '__main__':
    app.run(debug=False)
