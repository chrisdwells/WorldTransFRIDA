import pandas as pd
import numpy as np
import copy

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

variables = [
     'Energy Balance Model.Surface Temperature Anomaly[1]',
     'Emissions.Total CO2 Emissions[1]',
     'Emissions.CO2 emissions from Energy[1]',
     'Emissions.CO2 Emissions from Food and Land Use[1]',
     'solar energy.Current Solar Capacity[1]',
     'wind energy.Current Wind Capacity[1]',
     'bio fuel energy.bio fuel production Capacity[1]',
     'bio fuel energy.bio fuel production[1]',
     'fossil energy coal.Fossil Energy and Fuel Capital[1]',
     'fossil energy gas.Fossil Energy and Fuel Capital[1]',
     'fossil energy oil.Fossil Energy and Fuel Capital[1]',
     'hydropower energy.Hydropower Energy Capacity[1]',
     'nuclear energy.Nuclear Energy Capacity[1]',
     'energy supply.Total Energy Output[1]',
     'fossil energy coal.Secondary Fossil Energy Output[1]',
     'fossil energy gas.Secondary Fossil Energy Output[1]',
     'fossil energy oil.Secondary Fossil Energy Output[1]',
     'nuclear energy.Nuclear Energy Output[1]',
     'bio fuel energy.bio fuel secondary energy output[1]',
     'hydropower energy.Hydropower Energy Output[1]',
     'solar energy.Solar Energy Output[1]',
     'wind energy.Wind Energy Output[1]',
         ]
    

frida_to_iamc = pd.read_csv('../../data/misc/FRIDA_to_IAMC.csv')

n_members = 1000
years = np.arange(1980, 2155, 5)

# load kept idxs from plot_results
keep = np.loadtxt(
    "../../data/misc/keep_idxs.csv",
).astype(np.int64)

columns = ['Model', 'Scenario', 'Region', 'Variable', 'Unit'] + list(years)

df_template = pd.DataFrame(columns = columns)

for scen in scenarios:
    
    offset = 1000
    if scen == 'NDC_EI_DERP2_HD':
        offset = 0
    
    df_out_50 = copy.deepcopy(df_template)
    df_out_5 = copy.deepcopy(df_template)
    df_out_95 = copy.deepcopy(df_template)

    
    df_scen = pd.read_csv(f'../../data/outputs/raw/{scen}.csv')
    df_scen = df_scen.loc[df_scen['Year'].isin(years)]
    
    for var in variables:
        in_data = np.full((years.shape[0], n_members), np.nan)
        
        for i in np.arange(n_members):
            in_data[:,i] = df_scen[f'="Run {i+1 + offset}: {var}"']
            
        median_data = np.nanpercentile(in_data[:,keep], 50, axis=1)
        perc_data_5 = np.nanpercentile(in_data[:,keep], 5, axis=1)
        perc_data_95 = np.nanpercentile(in_data[:,keep], 95, axis=1)

        
        row_out_med = ['FRIDAv2.1', scen, 'World', 
                 frida_to_iamc.loc[frida_to_iamc['FRIDA name'] == var]['IAMC name'].values[0],
                 frida_to_iamc.loc[frida_to_iamc['FRIDA name'] == var]['Units'].values[0],
                 ] + list(median_data)

        row_out_5 = ['FRIDAv2.1', scen, 'World', 
                 frida_to_iamc.loc[frida_to_iamc['FRIDA name'] == var]['IAMC name'].values[0],
                 frida_to_iamc.loc[frida_to_iamc['FRIDA name'] == var]['Units'].values[0],
                 ] + list(perc_data_5)

        row_out_95 = ['FRIDAv2.1', scen, 'World', 
                 frida_to_iamc.loc[frida_to_iamc['FRIDA name'] == var]['IAMC name'].values[0],
                 frida_to_iamc.loc[frida_to_iamc['FRIDA name'] == var]['Units'].values[0],
                 ] + list(perc_data_95)        

        df_out_50.loc[len(df_out_50)] = row_out_med
        df_out_5.loc[len(df_out_5)] = row_out_5
        df_out_95.loc[len(df_out_95)] = row_out_95

    df_out_50.to_csv(f'../../data/outputs/processed/FRIDA_{scen}.csv', index=False)
    df_out_5.to_csv(f'../../data/outputs/processed/FRIDA_{scen}_5th.csv', index=False)
    df_out_95.to_csv(f'../../data/outputs/processed/FRIDA_{scen}_95th.csv', index=False)
            
        
    