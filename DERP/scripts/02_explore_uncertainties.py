import pandas as pd
import xarray as xr
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

year = 2050
n_members = 1000

keep = np.loadtxt(
    "../data/misc/keep_idxs.csv",
).astype(np.int64)

samples = pd.read_csv('../data/inputs/samplePoints.csv')
paramlist = list(samples.keys())

params_to_remove = [
    'Circular Flow.normal bottom 40 wages[1]',
    'Circular Flow.time for bottom 40 to be affected[1]',
    'Circular Flow.xmiddle[1]', 
    'Circular Flow.xspeed[1]',
    'Circular Flow.yfrom[1]', 
    'Circular Flow.yto[1]',
    ]

for param in params_to_remove:
    paramlist.remove(param)

scenarios = {
    # 'HD_ER_RCP85_1_CDD_30_20': 'D1_ER_1RCP85_CDD_30_20',
    # 'HD_ER_RCP85_2_CDD_30_20': 'D1_ER_2RCP85_CDD_30_20',
    # 'HD_ER_RCP85_3_CDD_30_20': 'D1_ER_3RCP85_CDD_30_20',
    # 'HD_ER_RCP85_4_CDD_30_20': 'D1_ER_4RCP85_CDD_30_20',
    # 'HD_ER_RCP85_5_CDD_30_20': 'D1_ER_5RCP85_CDD_30_20',
    'HD_ER_RCP85_1_CDD_20_10': 'D1_ER_1RCP85_CDD_20_10',
    # 'HD_ER_RCP85_2_CDD_20_10': 'D1_ER_2RCP85_CDD_20_10',
    # 'HD_ER_RCP85_3_CDD_20_10': 'D1_ER_3RCP85_CDD_20_10',
    # 'HD_ER_RCP85_4_CDD_20_10': 'D1_ER_4RCP85_CDD_20_10',
    # 'HD_ER_RCP85_5_CDD_20_10': 'D1_ER_5RCP85_CDD_20_10',
    # 'HD_IR_RCP26_1_CDD_20_10_nCAP': 'D4_IR_1RCP26_CDD_20_10_nCAP',
    # 'HD_IR_RCP26_1_CDD_30_20_nCAP': 'D4_IR_1RCP26_CDD_30_20_nCAP',
    'HD_ER_RCP85_1_CDD_20_10_nCAP': 'D4_IR_1RCP85_CDD_20_10_nCAP',
    # 'HD_IR_RCP85_1_CDD_30_20_nCAP': 'D4_IR_1RCP85_CDD_30_20_nCAP',
    # 'HD_IR_RCP85_5_CDD_30_20_nCAP': 'D4_IR_5RCP85_CDD_30_20_nCAP',

}
scenlist = list(scenarios.keys())

ndc_data = pd.read_csv('../data/outputs/raw/NDC_EI_DERP2_HD.csv')
ndc_data = ndc_data.loc[ndc_data['Year'] == year]

varlist = []
for k in ndc_data.keys():
    if "Run 1: " in k:
        varlist.append(k.split('="Run 1: ')[1][:-4])

varlist.remove('CCS.Storing CO2')       

ds = xr.Dataset(
    data_vars = dict(
        r2 = (["Scenario", "Variable", "Parameter"],
              np.full((len(scenlist), len(varlist), len(paramlist)), np.nan)),
        ),
    coords = dict(
        Scenario = scenlist,
        Variable = varlist,
        Parameter = paramlist,
        )
    )

for scen in scenlist:
    print(scen)
    scen_data = pd.read_csv(f'../data/outputs/raw/{scen}.csv')
    scen_data = scen_data.loc[scen_data['Year'] == year]

    for var in varlist:
        print(var)
        ndc_arr = np.full(n_members, np.nan)
        for i in np.arange(n_members):
            ndc_arr[i] = ndc_data[f'="Run {i+1}: {var}[1]"'].values[0]
            
        scen_arr = np.full(n_members, np.nan)
        for i in np.arange(n_members):
            scen_arr[i] = scen_data[f'="Run {i+1+1000}: {var}[1]"'].values[0]
        
        scen_effect = scen_arr[keep] - ndc_arr[keep]
        for param in paramlist:
            param_data = samples[param].values[keep]
            if np.all(param_data == param_data[0]):
                continue
            
            result = scipy.stats.linregress(param_data, scen_effect)
            r2 = (result.rvalue)**2
            
            ds.loc[dict(Scenario=scen,
                        Variable = var,
                        Parameter = param,
                        )] = r2

#%%

