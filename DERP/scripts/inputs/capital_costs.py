import pandas as pd
# import numpy as np

# 1st value is cost increase of the damaged capital (ie thermoelectric plants
# and hydro); 2nd is the general capital cost increase
cost_combinations = [
    [30, 20],
    [20, 10],
    [10, 5],
    ]

for combo in cost_combinations:
    combo_name = f'{combo[0]}_{combo[1]}'
    
    data_dict = {}
    data_dict['fossil energy coal.damaged capital cost factor'] = [1 + 0.01*combo[0]]
    data_dict['solar energy.general capital cost factor'] = [1 + 0.01*combo[1]]
    
    df_frida = pd.DataFrame(data_dict)
    
    df_frida.to_csv(f'../../data/inputs/capital_costs_{combo_name}.csv', index=False)

