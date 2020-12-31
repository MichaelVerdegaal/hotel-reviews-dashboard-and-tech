from data.model_util import *

if __name__ == '__main__':
    model = read_model("simple_RNN.h5")
    print(model.summary())
