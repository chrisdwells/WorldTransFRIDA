import pandas as pd
import numpy as np

y1 = 1980
y2 = 2021
nt = y2 - y1 + 1

df_in = pd.read_csv('../../data/intermediate_outputs/baseline_energy_investments_by_source.csv')

n_members = 2


sources_damaged = ['Coal energy conversion', 'Coal fuel extraction', 
                   'Oil energy conversion', 'Oil fuel extraction', 
                   'Gas energy conversion', 'Gas fuel extraction', 
                   'Hydropower', 'Nuclear']

cols_remove = [k for k in df_in.keys() if "Calibration Data:" in k]

df_in.drop(cols_remove, axis=1, inplace=True)


data_dict = {
    'Years':np.arange(y1, y2+0.125, 0.125),
    }

for n in np.arange(n_members):
    for source in sources_damaged:
        data_dict[f'maximum investments in {source}[{n+1}]'
                  ] = df_in[f'Run {n+1}: energy investments.investment by source[1, {source}]']


sources_all = ['Coal energy conversion', 'Coal fuel extraction', 
                   'Oil energy conversion', 'Oil fuel extraction', 
                   'Gas energy conversion', 'Gas fuel extraction', 
                   'Hydropower', 'Nuclear', 'Solar', 'Wind', 'Bio']

df2_in = pd.read_csv('../../../test/other_outputs.csv')

for n in np.arange(n_members):
    data_dict[f'All Gross Energy Investments[{n+1}]'
              ] = df2_in[f'="Run {n+1}: energy investments.All Gross Energy Investments[1]"']
    
    for source in sources_all:
        data_dict[f'priority by source initial allocation[{n+1}, {source}]'
                  ] = df2_in[f'Run {n+1}: energy investments.priority by source initial allocation[1, {source}]']

    
df_frida = pd.DataFrame(data_dict)

df_frida = df_frida.set_index('Years')
df_frida.to_csv('../../../test/inputs.csv')

#%%

