from data.model_util import *
from tensorflow.keras.utils import plot_model

if __name__ == '__main__':
    """
    Script to create simple graphs of a model, to use replace the filepaths in modelpath and plotname
    """
    modelpath = "/models/2021_01_05-12_26/Epoch-09_ValLoss-0.1736.h5"
    plotname = "Epoch-09_ValLoss-0.1736.png"
    print("Loading model...\n")
    model = read_model(modelpath)
    plot_model(
        model,
        to_file=os.path.join(ROOT_DIR, f"static/models/plots/{plotname}"),
        show_shapes=True,
        show_layer_names=False,
        show_dtype=True
    )
    print(f"Created plot of {modelpath}!")

