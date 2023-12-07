import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

import traceback
import base64

from celery import Celery

from .Imports.vriCalc import observationManager
from matplotlib.figure import Figure
from matplotlib.colors import LogNorm
from matplotlib.ticker import MaxNLocator
from typing import Dict

obMan = observationManager(arrayDir='./vriBackend/tasks/arrays', 
                            verbose=True, debug=True)

obsMans:Dict[str, observationManager] = {}

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get('CELERY_BROKER_URL')
celery.conf.result_backend = os.environ.get('CELERY_RESULT_BACKEND')

@celery.task(name='init_obs')
def init_obs_man(obsId):
    obsMans[obsId] = observationManager(arrayDir='./vriBackend/tasks/arrays', 
                                        verbose=True, debug=True)
    return "ok"

@celery.task(name='array_select')
def select_array(array_config, haStart=6.0, haEnd=6.0, sampleRate=300.0, id=''):
    try:
        obsMan = obsMans[id]
        obsMan.select_array(
            array_config,
            haStart, haEnd,
            sampleRate
        )

        return {
            'status': 'array added',
            'array_config': array_config,
            'hour_angle_start': haStart,
            'hour_angle_end': haEnd,
            'sample_rate': sampleRate
        }
    
    except Exception as e:
        raise e

@celery.task(name='obs_option_select')
def select_observation_options(freq, src_declination, id=''):
    try:
        obsMan = obsMans[id]
        obsMan.set_obs_parms(freq, src_declination)
        return {
            'status': 'parameters added',
            'freq': freq,
            'src_declination': src_declination
        }
    except Exception as e:
        raise e

@celery.task(name='obs_pre_image_calculations')
def observation_setup(obs_id: str):
    obsMan = obsMans[obs_id]
    obsMan.calc_uvcoverage()

    # Plotting UV Cov code from vriCalc.py
    uvCovArr = obsMan.arrsSelected
    colLst=["r", "b", "g", "m", "c", "y", "k"]

    plt.title("UV Coverage")

    if uvCovArr is not None:
        oLst = []
        sLst = []
        for i, e in enumerate(uvCovArr):
            oLst.append(i)
            sLst.append(e["scaleMin_deg"])
        multiLst = list(zip(sLst, oLst))
        multiLst.sort()
        
        sLst, oLst = zip(*multiLst)
        zLst = range(len(oLst))
        multiLst = list(zip(oLst, zLst))
        multiLst.sort()
        oLst, zLst = zip(*multiLst)

    if uvCovArr is not None:
        for i, e in enumerate(uvCovArr):
            u = e["uArr_lam"]
            v = e["vArr_lam"]
            
            plt.scatter(x=u/1000, y=v/1000, marker=".", edgecolors='none',
                        s=2, color=colLst[i%len(colLst)], zorder=zLst[i])
            plt.scatter(x=-u/1000, y=-v/1000, marker=".", edgecolors='none',
                        s=2, color=colLst[i%len(colLst)], zorder=zLst[i])

    plt.xlabel(u"u (k$\lambda$)")
    plt.ylabel(u"v (k$\lambda$)")      
    plt.savefig(f'./vriBackend/tasks/plots/{obs_id}_uv_coverage.png',
                transparent=False)
    # Clearning all the plots
    plt.cla()
    plt.clf()

    return {
        'status': 'success',
        'figure': f'tasks/plots/{obs_id}_uv_coverage.png',
    }

