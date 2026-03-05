import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

y1 = 1980
y2 = 2150
nt = y2 - y1 + 1

derps = ['Derailment', 'Inertia']

n_regions = 11

for derp in derps:
    
    df_in = pd.read_csv(f'../../data/sheets/Cooling_demand_{derp}.csv')
    
    df_in = df_in[['year', 'e_cool_delta']]
    
    years = set(list(df_in['year']))
    
    global_totals = {}
    for year in years:
        year_data = df_in.loc[(df_in['year'] == year)]
        
        if len(year_data) != n_regions:
            raise Exception('Wrong # regions?')
        
        global_totals[year] = year_data['e_cool_delta'].sum()
        
    
    data_dict = {
        'Years':np.arange(y1, y2+1, 1),
        'energy demand.exogenous total Change in energy used for cooling due to climate change':np.full(nt, np.nan),
        }
    
    df_frida = pd.DataFrame(data_dict)
    
    # assume values valid for proceeding decade
    for year in years:
        df_frida.loc[(df_frida['Years'] >= year) & (df_frida['Years'] <= year + 9), 
              'energy demand.exogenous total Change in energy used for cooling due to climate change'
              ] = global_totals[year]
        
    # assume zero before 2030
    df_frida.loc[df_frida['Years'] <= 2029, 
          'energy demand.exogenous total Change in energy used for cooling due to climate change'
          ] = 0
    
    df_frida.loc[df_frida['Years'] >= 2109, 
          'energy demand.exogenous total Change in energy used for cooling due to climate change'
          ] = global_totals[2100]
    
    df_frida = df_frida.set_index('Years')
    df_frida.to_csv(f'../../data/inputs/cooling_energy_demand_{derp}.csv')
    
    plt.plot(np.arange(y1, y2+1, 1), df_frida['energy demand.exogenous total Change in energy used for cooling due to climate change'
          ], label=derp)
plt.legend()
