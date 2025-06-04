import pandas as pd
import numpy as np
import copy

twh_yr_to_gw = 1/8.76

scenarios = [
    'NDC_EI_DERP2_HD', 
    'HD_ER_RCP85_1_CDD_30_20', 
    'HD_ER_RCP85_2_CDD_30_20', 
    'HD_ER_RCP85_3_CDD_30_20', 
    'HD_ER_RCP85_4_CDD_30_20', 
    'HD_ER_RCP85_5_CDD_30_20', 
    'HD_ER_RCP85_1_CDD_20_10', 
    'HD_ER_RCP85_2_CDD_20_10', 
    'HD_ER_RCP85_3_CDD_20_10', 
    'HD_ER_RCP85_4_CDD_20_10', 
    'HD_ER_RCP85_5_CDD_20_10', 
    'HD_ER_RCP85_1_CDD_30_20_nCAP',
    'HD_ER_RCP85_1_CDD_20_10_nCAP', 
    'HD_ER_RCP26_1_CDD_30_20_nCAP', 
    'HD_ER_RCP26_1_CDD_20_10_nCAP'
             ]

percs = ['', '_5th', '_95th']
years = np.arange(1980, 2155, 5)

# fraction of total energy output which is from electricity.
# for fossils, take the factor used in FRIDA to process
# reduction in electricity plant efficiency. Then need to convert TWh/yr to GW
# for renewables, so just use capacity in GW. 

# biomass is 0 here as the elec from biomass is processed through oil. 

# we are assuming that the ratio of elec capacity to secondary fuel output
# is a constant for each source, since we don't model electricity explicitly.
# the factors for the sources damaged by climate which we use this assumption
# for - i.e. fossil fuels - will need to be adjusted to
# account for this damage, since this affects the capacity/energy ratio.


elec_factors = {
"Secondary Energy|Coal":0.57,
"Secondary Energy|Gas":0.41,
"Secondary Energy|Oil":0.35,
"Capacity|Electricity|Nuclear":1,
"Secondary Energy|Biomass":0,
"Capacity|Electricity|Hydro":1,
"Capacity|Electricity|Solar":1,
"Capacity|Electricity|Wind":1,
    }

for scen in scenarios:
    
    if scen != 'NDC_EI_DERP2_HD':
        
        ssp = 'rcp' + scen.split("RCP")[1].split("_")[0]
        multiple = scen.split("_")[3]
        
        df_damage = pd.read_csv(f'../../data/inputs/energy_supply_efficiency_{ssp}_{multiple}x.csv')
    
    for perc in percs:
        csv_in = pd.read_csv(f'../../data/outputs/processed/FRIDA_{scen}{perc}.csv')
        
        total_elec = np.full(years.shape[0], 0.0)
        
        for source in elec_factors.keys():
            factor = 1
            if "Secondary Energy" in source:
                factor = twh_yr_to_gw
                
            for y_i, year_i in enumerate(years):
                    
                damage = 1
                if scen != 'NDC_EI_DERP2_HD':
                    if "Secondary Energy" in source:
                        damage = df_damage.loc[df_damage['Years'] == year_i
                           ]['efficiency reduction in power plants.exogenous effect of STA on river cooled thermal power energy capacity efficiency']
                            
                total_elec[y_i] += csv_in.loc[csv_in["Variable"] == source][f"{year_i}"
                                   ].values[0]*elec_factors[source]*factor/damage
              
        csv_out = copy.deepcopy(csv_in)
        
        new_row = ['FRIDAv2.1', scen, 'World', 
                 'Capacity|Electricity','GW'] + list(total_elec)
        
        csv_out.loc[len(csv_out)] = new_row
        
        csv_out.to_csv(f'../../data/outputs/processed/with_elec_cap/FRIDA_{scen}{perc}.csv', index=False)
        
        
#%%
for scen in scenarios:
    
    if scen != 'NDC_EI_DERP2_HD':
        
        ssp = 'rcp' + scen.split("RCP")[1].split("_")[0]
        multiple = scen.split("_")[3]
        
        df_damage = pd.read_csv(f'../../data/inputs/energy_supply_efficiency_{ssp}_{multiple}x.csv')
    
    for perc in percs:
        csv_in = pd.read_csv(f'../../data/outputs/processed/with_elec_cap/FRIDA_{scen}{perc}.csv')
        
        csv_out = copy.deepcopy(csv_in)
        
        for source in elec_factors.keys():
            if "Secondary Energy" not in source or 'Biomass' in source:
                continue
            
            source_elec = np.full(years.shape[0], np.nan)

            factor = 1
            if "Secondary Energy" in source:
                factor = twh_yr_to_gw
            
            for y_i, year_i in enumerate(years):
                
                damage = 1
                if scen != 'NDC_EI_DERP2_HD':
                    if "Secondary Energy" in source:
                        damage = df_damage.loc[df_damage['Years'] == year_i
                           ]['efficiency reduction in power plants.exogenous effect of STA on river cooled thermal power energy capacity efficiency']
                        
                        
                source_elec[y_i] = csv_in.loc[csv_in["Variable"] == source][f"{year_i}"
                                   ].values[0]*elec_factors[source]*factor/damage
        
            new_row = ['FRIDAv2.1', scen, 'World', 
                     f'Capacity|Electricity|{source.split("|")[-1]}','GW'] + list(source_elec)
            
            csv_out.loc[len(csv_out)] = new_row
        
        csv_out.to_csv(f'../../data/outputs/processed/with_elec_cap/FRIDA_{scen}{perc}_bysource.csv', index=False)

