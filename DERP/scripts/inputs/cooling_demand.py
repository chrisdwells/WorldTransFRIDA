import pandas as pd
import numpy as np

y1 = 1980
y2 = 2150
nt = y2 - y1 + 1

derps = ['eroded', 'incremental']

for derp in derps:
    
    df_in = pd.read_csv(f'../../data/sheets/Cooling_demand_pop_WA_FRIDA_gcam_{derp}.csv')
    
    df_in = df_in[['region', 'year', 'e_cool_delta', 'GCAM Region']]
    
    regions = set(list(df_in['region']))
    years = set(list(df_in['year']))
    
    global_totals = {}
    for year in years:
        global_totals[year] = 0
        for region in regions:
            
            df_cropped = df_in.loc[(df_in['year'] == year) & (df_in['region'] == region)]
            
            # We need when GCAM region is nan, because that's where the aggregate
            # regional data is held. But China has its own region, so there isn't
            # a row with nan in this broader region. Instead, we take the broader
            # regional value - and check it still has the right shape.
    
            df_cropped_delta = df_cropped.loc[pd.isna(df_cropped['GCAM Region']) == True]['e_cool_delta']
            
            if len(df_cropped_delta) == 1:
                global_totals[year] += df_cropped_delta.values[0]
    
            else:
                if len(df_cropped) == 1:
                    global_totals[year] += df_cropped['e_cool_delta'].values[0]
                else:
                    raise Exception(f'Check data; wrong shape: {region} {year}')
    
    
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
