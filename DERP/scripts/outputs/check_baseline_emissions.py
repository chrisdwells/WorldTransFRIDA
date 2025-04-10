import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

n_members = 1000

var = 'Emissions.CO2 emissions from Energy'

tiam_time = [2005, 2010, 2015, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100]

tiam_emissions = [27569.09029, 29664.10879, 32524.99979, 31483.94859, 
                  23695.766, 17160.03866, 12404.63113, 9501.916877, 
                  7777.174729, 6593.071666, 5667.487622, 4984.560753]

gcam_time = [2005, 2010, 2015, 2020, 2025, 2030, 2035, 2040, 2045, 2050, 
             2055, 2060, 2065, 2070, 2075, 2080, 2085, 2090, 2095, 2100]

gcam_emissions = [29455.62074, 33498.14663, 35571.90241, 35891.50895, 34448.90401, 
                  33050.51107, 30446.54352, 27561.11641, 24699.71292, 22064.26636, 
                  19530.30235, 17446.12026, 15683.21795, 14108.1559, 12680.03351, 
                  11437.15033, 10315.03978, 9324.855556, 8530.450706, 7866.109736]

fig, axs = plt.subplots(1, 1, figsize=(7, 7))

plt.plot(tiam_time, tiam_emissions, label='TIAM')
plt.plot(gcam_time, gcam_emissions, label='GCAM')
plt.ylabel('GtCO2/yr')
plt.title('Energy CO2 Emissions')

baseline_data =  pd.read_csv("../../data/outputs/outputs_baseline_EMB.csv", index_col=False)

base_data = np.full((len(baseline_data['Year']), n_members), np.nan)

for i in np.arange(n_members):
    base_data[:,i] = baseline_data[f'="Run {i+1}: {var}[1]"']
    

plt.plot(baseline_data['Year'], np.nanpercentile(base_data, 50, axis=1),
         color='black', alpha=1, label='EMB')

plt.fill_between(baseline_data['Year'], np.nanpercentile(base_data, 5, axis=1),
         np.nanpercentile(base_data, 95, axis=1),
         color='black', alpha=0.3, linewidth=0)


baseline_data_run1 =  pd.read_csv("../../data/outputs/outputs_baseline_EMB_run1.csv", index_col=False)
plt.plot(baseline_data['Year'], baseline_data_run1[f'="Run 1: {var}[1]"'],
         color='red', alpha=1, label='EMB Run 1')


baseline_data_try2 =  pd.read_csv("../../data/outputs/outputs_baseline_try2_run1.csv", index_col=False)
plt.plot(baseline_data['Year'], baseline_data_try2[f'="Run 1: {var}[1]"'],
         color='green', alpha=1, label='Try2 Run 1')


baseline_data_try2_halvesubsidies =  pd.read_csv("../../data/outputs/outputs_baseline_try2_halvesubsidies_run1.csv", index_col=False)
plt.plot(baseline_data['Year'], baseline_data_try2_halvesubsidies[f'="Run 1: {var}[1]"'],
         color='purple', alpha=1, label='Try2 0.5*Subs Run 1')

baseline_data_try2_2_3rdssubsidies =  pd.read_csv("../../data/outputs/outputs_baseline_try2_2_3rdssubsidies_run1.csv", index_col=False)
plt.plot(baseline_data['Year'], baseline_data_try2_2_3rdssubsidies[f'="Run 1: {var}[1]"'],
         color='grey', alpha=1, label='Try2 2/3*Subs Run 1')

baseline_data_try2_2_3rdssubsidies_ext_subs_2090 =  pd.read_csv("../../data/outputs/outputs_baseline_try2_2_3rdssubsidies_ext_subs_2090_run1.csv", index_col=False)
plt.plot(baseline_data['Year'], baseline_data_try2_2_3rdssubsidies_ext_subs_2090[f'="Run 1: {var}[1]"'],
         color='pink', alpha=1, label='Try2 2/3*Subs 2090Subs Run 1')



baseline_data_new =  pd.read_csv("../../data/outputs/outputs_baseline_NDC.csv", index_col=False)

base_data_new = np.full((len(baseline_data_new['Year']), n_members), np.nan)

for i in np.arange(n_members):
    base_data_new[:,i] = baseline_data_new[f'="Run {i+1}: {var}[1]"']
    

plt.plot(baseline_data_new['Year'], np.nanpercentile(base_data_new, 50, axis=1),
         color='pink', alpha=1, label='NDC')

plt.fill_between(baseline_data_new['Year'], np.nanpercentile(base_data_new, 5, axis=1),
         np.nanpercentile(base_data_new, 95, axis=1),
         color='pink', alpha=0.3, linewidth=0)

plt.legend(loc='upper right')
