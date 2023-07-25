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
def conduct_observation(options: dict):
    obsMan = observationManager(verbose=True, debug=True)
    obsMan.get_available_arrays()

    obsMan.select_array(key=options['array'],
                        haStart=options['start'],
                        haEnd=options['end'],
                        sampRate_s=options['sampleRate'])
    return "doing task"