import os
import numpy as np
import matplotlib as mpl

from celery import Celery
from .friendlyVRI.vriCalc import observationManager
from matplotlib.figure import Figure
from matplotlib.colors import LogNorm
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get('CELERY_BROKER_URL')
celery.conf.result_backend = os.environ.get('CELERY_RESULT_BACKEND')

@celery.task(name='vri')
def conduct_observation(arrays):
    obsMan = observationManager(verbose=True, debug=True)
    obsMan.get_available_arrays()

    for array in arrays:

        obsMan.select_array(key=array['array'],
                            haStart=array['start'],
                            haEnd=array['end'],
                            sampRate_s=array['sampleRate'])
    

    return "doing task"