import pandas as pd
import numpy as np

y1 = 1980
y2 = 2150
nt = y2 - y1 + 1

# use multiple=0 for baseline

multiples = [0, 1, 2, 3, 4, 5]

# bring in as percentage damages
damage_pcts = {}
damage_pcts['Hydro'] = {}
damage_pcts['Thermo'] = {}
damage_pcts['Hydro']['1980-2019'] = {}
damage_pcts['Thermo']['1980-2019'] = {}
damage_pcts['Hydro']['2020-2039'] = {}
damage_pcts['Thermo']['2020-2039'] = {}
damage_pcts['Hydro']['2040-2150'] = {}
damage_pcts['Thermo']['2040-2150'] = {}

damage_pcts['Thermo']['1980-2019']['rcp26'] = 0
damage_pcts['Hydro']['1980-2019']['rcp26'] = 0

damage_pcts['Thermo']['2020-2039']['rcp26'] = -5.8
damage_pcts['Hydro']['2020-2039']['rcp26'] = -1.7

damage_pcts['Thermo']['2040-2150']['rcp26'] = -7
damage_pcts['Hydro']['2040-2150']['rcp26'] = -1.2


damage_pcts['Thermo']['1980-2019']['rcp85'] = 0
damage_pcts['Hydro']['1980-2019']['rcp85'] = 0

damage_pcts['Thermo']['2020-2039']['rcp85'] = -5.3
damage_pcts['Hydro']['2020-2039']['rcp85'] = -1.9

damage_pcts['Thermo']['2040-2150']['rcp85'] = -12.1
damage_pcts['Hydro']['2040-2150']['rcp85'] = -3.6


# convert to efficiency factors
efficiency_factor = {}
for var in damage_pcts.keys():
    efficiency_factor[var] = {}
    for years_set in damage_pcts[var].keys():
        efficiency_factor[var][years_set] = {}
        for scen in damage_pcts[var][years_set].keys():
            efficiency_factor[var][years_set][scen] = {}
            for multiple in multiples:
                efficiency_factor[var][years_set][scen][multiple] = 1 + 0.01*multiple*damage_pcts[var][years_set][scen]


# make a csv for each scenario and multiple
for scen in ['rcp26', 'rcp85']:
    for multiple in multiples:
            
        data_dict = {
            'Years':np.arange(y1, y2+1, 1),
            'efficiency reduction in power plants.exogenous effect of STA on river cooled thermal power energy capacity efficiency':np.full(nt, np.nan),
            'efficiency reduction in power plants.exogenous effect of STA on hydropower energy capacity efficiency':np.full(nt, np.nan),
            }
        
        df_frida = pd.DataFrame(data_dict)
        
        for years_set in efficiency_factor['Thermo'].keys():
            year1 = int(years_set.split("-")[0])
            year2 = int(years_set.split("-")[1])
                
            
            df_frida.loc[(df_frida['Years'] >= year1) & (df_frida['Years'] <= year2), 
                  'efficiency reduction in power plants.exogenous effect of STA on river cooled thermal power energy capacity efficiency'
                  ] = efficiency_factor['Thermo'][years_set][scen][multiple]
            
            
            df_frida.loc[(df_frida['Years'] >= year1) & (df_frida['Years'] <= year2), 
                  'efficiency reduction in power plants.exogenous effect of STA on hydropower energy capacity efficiency'
                  ] = efficiency_factor['Hydro'][years_set][scen][multiple]
            
        df_frida = df_frida.set_index('Years')
        df_frida.to_csv(f'../../data/inputs/energy_supply_efficiency_{scen}_{multiple}x.csv')