for scen in scenlist:
    print(scen)
    scen_data = pd.read_csv(f'../data/outputs/raw/{scen}.csv')
    scen_data = scen_data.loc[scen_data['Year'] == year]
    for var in varlist:
        print(var)
        ndc_arr = np.full(n_members, np.nan)
        for i in np.arange(n_members):
            ndc_arr[i] = ndc_data[f'="Run {i+1}: {var}[1]"'].values[0]
            
        scen_arr = np.full(n_members, np.nan)
        for i in np.arange(n_members):
            scen_arr[i] = scen_data[f'="Run {i+1+1000}: {var}[1]"'].values[0]
        
        scen_effect = scen_arr[keep]- ndc_arr[keep]
        

        fig, ax = plt.subplots(4, 4, figsize=(16, 12))
        ax = ax.ravel()
        
        corrs = ds.loc[dict(Scenario=scen,
                    Variable = var,
                    )]
        
        corrs_sort = corrs.sortby(corrs["r2"], ascending=False)
        corrs_sort_non_nan = corrs_sort.dropna(dim="Parameter")

        
        for p_i, param in enumerate(corrs_sort_non_nan.coords["Parameter"].values[:16]):
            
            params_keep = samples[param].values[keep]
            
            ax[p_i].scatter(params_keep, scen_effect, color='black')
            
            result = scipy.stats.linregress(params_keep, scen_effect)
            slope = result.slope
            intercept = result.intercept
            r_value = result.rvalue
            r2_round = np.around(r_value**2, decimals=3)

            x_fit = np.linspace(params_keep.min(), params_keep.max(), 100)
            y_fit = slope * x_fit + intercept
            
            ax[p_i].plot(x_fit, y_fit, color='red', label=f'R2 = {r2_round}')
            
            mid = len(param) // 2
            param_name = ''.join(param[:mid]) + '\n' + ''.join(param[mid:])
            
            ax[p_i].set_title(f'{param_name}')
            ax[p_i].legend()
                        
        plt.suptitle(f'{var} {scen}', fontsize=16)
        
        plt.tight_layout()
        plt.savefig(
            f"../figures/correlations/{scen}_{var}.png"
        )
        
#%%

varlist_plot = [
     # 'Energy Balance Model.Surface Temperature Anomaly',
     # 'Emissions.Total CO2 Emissions',
     # 'Emissions.CO2 emissions from Energy',
     # 'Emissions.CO2 Emissions from Food and Land Use',
     # 'solar energy.Current Solar Capacity',
     # 'wind energy.Current Wind Capacity',
     # 'bio fuel energy.bio fuel production Capacity',
     # 'bio fuel energy.bio fuel production',
     'fossil energy coal.Fossil Energy and Fuel Capital',
     # 'fossil energy gas.Fossil Energy and Fuel Capital',
     # 'fossil energy oil.Fossil Energy and Fuel Capital',
     # 'hydropower energy.Hydropower Energy Capacity',
     # 'nuclear energy.Nuclear Energy Capacity',
     # 'energy supply.Total Energy Output',
      'fossil energy coal.Secondary Fossil Energy Output',
      'fossil energy gas.Secondary Fossil Energy Output',
     # 'fossil energy oil.Secondary Fossil Energy Output',
     # 'nuclear energy.Nuclear Energy Output',
      'bio fuel energy.bio fuel secondary energy output',
     # 'hydropower energy.Hydropower Energy Output',
     # 'solar energy.Solar Energy Output',
     # 'wind energy.Wind Energy Output'
    ]

n_params = 4

for scen in scenlist:
    print(scen)
    scen_data = pd.read_csv(f'../data/outputs/raw/{scen}.csv')
    scen_data = scen_data.loc[scen_data['Year'] == year]

    fig, ax = plt.subplots(len(varlist_plot), n_params, figsize=(4*n_params, 3*len(varlist_plot)))
    ax = ax.ravel()

    c = -1
    for var in varlist_plot:
        print(var)
        ndc_arr = np.full(n_members, np.nan)
        for i in np.arange(n_members):
            ndc_arr[i] = ndc_data[f'="Run {i+1}: {var}[1]"'].values[0]
            
        scen_arr = np.full(n_members, np.nan)
        for i in np.arange(n_members):
            scen_arr[i] = scen_data[f'="Run {i+1+1000}: {var}[1]"'].values[0]
        
        scen_effect = scen_arr[keep]- ndc_arr[keep]
        
        corrs = ds.loc[dict(Scenario=scen,
                    Variable = var,
                    )]
        
        corrs_sort = corrs.sortby(corrs["r2"], ascending=False)
        corrs_sort_non_nan = corrs_sort.dropna(dim="Parameter")

        
        for p_i, param in enumerate(corrs_sort_non_nan.coords["Parameter"].values[:n_params]):
            c += 1
            
            params_keep = samples[param].values[keep]

            ax[c].scatter(params_keep, scen_effect, color='black')
            
            result = scipy.stats.linregress(params_keep, scen_effect)
            slope = result.slope
            intercept = result.intercept
            r_value = result.rvalue
            r2_round = np.around(r_value**2, decimals=3)

            x_fit = np.linspace(params_keep.min(), params_keep.max(), 100)
            y_fit = slope * x_fit + intercept
            
            ax[c].plot(x_fit, y_fit, color='red', label=f'R2 = {r2_round}')
            
            mid = len(param) // 2
            param_name = ''.join(param[:mid]) + '\n' + ''.join(param[mid:])
            
            ax[c].set_title(f'{param_name}')
            ax[c].legend()
            
            if p_i == 0:
                mid = len(var) // 2
                var_name = ''.join(var[:mid]) + '\n' + ''.join(var[mid:])
                ax[c].set_ylabel(f'{var_name}')
                        
    plt.suptitle(f'{scen}', fontsize=16)
    
    plt.tight_layout()
    plt.savefig(
        f"../figures/correlations/{scen}_variables_v2.png"
    )
    
#%%

ds.to_netcdf("../data/outputs/correlations/param_correlations_2050.nc")
