# Maxfilter the NTAD dataset at OHBA

import os
from osl import maxfilter
from glob import glob
import pandas as pd

base_dir = '/ohba/pi/mwoolrich/datasets/ntad/' # top directory
meta_dir = base_dir + '/DataPortalIngest_March2025' # directory of meta data
MAXFILTER_PATH = '/neuro/bin/util/maxfilter' # Where the (licensed) MaxFilter is located

# gather data
df = pd.read_csv(meta_dir + '/MEG_metadata.csv', encoding='latin1')
files_to_maxfilter = glob(base_dir + 'sub-*/ses-*/meg/*.fif')
no_movecomp_ids = []

# needed to map from the file paths to the metadata
VISIT_MAP = {
    'bl': 'Baseline', 'bl2': 'Baseline2', 'tw': 'Two-week',
    'af': 'Annual follow-up', 'af2': 'Annual follow-up2',
}

outdirs = []
for f in files_to_maxfilter:
    ntad_id = f.split('/')[-4]
    visit_id = f.split('/')[-3]
    visit_id = VISIT_MAP[visit_id]
    
    df_row = df[(df['participant_id'] == ntad_id) & (df['visit_id'] == visit_id)]
    
    # default maxfilter args
    maxfilter_args = f"--maxpath {0} --headpos --mode cbu".format(MAXFILTER_PATH)
    
    if df_row['SCANNER'] == 'Elekta Neuromag':
         maxfilter_args += "--cal maxfilter_calibration_files/sss_cal_cambridge_vectorview.dat --ctc maxfilter_calibration_files/ct_sparse_cambridge_vectorview.fif"
    elif df_row['SCANNER']=='Elekta Triux Neo':
        maxfilter_args += "--cal maxfilter_calibration_files/sss_cal_cambridge_triux.dat --ctc maxfilter_calibration_files/ct_sparse_cambridge_triux.fif"
    elif df_row['SCANNER']=='MEGIN TriuxNeo':
        maxfilter_args += "--cal maxfilter_calibration_files/sss_cal_oxford_triux.dat --ctc maxfilter_calibration_files/ct_sparse_oxford_triux.fif"

    if ntad_id in no_movecomp_ids:
        maxfilter_args += "--nomovecompinter"
      
    outdirs.append("/".join(f.split('/')[:-1]))


# we will now run the maxfilter in series so that we can have different savepaths for each file
for f,o in zip(files_to_maxfilter, outdirs):
    maxfilter.run_maxfilter_batch(f, o, maxfilter_args)