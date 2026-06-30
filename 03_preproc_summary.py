import mne
import pandas as pd
import numpy as np
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

N_JOBS = 12

base_dir = '/ohba/pi/mwoolrich/datasets/ntad'
meta_dir = base_dir + '/DataPortalIngest_March2025'
fname_base = base_dir + '/preprocessed/{task_id}/tsss/{ntad_id}_{task_name}_{visit_name}_raw_tsss/{ntad_id}_{task_name}_{visit_name}_tsss_'

df0 = pd.read_csv(meta_dir + '/ParticipantOverview.csv')
df0 = df0[df0['analyseable_using_NTAD_criteria'] == 'Yes']
df1 = pd.read_csv(meta_dir + '/MEG_metadata.csv', encoding='latin1')
df1 = df1[df1['NTAD_ID'].isin(df0['NTAD_ID'])]

TASK_COLUMNS = ['AV', 'MMN', 'SCENEREP', 'VAB', 'RSO', 'RSC']
TASK_NAMES   = ['av_task', 'mmn', 'scenerep', 'vao_task', 'resting_open', 'resting_close']

VISIT_MAP = {
    'Baseline': 'bl', 'Baseline2': 'bl2', 'Two-week': 'tw',
    'Annual': 'af', 'Annual follow-up': 'af', 'Annual follow-up2': 'af2',
}


def process_file(fname, ntad_id, visit_id, task):
    tqdm.write(f"  reading: {ntad_id} {visit_id} {task}")
    try:
        raw = mne.io.read_raw_fif(fname + 'preproc_raw.fif', preload=False, verbose=False)
        ica = mne.preprocessing.read_ica(fname + 'ica.fif', verbose=False)
    except Exception as e:
        tqdm.write(f"  SKIPPED {ntad_id} {visit_id} {task}: {e}")
        return task, None

    durs = np.array([r['duration'] for r in raw.annotations if 'bad' in r['description'].lower()])
    full_dur = raw.n_times / raw.info['sfreq']
    bad_segments = np.sum(durs) / full_dur * 100

    bads = raw.info['bads']
    types = raw.get_channel_types(picks=bads) if len(bads) > 0 else []
    grad_bads = len([ch for ch, t in zip(bads, types) if t == 'grad'])
    mag_bads  = len([ch for ch, t in zip(bads, types) if t == 'mag'])
    ica_bads  = len(ica.exclude)

    return task, {
        'NTAD ID': ntad_id,
        'Visit ID': visit_id,
        'Bad segments (%)': bad_segments,
        'Bad gradiometers (#)': grad_bads,
        'Bad magnetometers (#)': mag_bads,
        'Bad ICA components (#)': ica_bads,
    }


# build job list
jobs = []
for _, row in df1.iterrows():
    ntad_id  = row['NTAD_ID']
    visit_id = VISIT_MAP.get(row['VISIT_ID'], row['VISIT_ID'])
    for itask, (task, task_col) in enumerate(zip(TASK_NAMES, TASK_COLUMNS)):
        if row[task_col] == 'Y':
            fname = fname_base.format(task_id=itask+1, ntad_id=ntad_id, visit_name=visit_id, task_name=task)
            jobs.append((fname, ntad_id, visit_id, task))

stats = {task: [] for task in TASK_NAMES}

with ThreadPoolExecutor(max_workers=N_JOBS) as executor:
    futures = {executor.submit(process_file, *job): job for job in jobs}
    with tqdm(total=len(jobs), desc='Processing files', unit='file') as pbar:
        for future in as_completed(futures):
            fname, ntad_id, visit_id, task = futures[future]
            pbar.set_postfix(subject=ntad_id, visit=visit_id, task=task)
            task_key, entry = future.result()
            if entry is not None:
                stats[task_key].append(entry)
            pbar.update(1)

stats = {task: pd.DataFrame(rows) for task, rows in stats.items()}

for task, df in stats.items():
    df.to_csv(base_dir + f'/preprocessed/{task}_preproc_stats.csv', index=False)

all_stats = pd.concat(stats.values(), keys=stats.keys(), names=['Task', 'Row'])
all_stats.to_csv(base_dir + '/preprocessed/all_tasks_preproc_stats.csv', index=True)

METRICS = ['Bad segments (%)', 'Bad gradiometers (#)', 'Bad magnetometers (#)', 'Bad ICA components (#)']

def fmt(series):
    return f"{series.mean():.2f} ({series.std():.2f}) [{series.min():.2f}-{series.max():.2f}]"

rows = {}
rows['All tasks'] = {'Number of files': len(all_stats)}
for m in METRICS:
    rows['All tasks'][m] = fmt(all_stats[m])

for task, df in stats.items():
    rows[task] = {'Number of files': len(df)}
    for m in METRICS:
        rows[task][m] = fmt(df[m])

summary = pd.DataFrame(rows).T
summary.index.name = 'Task'
print(summary.to_string())
summary.to_csv(base_dir + '/preprocessed/preproc_summary_stats.csv')
