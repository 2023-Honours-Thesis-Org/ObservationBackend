from .Imports.vriCalc import observationManager
from matplotlib.figure import Figure
from matplotlib.colors import LogNorm
from matplotlib.ticker import MaxNLocator

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

import logging
import threading

# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

obsMan = observationManager(arrayDir='./vriBackend/tasks/arrays',
                            verbose=True, debug=True)