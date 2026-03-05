import pandas as pd
import numpy as np

scenarios = [
    "HD_D1",
    "HD_D1_20_10",
    "HD_D1_20_10_Limit",
    "HD_D1_Limit",
    # "HD_D2", #baseline
    "HD_D4",
    "HD_D4_20_10",
    "HD_D4_20_10_Limit",
    "HD_D4_Limit",
]



variables = [
     # 'Energy Balance Model.Surface Temperature Anomaly[1]',
     # 'Emissions.Total CO2 Emissions[1]',
     # 'Emissions.CO2 emissions from Energy[1]',
     # 'Emissions.CO2 Emissions from Food and Land Use[1]',
     'solar energy.Current Solar Capacity[1]',
     'wind energy.Current Wind Capacity[1]',
     'bio fuel energy.bio fuel production Capacity[1]',
     # 'bio fuel energy.bio fuel production[1]',
     'fossil energy coal.Fossil Energy and Fuel Capital[1]',
     'fossil energy gas.Fossil Energy and Fuel Capital[1]',
     'fossil energy oil.Fossil Energy and Fuel Capital[1]',
     'hydropower energy.Hydropower Energy Capacity[1]',
     'nuclear energy.Nuclear Energy Capacity[1]',
      # 'fossil energy coal.Secondary Fossil Energy Output[1]',
      # 'fossil energy gas.Secondary Fossil Energy Output[1]',
     # 'fossil energy oil.Secondary Fossil Energy Output[1]',
     # 'nuclear energy.Nuclear Energy Output[1]',
      # 'bio fuel energy.bio fuel secondary energy output[1]',
     # 'hydropower energy.Hydropower Energy Output[1]',
     # 'solar energy.Solar Energy Output[1]',
     # 'wind energy.Wind Energy Output[1]',
         ]


n_members = 1000
years = np.asarray([2040, 2070, 2100])

frida_to_iamc = pd.read_csv('../../data/misc/FRIDA_to_IAMC.csv')

# load kept idxs from plot_results
keep = np.loadtxt(
    "../../data/misc/keep_idxs.csv",
).astype(np.int64)

columns = ['Variable', 'Scenario', 'Percentile'] + list(years)

df_out = pd.DataFrame(columns = columns)

dict_baseline = {}

df_baseline_data = pd.read_csv('../../data/outputs/raw/HD_D2.csv')
df_baseline_data = df_baseline_data.loc[df_baseline_data['Year'].isin(years)]


for var in variables:
    in_data = np.full((years.shape[0], n_members), np.nan)
    
    for i in np.arange(n_members):
        in_data[:,i] = df_baseline_data[f'="Run {i+1}: {var}"']
            
    dict_baseline[var] = in_data[:,keep]
        

for scen in scenarios:
    
    df_scen = pd.read_csv(f'../../data/outputs/raw/{scen}.csv')
    df_scen = df_scen.loc[df_scen['Year'].isin(years)]
    
    for var in variables:
        in_data = np.full((years.shape[0], n_members), np.nan)
        
        for i in np.arange(n_members):
            in_data[:,i] = df_scen[f'="Run {i+1 + 1000}: {var}"']
            
        perc_dif = 100*(in_data[:,keep] - dict_baseline[var])/dict_baseline[var]
            
        median_data = np.nanpercentile(perc_dif, 50, axis=1)
        perc_data_5 = np.nanpercentile(perc_dif, 5, axis=1)
        perc_data_95 = np.nanpercentile(perc_dif, 95, axis=1)
        
        
        row_out_med = [frida_to_iamc.loc[frida_to_iamc['FRIDA name'
                       ] == var]['IAMC name'].values[0], scen, '50'] + list(median_data)
        row_out_5 = [frida_to_iamc.loc[frida_to_iamc['FRIDA name'
                         ] == var]['IAMC name'].values[0], scen, '5'] + list(perc_data_5)
        row_out_95 = [frida_to_iamc.loc[frida_to_iamc['FRIDA name'
                      ] == var]['IAMC name'].values[0], scen, '95'] + list(perc_data_95)

        
        df_out.loc[len(df_out)] = row_out_med
        df_out.loc[len(df_out)] = row_out_5
        df_out.loc[len(df_out)] = row_out_95

    geo_row_med = ['Capacity|Geothermal', scen, '50'] + list(np.full(years.shape[0], np.nan))
    geo_row_5 = ['Capacity|Geothermal', scen, '5'] + list(np.full(years.shape[0], np.nan))
    geo_row_95 = ['Capacity|Geothermal', scen, '95'] + list(np.full(years.shape[0], np.nan))
    
    df_out.loc[len(df_out)] = geo_row_med
    df_out.loc[len(df_out)] = geo_row_5
    df_out.loc[len(df_out)] = geo_row_95

df_out.to_csv('../../data/outputs/for_supplement/perc_cap_dif.csv')
