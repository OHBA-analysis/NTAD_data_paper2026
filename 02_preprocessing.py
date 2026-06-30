
import os
import osl
import numpy as np
import glmtools as glm
from scipy import stats
from sys import argv
from glob import glob
from dask.distributed import Client


base_dir = '/ohba/pi/mwoolrich/datasets/ntad/'
task = 'rsc'
maxf = 'tsss'
use_dask = False
n_workers = 4

# Notch filters: line noise and HPI artefacts
config = """
meta:
  event_codes:
preproc:
  - pick_types:         {meg: True, eeg: False, stim: True, eog: True, ecg: True, chpi: True, misc: True, ref_meg: True}
  - crop:               {tmin: 30}
  - filter:             {l_freq: 0.5, h_freq: 125, method: iir, iir_params: {order: 5, ftype: butter}}
  - notch_filter:       {freqs: 50 58 88 100 117 150 156 185 200 224, notch_widths: 2} 
  - resample:           {sfreq: 500}
  - bad_segments:       {segment_len: 1000, picks: mag, significance_level: 0.1}
  - bad_segments:       {segment_len: 1000, picks: grad, significance_level: 0.1}
  - bad_segments:       {segment_len: 1000, picks: mag, mode: diff, significance_level: 0.1}
  - bad_segments:       {segment_len: 1000, picks: grad, mode: diff, significance_level: 0.1}
  - bad_channels:       {picks: mag, significance_level: 0.1}
  - bad_channels:       {picks: grad, significance_level: 0.1}
  - ica_raw:            {picks: meg, n_components: 64, random_state: 42}
  - ica_autoreject:     {picks: meg, ecgmethod: correlation, eogthreshold: 0.5, apply: False}
"""


if __name__ == '__main__':
    raw_files = glob(base_dir + 'sub-*/ses-*/meg/*.fif')
    subjects = [raw_file.split('/')[-1].split('.')[0] for raw_file in raw_files]
    outdir = base_dir + 'derivatives/preprocessed/'
      
    if use_dask:
      client = Client(n_workers=n_workers, threads_per_worker=1)
    goods = osl.preprocessing.run_proc_batch(config, 
                                             raw_files,
                                              subjects,
                                              outdir=outdir,
                                              overwrite=False,
                                              dask_client=use_dask,
                                            )
    
    