@celery.task(name='obs_image_calculations')
def observation_image_calc(obs_id, img_path):
        obsMan = obsMans[obs_id]
        resulting_figures = {}

    # Plotting UV Coverage
        obsMan.calc_uvcoverage()
        uvCovArr = obsMan.arrsSelected
        colLst=["r", "b", "g", "m", "c", "y", "k"]

        plt.title("UV Coverage")

        if uvCovArr is not None:
            oLst = []
            sLst = []
            for i, e in enumerate(uvCovArr):
                oLst.append(i)
                sLst.append(e["scaleMin_deg"])
            multiLst = list(zip(sLst, oLst))
            multiLst.sort()
            
            sLst, oLst = zip(*multiLst)
            zLst = range(len(oLst))
            multiLst = list(zip(oLst, zLst))
            multiLst.sort()
            oLst, zLst = zip(*multiLst)

        if uvCovArr is not None:
            for i, e in enumerate(uvCovArr):
                u = e["uArr_lam"]
                v = e["vArr_lam"]
                
                plt.scatter(x=u/1000, y=v/1000, marker=".", edgecolors='none',
                            s=2, color=colLst[i%len(colLst)], zorder=zLst[i])
                plt.scatter(x=-u/1000, y=-v/1000, marker=".", edgecolors='none',
                            s=2, color=colLst[i%len(colLst)], zorder=zLst[i])

        plt.xlabel(u"u (k$\lambda$)")
        plt.ylabel(u"v (k$\lambda$)")      
        plt.savefig(f'./vriBackend/tasks/plots/{obs_id}_uv_coverage.png',
                    transparent=False)
        with open(f'./vriBackend/tasks/plots/{obs_id}_uv_coverage.png', 'rb') as uv_cov:
            resulting_figures['uv_cov'] = base64.b64encode(uv_cov.read()).decode('utf-8')
        
    # Clearning all the plots
        plt.cla()
        plt.clf()

    # Processing The Model Image to Sample    
        obsMan.load_model_image(img_path)
        obsMan.set_pixscale(1.0)
        obsMan.invert_model()

    # Plotting FFT
        fftArr = obsMan.modelFFTarr
        paramDict = obsMan.get_scales()
        limit = paramDict['fftScale_lam']/1e3

        plt.title("Model FFT")
        extent = [-limit, limit, -limit, limit]
        plt.xlabel(u"u (k$\lambda$)")
        plt.ylabel(u"v (k$\lambda$)")
        plt.imshow(np.abs(fftArr), norm=LogNorm(), cmap=plt.cm.cubehelix,
                   interpolation="nearest", origin="lower", extent=extent)
        plt.savefig(f'./vriBackend/tasks/plots/{obs_id}_fft_coverage.png')
        with open(f'./vriBackend/tasks/plots/{obs_id}_fft_coverage.png', 'rb') as fft_cov_img:
            resulting_figures['fft_cov'] = base64.b64encode(fft_cov_img.read()).decode('utf-8')

    # Clearning all the plots
        plt.cla()
        plt.clf()

        obsMan.grid_uvcoverage()

    # Plot Observed FFT
        fftArr = obsMan.obsFFTarr
        paramDict = obsMan.get_scales()
        limit = paramDict['fftScale_lam']/1e3
        
        plt.title("Observation FFT")
        extent = [-limit, limit, -limit, limit]
        plt.xlabel(u"u (k$\lambda$)")
        plt.ylabel(u"v (k$\lambda$)")
        plt.imshow(np.abs(fftArr), norm=LogNorm(), cmap=plt.cm.cubehelix,
                   interpolation="nearest", origin="lower", extent=extent)
        plt.savefig(f'./vriBackend/tasks/plots/{obs_id}_obs_fft_coverage.png')
        with open(f'./vriBackend/tasks/plots/{obs_id}_obs_fft_coverage.png', 'rb') as obs_fft_cov:
            resulting_figures['obs_fft_cov'] = base64.b64encode(obs_fft_cov.read()).decode('utf-8')
    
    # Clearning all the plots
        plt.cla()
        plt.clf()

    # Create the beam image
        obsMan.calc_beam()

        # Plot Synthesised Beam
        beamArr = np.abs(obsMan.beamArr)
        pRange = (-0.1, 0.5)

        zMin = np.nanmin(beamArr)
        zMax = np.nanmax(beamArr)
        zRng = zMin - zMax
        zMin -= zRng * pRange[0]
        zMax += zRng * pRange[1]

        plt.title("Synthesised Beam")
        plt.xticks([])
        plt.yticks([])
        plt.xlabel(u"")
        plt.ylabel(u"")
        plt.imshow(beamArr, cmap=plt.cm.cubehelix, interpolation="nearest",
                   origin="lower", vmin=zMin, vmax=zMax)
        plt.savefig(f'./vriBackend/tasks/plots/{obs_id}_synth_beam.png')
        with open(f'./vriBackend/tasks/plots/{obs_id}_synth_beam.png', 'rb') as synth_beam:
            resulting_figures['synth_beam'] = base64.b64encode(synth_beam.read()).decode('utf-8')

    # Clearning all the plots
        plt.cla()
        plt.clf()

    # Apply UV Coverage and Create Observed Image
        obsMan.invert_observation()
        imgArr = np.abs(obsMan.obsImgArr)
        plt.title("Final Observed Image")
        plt.xticks([])
        plt.yticks([])
        plt.xlabel(u"")
        plt.ylabel(u"")
        plt.imshow(imgArr, cmap=plt.cm.cubehelix, interpolation="nearest",
                   origin="lower")
        
        plt.savefig(f'./vriBackend/tasks/plots/{obs_id}_final_image.png')
        with open(f'./vriBackend/tasks/plots/{obs_id}_final_image.png', 'rb') as final_img:
            resulting_figures['final_img'] = base64.b64encode(final_img.read()).decode('utf-8')

    # Clearning all the plots
        plt.cla()
        plt.clf()

        return resulting_figures

@celery.task(name='obs_clear')
def clear_obs(id=''):
    obsMans[id] = observationManager(arrayDir='./vriBackend/tasks/arrays', 
                                     verbose=True, debug=True)
    plt.cla()
    plt.clf()
    plt.clim()

    return {'status': 'cleared'}