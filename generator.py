from pycomposer.gancomposable._mxnet.conditional_gan_composer import ConditionalGANComposer
from logging import getLogger, StreamHandler, NullHandler, DEBUG, ERROR
import mxnet as mx
import torch

ctx = "cuda:0" if torch.cuda.is_available() else "cpu"

logger = getLogger("pygan")
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)

composer = ConditionalGANComposer(midi_path_list=['/Users/siya/UIUC/CS 222/course-project-group-27/test.mid'], 
                                  batch_size = 1,
                                  seq_len = 100,
                                  learning_rate = 0.0002,
                                  time_fraction = 0.25,
                                  ctx = mx.gpu())

composer.learn(iter_n=1000, k_step=10)

composer.compose(
    file_path="/Users/siya/UIUC/CS 222/course-project-group-27/output.mid", 
    # Mean of velocity.
    # This class samples the velocity from a Gaussian distribution of 
    # `velocity_mean` and `velocity_std`.
    # If `None`, the average velocity in MIDI files set to this parameter.
    velocity_mean=30,
    # Standard deviation(SD) of velocity.
    # This class samples the velocity from a Gaussian distribution of 
    # `velocity_mean` and `velocity_std`.
    # If `None`, the SD of velocity in MIDI files set to this parameter.
    velocity_std=0
)