import os
import time
# noinspection PyUnresolvedReferences
import tensorflow  # Do not remove this import despite what Pycharms says, as tensorboard won't run without it
from tensorboard import program

from config import ROOT_DIR

if __name__ == '__main__':
    # TODO: Validation data is not being displayed in the dashboard
    log_dir = os.path.join(ROOT_DIR, "static/logs/")
    tb = program.TensorBoard()
    tb.configure(argv=[None, '--logdir', log_dir])
    url = tb.launch()
    print(url)
    while True:
        time.sleep(60)
        pass
