#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Load packages
import pyam
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List, Optional
from typing import List, Optional, Union
import math as math
import warnings
import os
import pathlib
import matplotlib.colors as mcolors
import matplotlib.lines as mlines
from typing import List, Optional, Dict

import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import matplotlib.ticker as mticker
import pathlib, math
from typing import List, Dict


# Only in interactive/Jupyter contexts:
get_ipython().run_line_magic('matplotlib', 'inline')

# Ignore all warnings
warnings.filterwarnings("ignore")


# # 1) Load data

# In[2]:


# -------------------
# Function to load and concatenate files from a directory
# -------------------

def load_and_concat_files_then_pyam(directory_path, file_types=None):
    """
    Load specified file types from a directory, concatenate them as pandas DataFrames,
    then convert the result to a pyam IamDataFrame.

    Parameters:
    -----------
    directory_path : str
        Path to the directory containing data files
    file_types : str or list, optional
        Specify which file types to process: "xlsx", "csv", or ["xlsx", "csv"]
        If None, both xlsx and csv files will be processed

    Returns:
    --------
    pyam.IamDataFrame
        Combined IamDataFrame from all files
    """
    # Set default file types if not specified
    if file_types is None:
        file_types = ["xlsx", "csv"]
    elif isinstance(file_types, str):
        file_types = [file_types]

    # Create lookup for file extensions
    valid_extensions = {
        "xlsx": ".xlsx",
        "csv": ".csv"
    }

    # Get the extensions to look for
    extensions_to_check = [valid_extensions[ft] for ft in file_types if ft in valid_extensions]

    # List to store all pandas dataframes
    all_dfs = []

    # Get all files with the specified extensions in the directory
    for file_name in os.listdir(directory_path):
        if any(file_name.endswith(ext) for ext in extensions_to_check):
            full_path = os.path.join(directory_path, file_name)

            try:
                # Read the file based on its extension
                if file_name.endswith('.csv'):
                    try:
                        data_file = pd.read_csv(full_path)
                    except UnicodeDecodeError:
                        data_file = pd.read_csv(full_path, encoding='ISO-8859-1')
                elif file_name.endswith('.xlsx'):
                    data_file = pd.read_excel(full_path)

                # Add to list of pandas DataFrames
                all_dfs.append(data_file)
                print(f"Read {file_name}")

            # If there is an error, print a message and continue to the next file
            except Exception as e:
                print(f"Error reading {file_name}: {e}")
                continue

    # Concatenate all pandas dataframes
    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)
        # Convert the combined DataFrame to pyam IamDataFrame
        result_df = pyam.IamDataFrame(combined_df)
        return result_df
    else:
        print("No files were processed")
        return None


# In[3]:


# Load data
path = "../data/outputs/processed/with_elec_cap/plot_test/"  
df = load_and_concat_files_then_pyam(path, file_types=["csv"])


# In[4]:


df


# In[5]:


df.scenario


# # 2) Explore and modify the data

# In[6]:


# -------------------
# Function to explore data
# -------------------

def explore_data(iam_df: pyam.IamDataFrame):
    """Explores a pyam.IamDataFrame (lists regions, variables, models, scenarios)."""

    if iam_df is None:
        print("Error: No IamDataFrame provided for exploration.")
        return

    print("\nAvailable Regions:", iam_df.region)
    print("\nAvailable Variables:", iam_df.variable)
    print("\nAvailable Models:", iam_df.model)
    print("\nAvailable Scenarios:", iam_df.scenario)

# -------------------
# Examples
# -------------------
# # Explore the combined data
# explore_data(all_data)


# In[7]:


explore_data(df)


# In[8]:


# -------------------
# Function to rename data
# -------------------

def rename_data(iam_df: pyam.IamDataFrame, renaming: dict, obj_type: str = "scenario") -> Optional[pyam.IamDataFrame]:
    """Renames scenarios, models, or variables in a pyam.IamDataFrame."""

    if iam_df is None:
        print("Error: No IamDataFrame provided for renaming.")
        return None

    try:
        iam_df.rename(**{obj_type: renaming}, inplace=True)
        return iam_df
    except Exception as e:
        print(f"Error during renaming: {e}")
        return None

# -------------------
# Examples
# -------------------

# # Rename scenarios
# scenario_renaming = {
#     'DERP1': 'NDC_EI_DERP1',
#     #... (rest of your renaming mapping)
# }
# renamed_data = rename_data(all_data, scenario_renaming)

# # Rename Models
# model_renaming = {
#     'AIM/CGE': 'AIM',
#     'MESSAGEix-GLOBIOM 1.0': 'MESSAGE',
# }
# renamed_models = rename_data(all_data, model_renaming, obj_type='model')


# In[9]:


# Rename Variables
variable_renaming = {
    'Capacity|Electricity|Gas|CCS': 'Capacity|Electricity|Gas|w/ CCS',
    'Capacity|Electricity|Coal|CCS': 'Capacity|Electricity|Coal|w/ CCS',
}
renamed_variables = rename_data(df, variable_renaming, obj_type='variable')


# In[10]:


# # rename scenarios

# scenario_renaming = {
#     'NDC_EI_DERP1': 'NDC_EI_DERP2_HD',
#     'HD_ER_RCP85_1_CDD_20_10_nocap': 'HD_IR_RCP85_1_CDD_20_10_nCAP',
#     'HD_ER_RCP85_1_CDD_30_20_nocap': 'HD_IR_RCP85_1_CDD_30_20_nCAP',
#     'HD_ER_RCP85_5_CDD_30_20_nocap': 'HD_IR_RCP85_5_CDD_30_20_nCAP',
#     'D4_IR_1RCP85_CDD_20_10_nCAP' : 'HD_IR_RCP85_1_CDD_20_10_nCAP',
#     'D4_IR_1RCP85_CDD_30_20_nCAP' : 'HD_IR_RCP85_1_CDD_30_20_nCAP',
#     'D4_IR_5RCP85_CDD_30_20_nCAP' : 'HD_IR_RCP85_5_CDD_30_20_nCAP',
# }
# renamed_data = rename_data(df, scenario_renaming)


# In[11]:


df.scenario


# In[12]:


# df.region


# In[13]:


df.filter(model = "*FRIDA*", 
          # variable = "*Secondary *",

            # region = "*EU*"

          ).variable


# # 3) Explore variables

# In[14]:


### Variables groups ###

# Capacity Additions (stacked area plot)
capacity_additions = [
    # 'Capacity Additions|Electricity|Biomass',
    # 'Capacity Additions|Electricity|Fossil',
    # 'Capacity Additions|Electricity|Coal',
    # 'Capacity Additions|Electricity|Gas',
    # 'Capacity Additions|Electricity|Oil',
    # 'Capacity Additions|Electricity|Biomass|w/ CCS',
    # 'Capacity Additions|Electricity|Biomass|w/o CCS',
    # 'Capacity Additions|Electricity|Coal|w/ CCS',
    # 'Capacity Additions|Electricity|Coal|w/o CCS',
    # 'Capacity Additions|Electricity|Gas|w/ CCS',
    # 'Capacity Additions|Electricity|Gas|w/o CCS',
    # 'Capacity Additions|Electricity|Oil|w/ CCS',
    # 'Capacity Additions|Electricity|Oil|w/o CCS',
    # 'Capacity Additions|Electricity|Solar',
    # 'Capacity Additions|Electricity|Wind',
    # 'Capacity Additions|Electricity|Geothermal',
    # 'Capacity Additions|Electricity|Nuclear',
    # 'Capacity Additions|Electricity|Hydro',
]

# Overall capacity (stacked area plot)
overall_capacity_electricity = [
    'Capacity|Electricity|Biomass',
    # 'Capacity|Electricity|Biomass|w/ CCS',
    # 'Capacity|Electricity|Biomass|w/o CCS',
    'Capacity|Electricity|Coal',
    # 'Capacity|Electricity|Coal|w/ CCS',  # Might need renaming!
    # 'Capacity|Electricty|Coal|CCS',
    # 'Capacity|Electricity|Coal|w/o CCS',
    'Capacity|Electricity|Gas',
    # 'Capacity|Electricity|Gas|w/ CCS',
    # 'Capacity|Electricity|Gas|CCS',
    # 'Capacity|Electricity|Gas|w/o CCS',
    'Capacity|Electricity|Oil',
    # 'Capacity|Electricity|Oil|w/ CCS',
    # 'Capacity|Electricity|Oil|w/o CCS',
    'Capacity|Electricity|Solar',
    # 'Capacity|Electricity|Solar|CSP',
    # 'Capacity|Electricity|Solar|PV',
    'Capacity|Electricity|Wind',
    # 'Capacity|Electricity|Wind|Offshore',
    # 'Capacity|Electricity|Wind|Onshore',
    'Capacity|Electricity|Geothermal',
    'Capacity|Electricity|Hydro',
    'Capacity|Electricity|Nuclear',
    # 'Capacity|Electricity|Ocean',
]

# Emissions (linear individual plots)
emissions = [
    # 'Emissions|CO2',
    # 'Emissions|CH4',
    # 'Emissions|Kyoto Gases',
    # 'Emissions|N2O',
    # 'Emissions|NOx',
    # 'Emissions|BC',
    # 'Emissions|CF4',
    # 'Emissions|C2F6',
    # 'Emissions|CO',
    # 'Emissions|F-Gases',
    # 'Emissions|HFC',
    # 'Emissions|NH3',
    # 'Emissions|OC',
    # 'Emissions|SF6',
    # 'Emissions|Sulfur',
    # 'Emissions|VOC',
]

# CO2 emissions (stacked area plot)
CO2_emissions = [
    # 'Emissions|CO2|AFOLU',
    # 'Emissions|CO2|Energy',
    # 'Emissions|CO2|Energy and Industrial Processes',
    # 'Emissions|CO2|Fossil Fuels and Industry',
    # 'Emissions|CO2|Industrial Processes',
    # 'Emissions|CO2|Product Use',
    # 'Emissions|CO2|Waste',
    # 'Emissions|CO2|Capture and Removal',  # You might want to uncomment this if relevant
]

# carbon sequestration (stacked area plot)
carbon_sequestration = [
    'Carbon Sequestration|Direct Air Capture',
#  'Carbon Sequestration|CCS',
    'Carbon Sequestration|CCS|Biomass',
#  'Carbon Sequestration|CCS|Biomass|Energy|Supply',
#  'Carbon Sequestration|CCS|Biomass|Energy|Supply|Electricity',
#  'Carbon Sequestration|CCS|Biomass|Energy|Supply|Liquids',
#  'Carbon Sequestration|CCS|Biomass|Energy|Supply|Hydrogen'
#  'Carbon Sequestration|CCS|Biomass|Energy|Demand|Industry',
    'Carbon Sequestration|CCS|Fossil',
    'Carbon Sequestration|CCS|Fossil|Energy|Demand|Industry',
    'Carbon Sequestration|CCS|Fossil|Energy|Supply',
#  'Carbon Sequestration|CCS|Fossil|Energy|Supply|Electricity',
#  'Carbon Sequestration|CCS|Fossil|Energy|Supply|Hydrogen',
#  'Carbon Sequestration|CCS|Fossil|Energy|Supply|Liquids',
#  'Carbon Sequestration|CCS|Industrial Processes',
    # 'Carbon Sequestration|Direct Air Capture',
    # 'Carbon Sequestration|CCS|Direct Air Capture',
    # 'Carbon Sequestration|CCS|Industrial Processes',
    # 'Carbon Sequestration|Land Use',
    # 'Carbon Sequestration|CCS|Industry',
]

# Land use sequestration (stacked area plot)
land_use_sequestration = [
#     'Carbon Sequestration|Land Use|Afforestation',
#     'Carbon Sequestration|Land Use|Agriculture',
#     'Carbon Sequestration|Land Use|Forest Management',
#     'Carbon Sequestration|Land Use|Other',
#     'Carbon Sequestration|Land Use|Other LUC',
]

# Carbon dioxide removal (stacked area plot)
carbon_dioxide_removal = [
    # 'Carbon Sequestration|Direct Air Capture',
    # 'Carbon Sequestration|Ocean',
    # 'Carbon Sequestration|Soil Carbon',
    # 'Carbon Sequestration|Land Use|Afforestation',
    # 'Carbon Sequestration|Land Use|Agriculture',
    # 'Carbon Sequestration|Land Use|Forest Management',
    # 'Carbon Sequestration|Land Use|Other',
    # 'Carbon Sequestration|Land Use|Other LUC',   
    # 'Carbon Removal',
    # 'Carbon Removal|Geological Storage|Direct Air Capture',
    # # 'Carbon Removal|Geological Storage',
    # 'Carbon Removal|Geological Storage|Biomass',
    # 'Carbon Removal|Land Use',
    # 'Carbon Capture|Geological Storage|Direct Air Capture',
    # # 'Carbon Sequestration|Geological Storage',
    # 'Carbon Capture|Geological Storage|Other Sources',
    # 'Carbon Capture|Industrial Processes',
#     'Carbon Removal|Geological Storage',
#  'Carbon Removal|Land Use',
#  'Gross Removals|CO2'
]

# Overall picture (linear individual plots)
timeseries_variables = [
    'Carbon Sequestration|CCS',
    # 'Carbon Sequestration|Land Use',
    # 'Primary Energy',
    'Final Energy',
    # 'GDP|PPP',
    # 'Emissions|CO2',
    # 'Temperature|Global Mean',
    # 'Investment|Energy Supply|Electricity',
    # 'Land Cover',
    # 'Secondary Energy',
    # 'Capacity Additions|Electricity',
    'Capacity|Electricity',
    # 'Price|Carbon',
    # 'CO2|Energy and Industrial Processes',
    'Emissions|CO2|Energy and Industrial Processes',
    'Final Energy|Electricity',
]

# Investment in energy supply (stacked area plot)
energy_investment = [
    # 'Investment|Energy Supply|CO2 Transport and Storage',
    # 'Investment|Energy Supply|Electricity',
    # 'Investment|Energy Supply|Heat',
    # 'Investment|Energy Supply|Hydrogen',
    # 'Investment|Energy Supply|Liquids',
    # 'Investment|Energy Supply|Other',
    # 'Investment|Energy Supply|Electricity|Biomass|w/ CCS',
    # 'Investment|Energy Supply|Electricity|Biomass|w/o CCS',
    # 'Investment|Energy Supply|Electricity|Coal|w/ CCS',
    # 'Investment|Energy Supply|Electricity|Coal|w/o CCS',
    # 'Investment|Energy Supply|Electricity|Gas|w/ CCS',
    # 'Investment|Energy Supply|Electricity|Gas|w/o CCS',
    # 'Investment|Energy Supply|Electricity|Oil|w/ CCS',
    # 'Investment|Energy Supply|Electricity|Oil|w/o CCS',
    # 'Investment|Energy Supply|Electricity|Solar',
    # 'Investment|Energy Supply|Electricity|Wind',
    # 'Investment|Energy Supply|Electricity|Geothermal',
    # 'Investment|Energy Supply|Electricity|Hydro',
    # 'Investment|Energy Supply|Electricity|Nuclear',
    # 'Investment|Energy Supply|Electricity|Transmission and Distribution',
]

# Primary energy (stacked area plot)
primary_energy = [
    # 'Primary Energy|Biomass',
    # 'Primary Energy|Biomass|w/ CCS',
    # 'Primary Energy|Biomass|w/o CCS',
    # 'Primary Energy|Coal',
    # 'Primary Energy|Coal|w/ CCS',
    # 'Primary Energy|Coal|w/o CCS',
    # # 'Primary Energy|Fossil',  
    # 'Primary Energy|Gas',
    # 'Primary Energy|Gas|w/ CCS',
    # 'Primary Energy|Gas|w/o CCS',
    # 'Primary Energy|Geothermal',
    # 'Primary Energy|Hydro',
    # # 'Primary Energy|Non-Biomass Renewables',  
    # 'Primary Energy|Nuclear',
    # 'Primary Energy|Ocean',
    # 'Primary Energy|Oil',
    # 'Primary Energy|Oil|w/ CCS',
    # 'Primary Energy|Oil|w/o CCS',
    # 'Primary Energy|Other',
    # 'Primary Energy|Secondary Energy Trade',
    # 'Primary Energy|Solar',
    # 'Primary Energy|Wind',
    # 'Primary Energy|Non-Biomass Renewables',
    # 'Primary Energy|Other',
]


# Final energy by carriers (stacked area plot)
final_energy_by_carriers = [
    'Final Energy|Electricity',
    'Final Energy|Gases',
    'Final Energy|Heat',
    'Final Energy|Liquids',
    'Final Energy|Solids',
    # 'Final Energy|Solids|Biomass', 
    #  'Final Energy|Solids|Biomass|Traditional',
    # 'Final Energy|Solids|Coal', 
    # 'Final Energy|Other Sector',
]

# Final energy by sources (stacked area plot)
final_energy_by_sources = [
    'Final Energy|Geothermal',
    'Final Energy|Solar',
    'Final Energy|Hydrogen',
]

# Finals by sector (stacked area plot)
finals_by_sector = [
    # 'Final Energy|Agriculture', 
    # 'Final Energy|Bunkers', 
    # 'Final Energy|Commercial', 
    'Final Energy|Industry',
    'Final Energy|Non-Energy Use', 
    # 'Final Energy|Residential', 
    'Final Energy|Residential and Commercial',
    'Final Energy|Transportation',
    # 'Final Energy|Transportation (w/ bunkers)', 
    # 'Final Energy|Other Sector', 
    # 'Final Energy|Other Sector|Electricity',
    # 'Final Energy|Non-Energy Use', 
    # 'Final Energy|Non-Energy Use|Coal',
    # 'Final Energy|Non-Energy Use|Gas',
    # 'Final Energy|Non-Energy Use|Oil',
    # 'Final Energy|Non-Energy Use|Biomass',
]

finals_by_sector_electricity = [
    'Final Energy|Industry|Electricity',
    'Final Energy|Residential and Commercial|Electricity',
    'Final Energy|Transportation|Electricity',
]

# Secondary energy (stacked area plot)
secondary_energy_electricity = [
    'Secondary Energy|Electricity|Biomass',
    # 'Secondary Energy|Electricity|Biomass|w/ CCS', 
    # 'Secondary Energy|Electricity|Biomass|w/o CCS', 
    'Secondary Energy|Electricity|Coal',
    # 'Secondary Energy|Electricity|Coal|w/ CCS', 
    # 'Secondary Energy|Electricity|Coal|w/o CCS', 
    'Secondary Energy|Electricity|Gas',
    # 'Secondary Energy|Electricity|Gas|w/ CCS', 
    # 'Secondary Energy|Electricity|Gas|w/o CCS', 
    'Secondary Energy|Electricity|Oil',
    # 'Secondary Energy|Electricity|Oil|w/o CCS', 
    'Secondary Energy|Electricity|Geothermal',
    'Secondary Energy|Electricity|Hydro',
    'Secondary Energy|Electricity|Nuclear',
    'Secondary Energy|Electricity|Solar',
    'Secondary Energy|Electricity|Wind',
    # 'Secondary Energy|Electricity|Non-Biomass Renewables', 
    # 'Secondary Energy|Gases', 
    # 'Secondary Energy|Heat', 
    # 'Secondary Energy|Hydrogen', 
    # 'Secondary Energy|Liquids', 
    # 'Secondary Energy|Solids', 

    'Secondary Energy|Electricity|Ocean',
    # 'Secondary Energy|Electricity|Solar|CSP',
    # 'Secondary Energy|Electricity|Solar|PV',
    # 'Secondary Energy|Electricity|Wind|Offshore',
    # 'Secondary Energy|Electricity|Wind|Onshore',


    # 'Secondary Energy|Hydrogen|Fossil',
    # 'Secondary Energy|Hydrogen|Fossil|w/ CCS',
    # 'Secondary Energy|Hydrogen|Fossil|w/o CCS',
    # 'Secondary Energy|Liquids|Oil',
    # 'Secondary Energy|Liquids|Biomass',
    # 'Secondary Energy|Liquids|Biomass|w/ CCS',
    # 'Secondary Energy|Liquids|Gas',
    # 'Secondary Energy|Liquids|Gas|w/o CCS',
    # 'Secondary Energy|Hydrogen|Biomass',
    # 'Secondary Energy|Hydrogen|Biomass|w/ CCS',
    # 'Secondary Energy|Liquids|Biomass|w/o CCS',
    # 'Secondary Energy|Hydrogen|Electricity',

    #  'Secondary Energy|Gases|Biomass',
    #  'Secondary Energy|Gases|Coal',
    #  'Secondary Energy|Gases|Natural Gas',
    #  'Secondary Energy|Hydrogen|Biomass|w/o CCS',
    #  'Secondary Energy|Hydrogen|Coal',
    #  'Secondary Energy|Hydrogen|Coal|w/ CCS',
    #  'Secondary Energy|Hydrogen|Gas',
    #  'Secondary Energy|Hydrogen|Gas|w/ CCS',
    #  'Secondary Energy|Hydrogen|Gas|w/o CCS',
    #  'Secondary Energy|Liquids|Biomass|w/o CCS',
    #  'Secondary Energy|Liquids|Coal',
    #  'Secondary Energy|Liquids|Coal|w/ CCS',
    #  'Secondary Energy|Liquids|Coal|w/o CCS',
    #  'Secondary Energy|Liquids|Fossil',
    #  'Secondary Energy|Liquids|Fossil|w/ CCS',
    #  'Secondary Energy|Liquids|Fossil|w/o CCS',
    #  'Secondary Energy|Solids|Biomass',
    #  'Secondary Energy|Solids|Coal',
]

secondary_energy_non_electric = [
        'Secondary Energy|Gases', # Added, uncommented
    'Secondary Energy|Hydrogen', # Added, uncommented
    # 'Secondary Energy|Hydrogen|Electricity',
    # 'Secondary Energy|Hydrogen|Fossil',
    # 'Secondary Energy|Hydrogen|Fossil|w/ CCS',
    # 'Secondary Energy|Hydrogen|Fossil|w/o CCS',
    'Secondary Energy|Liquids', # Added, uncommented
    # 'Secondary Energy|Liquids|Biomass',
    # 'Secondary Energy|Liquids|Biomass|w/ CCS',
    # 'Secondary Energy|Liquids|Biomass|w/o CCS',
    # 'Secondary Energy|Liquids|Gas',
    # 'Secondary Energy|Liquids|Gas|w/o CCS',
    # 'Secondary Energy|Liquids|Oil',
    'Secondary Energy|Solids', # Added, uncommented
]


# Residential final energy (stacked area plot)
residential_final_energy = [
    # 'Final Energy|Residential and Commercial|Residential|Cooling', 
    # 'Final Energy|Residential and Commercial|Residential|Electricity', 
    # 'Final Energy|Residential and Commercial|Residential|Gases', 
    # 'Final Energy|Residential and Commercial|Residential|Heat', 
    # 'Final Energy|Residential and Commercial|Residential|Heating|Space', 
    # 'Final Energy|Residential and Commercial|Residential|Hydrogen', 
    # 'Final Energy|Residential and Commercial|Residential|Liquids', 
#  'Final Energy|Residential and Commercial|Commercial|Solids',
#  'Final Energy|Residential and Commercial|Commercial|Solids|Biomass',
#  'Final Energy|Residential and Commercial|Commercial|Solids|Coal',
]

# Commercial final energy (stacked area plot)
commercial_final_energy = [
    # 'Final Energy|Residential and Commercial|Commercial|Cooling', 
    # 'Final Energy|Residential and Commercial|Commercial|Electricity', 
    # 'Final Energy|Residential and Commercial|Commercial|Gases', 
    # 'Final Energy|Residential and Commercial|Commercial|Heat', 
    # 'Final Energy|Residential and Commercial|Commercial|Heating|Space', 
    # 'Final Energy|Residential and Commercial|Commercial|Hydrogen', 
    # 'Final Energy|Residential and Commercial|Commercial|Liquids', 
    # 'Final Energy|Residential and Commercial|Commercial|Solids', 
    # 'Final Energy|Residential and Commercial|Commercial|Solids|Biomass', 
    # 'Final Energy|Residential and Commercial|Commercial|Solids|Coal', 

]


# Residential and commercial final energy (stacked area plot)
residential_commercial_final_energy = [
    # 'Final Energy|Residential and Commercial|Cooling', 
    # 'Final Energy|Residential and Commercial|Heating', 
    'Final Energy|Residential and Commercial|Electricity',
    'Final Energy|Residential and Commercial|Gases',
    # 'Final Energy|Residential and Commercial|Heat|Space', 
    'Final Energy|Residential and Commercial|Heat', 
    'Final Energy|Residential and Commercial|Liquids',
    'Final Energy|Residential and Commercial|Hydrogen', 
    'Final Energy|Residential and Commercial|Solids',
    # 'Final Energy|Residential and Commercial|Solids|Biomass',
    # 'Final Energy|Residential and Commercial|Solids|Biomass|Traditional', 
    # 'Final Energy|Residential and Commercial|Solids|Coal',
    # 'Final Energy|Residential and Commercial|Other', 

]

# # Electricity by sector (stacked area plot)
# residential_commercial_final_energy = [
#     'Final Energy|Residential and Commercial|Electricity',
#     'Final Energy|Transportation|ELectricity',
#     'Final Energy|Industry|Electricity', 
# ]


# Final energy transport by mode (stacked area plot)
transport_mode_final_energy = [
    # 'Final Energy|Transportation|Domestic Aviation', 
    # 'Final Energy|Transportation|Domestic Shipping', 
    # 'Final Energy|Transportation|Bus', 
    # 'Final Energy|Transportation|Light-Duty Vehicle', 
    # 'Final Energy|Transportation|Truck', 

    # 'Final Energy|Transportation|Aviation',
    # 'Final Energy|Transportation|Aviation|Passenger',
    # 'Final Energy|Transportation|Freight',
    # 'Final Energy|Transportation|Freight|Electricity',
    # 'Final Energy|Transportation|Freight|Hydrogen',
    # 'Final Energy|Transportation|Freight|Liquids',
    # 'Final Energy|Transportation|Freight|Other',
    # 'Final Energy|Transportation|Maritime',
    # 'Final Energy|Transportation|Maritime|Freight',
    # 'Final Energy|Transportation|Other',
    # 'Final Energy|Transportation|Passenger',
    # 'Final Energy|Transportation|Passenger|Electricity',
    # 'Final Energy|Transportation|Passenger|Gases',
    # 'Final Energy|Transportation|Passenger|Hydrogen',
    # 'Final Energy|Transportation|Passenger|Liquids',
    # 'Final Energy|Transportation|Rail',
    # 'Final Energy|Transportation|Rail|Freight',
    # 'Final Energy|Transportation|Rail|Passenger',
    # 'Final Energy|Transportation|Road',
    # 'Final Energy|Transportation|Road|Freight',
    # 'Final Energy|Transportation|Road|Passenger',
    # 'Final Energy|Transportation|Road|Passenger|2W&3W',
    # 'Final Energy|Transportation|Road|Passenger|4W',
    # 'Final Energy|Transportation|Road|Passenger|Bus'

]

# Final energy transport by carrier (stacked area plot)
transport_carrier_final_energy = [
    'Final Energy|Transportation|Electricity',
    'Final Energy|Transportation|Gases',
    'Final Energy|Transportation|Hydrogen',
    'Final Energy|Transportation|Liquids',
    'Final Energy|Transportation|Solids', 
    # 'Final Energy|Transportation|Other', 
    # 'Final Energy|Transportation|Liquids|Biomass', 
    # 'Final Energy|Transportation|Liquids|Oil', 



]



# Final energy industry by carrier (stacked area plot)
industry_carrier_final_energy = [
    'Final Energy|Industry|Electricity',
    'Final Energy|Industry|Gases',
    'Final Energy|Industry|Heat',
    'Final Energy|Industry|Hydrogen',
    'Final Energy|Industry|Liquids',
    'Final Energy|Industry|Other', 
    'Final Energy|Industry|Solids',
    # 'Final Energy|Industry|Solids|Biomass',
    # 'Final Energy|Industry|Solids|Coal',
]

# Final energy INDUSTRY by subsecto (stacked area plot)
industry_subsector_final_energy = [
    # 'Final Energy|Industry|Cement',
    # 'Final Energy|Industry|Cement|Electricity',
    # 'Final Energy|Industry|Cement|Gases',
    # 'Final Energy|Industry|Chemicals',
    # 'Final Energy|Industry|Chemicals|Ammonia',
    # 'Final Energy|Industry|Chemicals|Ammonia|Gases',
    # 'Final Energy|Industry|Chemicals|Ammonia|Hydrogen',
    # 'Final Energy|Industry|Chemicals|Ammonia|Liquids',
    # 'Final Energy|Industry|Chemicals|Ammonia|Solids',
    # 'Final Energy|Industry|Chemicals|Ammonia|Solids|Fossil',
    # 'Final Energy|Industry|Chemicals|Electricity',
    # 'Final Energy|Industry|Chemicals|Gases',
    # 'Final Energy|Industry|Chemicals|Heat',
    # 'Final Energy|Industry|Chemicals|Hydrogen',
    # 'Final Energy|Industry|Chemicals|Liquids',
    # 'Final Energy|Industry|Chemicals|Solids',
    # 'Final Energy|Industry|Chemicals|Solids|Bioenergy',
    # 'Final Energy|Industry|Chemicals|Solids|Fossil',
    # 'Final Energy|Industry|Non-ferrous metals',
    # 'Final Energy|Industry|Non-ferrous metals|Electricity',
    # 'Final Energy|Industry|Non-ferrous metals|Gases',
    # 'Final Energy|Industry|Non-ferrous metals|Liquids',
    # 'Final Energy|Industry|Non-ferrous metals|Solids',
    # 'Final Energy|Industry|Non-ferrous metals|Solids|Bioenergy',
    # 'Final Energy|Industry|Non-ferrous metals|Solids|Fossil',
    # 'Final Energy|Industry|Steel',
    # 'Final Energy|Industry|Steel|Electricity',
    # 'Final Energy|Industry|Steel|Hydrogen',
    # 'Final Energy|Industry|Steel|Liquids',
    # 'Final Energy|Industry|Steel|Solids',
    # 'Final Energy|Industry|Steel|Solids|Bioenergy',
    # 'Final Energy|Industry|Steel|Solids|Fossil'

]

# CO2 Emissions from transport (stacked area plot)
CO2_emissions_transport = [
    # 'Emissions|CO2|Energy|Demand|Transportation|Freight',
    # 'Emissions|CO2|Energy|Demand|Transportation|Passenger',
    # 'Emissions|CO2|Energy|Demand|Transportation',
]


# In[15]:


capacity_additions
overall_capacity_electricity 
emissions 
CO2_emissions 
carbon_sequestration 
land_use_sequestration 
carbon_dioxide_removal 
timeseries_variables 
energy_investment 
primary_energy 
final_energy_by_carriers 
final_energy_by_sources 
finals_by_sector 
finals_by_sector_electricity 
secondary_energy_electricity 
secondary_energy_non_electric 
residential_final_energy 
commercial_final_energy 
residential_commercial_final_energy 
transport_mode_final_energy
transport_carrier_final_energy 
industry_carrier_final_energy 
industry_subsector_final_energy 
CO2_emissions_transport 


# In[16]:


### Updated Variable Group Naming Dictionaries ###

# Capacity Additions (all commented in original list)
capacity_additions_names = {
    # 'Capacity Additions|Electricity|Biomass': 'CapAdd|Elec|Biomass',
    # 'Capacity Additions|Electricity|Fossil': 'CapAdd|Elec|Fossil',
    # 'Capacity Additions|Electricity|Coal': 'CapAdd|Elec|Coal',
    # 'Capacity Additions|Electricity|Gas': 'CapAdd|Elec|Gas',
    # 'Capacity Additions|Electricity|Oil': 'CapAdd|Elec|Oil',
    # 'Capacity Additions|Electricity|Biomass|w/ CCS': 'CapAdd|Elec|Biomass|w/ CCS',
    # 'Capacity Additions|Electricity|Biomass|w/o CCS': 'CapAdd|Elec|Biomass|w/o CCS',
    # 'Capacity Additions|Electricity|Coal|w/ CCS': 'CapAdd|Elec|Coal|w/ CCS',
    # 'Capacity Additions|Electricity|Coal|w/o CCS': 'CapAdd|Elec|Coal|w/o CCS',
    # 'Capacity Additions|Electricity|Gas|w/ CCS': 'CapAdd|Elec|Gas|w/ CCS',
    # 'Capacity Additions|Electricity|Gas|w/o CCS': 'CapAdd|Elec|Gas|w/o CCS',
    # 'Capacity Additions|Electricity|Oil|w/ CCS': 'CapAdd|Elec|Oil|w/ CCS',
    # 'Capacity Additions|Electricity|Oil|w/o CCS': 'CapAdd|Elec|Oil|w/o CCS',
    # 'Capacity Additions|Electricity|Solar': 'CapAdd|Elec|Solar',
    # 'Capacity Additions|Electricity|Wind': 'CapAdd|Elec|Wind',
    # 'Capacity Additions|Electricity|Geothermal': 'CapAdd|Elec|Geothermal',
    # 'Capacity Additions|Electricity|Nuclear': 'CapAdd|Elec|Nuclear',
    # 'Capacity Additions|Electricity|Hydro': 'CapAdd|Elec|Hydro',
}

# Overall Capacity
overall_capacity_names = {
    'Capacity|Electricity|Biomass|w/ CCS': 'Cap|Elec|Biomass|w/ CCS',
    'Capacity|Electricity|Biomass|w/o CCS': 'Cap|Elec|Biomass|w/o CCS',
    'Capacity|Electricity|Biomass': 'Biomass', # changed on 18 June 2025
    'Capacity|Electricity|Fossil': 'Cap|Elec|Fossil',
    'Capacity|Electricity|Coal': 'Coal',
    'Capacity|Electricity|Gas': 'Gas',
    'Capacity|Electricity|Coal|w/ CCS': 'Cap|Elec|Coal|w/ CCS',  
    'Capacity|Electricity|Coal|w/o CCS': 'Cap|Elec|Coal|w/o CCS',
    'Capacity|Electricity|Gas|w/ CCS': 'Cap|Elec|Gas|w/ CCS',
    'Capacity|Electricity|Gas|w/o CCS': 'Cap|Elec|Gas|w/o CCS',
    'Capacity|Electricity|Oil': 'Oil',
    'Capacity|Electricity|Solar': 'Solar',
    'Capacity|Electricity|Wind': 'Wind',
    'Capacity|Electricity|Geothermal': 'Geothermal',
    'Capacity|Electricity|Hydro': 'Hydro',
    'Capacity|Electricity|Nuclear': 'Nuclear',
    # 'Capacity|Electricity|Ocean': 'Cap|Elec|Ocean',
    # 'Capacity|Electricity|Solar|CSP': 'Cap|Elec|Solar|CSP',
    # 'Capacity|Electricity|Solar|PV': 'Cap|Elec|Solar|PV',
    # 'Capacity|Electricity|Wind|Offshore': 'Cap|Elec|Wind|Offshore',
    # 'Capacity|Electricity|Wind|Onshore': 'Cap|Elec|Wind|Onshore',
}

# Emissions (all commented in original list)
emissions_names = {
    # 'Emissions|CO2': 'CO2',
    # 'Emissions|CH4': 'CH4',
    # 'Emissions|Kyoto Gases': 'Kyoto Gases',
    # 'Emissions|N2O': 'N2O',
    # 'Emissions|NOx': 'NOx',
    # 'Emissions|BC': 'BC',
    # 'Emissions|CF4': 'CF4',
    # 'Emissions|C2F6': 'C2F6',
    # 'Emissions|CO': 'CO',
    # 'Emissions|F-Gases': 'F-Gases',
    # 'Emissions|HFC': 'HFC',
    # 'Emissions|NH3': 'NH3',
    # 'Emissions|OC': 'OC',
    # 'Emissions|SF6': 'SF6',
    # 'Emissions|Sulfur': 'Sulfur',
    # 'Emissions|VOC': 'VOC',
}

# CO2 Emissions (all commented in original list)
CO2_emissions_names = {
    # 'Emissions|CO2|AFOLU': 'CO2|AFOLU',
    # 'Emissions|CO2|Energy': 'CO2|Energy',
    # 'Emissions|CO2|Energy and Industrial Processes': 'CO2|Energy and IndProc',
    # 'Emissions|CO2|Fossil Fuels and Industry': 'CO2|Fossil Fuels and Industry',
    # 'Emissions|CO2|Industrial Processes': 'CO2|IndProc',
    # 'Emissions|CO2|Product Use': 'CO2|Product Use',
    # 'Emissions|CO2|Waste': 'CO2|Waste',
    # 'Emissions|CO2|Capture and Removal': 'CO2|Capture and Removal',
}

# Carbon Sequestration
carbon_sequestration_names = {
    'Carbon Sequestration|Direct Air Capture': 'CSeq|DAC',
    'Carbon Sequestration|CCS|Biomass': 'CSeq|CCS|Biomass',
    'Carbon Sequestration|CCS|Fossil': 'CSeq|CCS|Fossil',
    'Carbon Sequestration|CCS|Fossil|Energy|Demand|Industry': 'CSeq|CCS|Fossil|Industry',
    'Carbon Sequestration|CCS|Fossil|Energy|Supply': 'CSeq|CCS|Fossil|Supply',
    # 'Carbon Sequestration|CCS': 'CSeq|CCS',
    # 'Carbon Sequestration|CCS|Biomass|Energy|Supply': 'CSeq|CCS|Biomass|Supply',
    # 'Carbon Sequestration|CCS|Biomass|Energy|Supply|Electricity': 'CSeq|CCS|Biomass|Supply|Elec',
    # 'Carbon Sequestration|CCS|Biomass|Energy|Supply|Liquids': 'CSeq|CCS|Biomass|Supply|Liquids',
    # 'Carbon Sequestration|CCS|Biomass|Energy|Supply|Hydrogen': 'CSeq|CCS|Biomass|Supply|H2',
    # 'Carbon Sequestration|CCS|Biomass|Energy|Demand|Industry': 'CSeq|CCS|Biomass|Industry',
    # 'Carbon Sequestration|CCS|Fossil|Energy|Supply|Electricity': 'CSeq|CCS|Fossil|Supply|Elec',
    # 'Carbon Sequestration|CCS|Fossil|Energy|Supply|Hydrogen': 'CSeq|CCS|Fossil|Supply|H2',
    # 'Carbon Sequestration|CCS|Fossil|Energy|Supply|Liquids': 'CSeq|CCS|Fossil|Supply|Liquids',
    # 'Carbon Sequestration|CCS|Industrial Processes': 'CSeq|CCS|IndProc',
    # 'Carbon Sequestration|CCS|Direct Air Capture': 'CSeq|CCS|DAC',
    # 'Carbon Sequestration|Land Use': 'CSeq|Land Use',
    # 'Carbon Sequestration|CCS|Industry': 'CSeq|CCS|Industry',
}

# Land use sequestration (all commented in original list)
land_use_sequestration_names = {
    # 'Carbon Sequestration|Land Use|Afforestation': 'CSeq|Land Use|Afforestation',
    # 'Carbon Sequestration|Land Use|Agriculture': 'CSeq|Land Use|Agriculture',
    # 'Carbon Sequestration|Land Use|Forest Management': 'CSeq|Land Use|Forest Management',
    # 'Carbon Sequestration|Land Use|Other': 'CSeq|Land Use|Other',
    # 'Carbon Sequestration|Land Use|Other LUC': 'CSeq|Land Use|Other LUC',
}

# Carbon dioxide removal (all commented in original list)
carbon_dioxide_removal_names = {
    # 'Carbon Sequestration|Direct Air Capture': 'CDR|DAC',
    # 'Carbon Sequestration|Ocean': 'CDR|Ocean',
    # 'Carbon Sequestration|Soil Carbon': 'CDR|Soil Carbon',
    # 'Carbon Sequestration|Land Use|Afforestation': 'CDR|Land Use|Afforestation',
    # 'Carbon Sequestration|Land Use|Agriculture': 'CDR|Land Use|Agriculture',
    # 'Carbon Sequestration|Land Use|Forest Management': 'CDR|Land Use|Forest Management',
    # 'Carbon Sequestration|Land Use|Other': 'CDR|Land Use|Other',
    # 'Carbon Sequestration|Land Use|Other LUC': 'CDR|Land Use|Other LUC',
    # 'Carbon Removal': 'CDR',
    # 'Carbon Removal|Geological Storage|Direct Air Capture': 'CDR|Geol|DAC',
    # 'Carbon Removal|Geological Storage': 'CDR|Geol',
    # 'Carbon Removal|Geological Storage|Biomass': 'CDR|Geol|Biomass',
    # 'Carbon Removal|Land Use': 'CDR|Land Use',
    # 'Carbon Capture|Geological Storage|Direct Air Capture': 'CDR|Geol|DAC',
    # 'Carbon Capture|Geological Storage|Other Sources': 'CDR|Geol|Other',
    # 'Carbon Capture|Industrial Processes': 'CDR|IndProc',
    # 'Gross Removals|CO2': 'Gross Removals|CO2',
}

# Overall picture (Timeseries Variables)
timeseries_variables_names = {
    'Carbon Sequestration|CCS': 'CSeq|CCS',
    'Final Energy': 'Final Energy',
    'Capacity|Electricity': 'Cap|Elec',
    'CO2|Energy and Industrial Processes': 'CO2|Energy and IndProc',
    'Emissions|CO2|Energy and Industrial Processes': 'CO2|Energy and IndProc',
    'Final Energy|Electricity': 'FE|Electricity',
    # 'Carbon Sequestration|Land Use': 'CSeq|Land Use',
    # 'Primary Energy': 'Primary Energy',
    # 'GDP|PPP': 'GDP|PPP',
    # 'Emissions|CO2': 'CO2 Emissions',
    # 'Temperature|Global Mean': 'Temperature|Global Mean',
    # 'Investment|Energy Supply|Electricity': 'Inv|Elec',
    # 'Land Cover': 'Land Cover',
    # 'Secondary Energy': 'Secondary Energy',
    # 'Capacity Additions|Electricity': 'CapAdd|Elec',
    # 'Price|Carbon': 'Price|Carbon',
}

# Investment in energy supply (all commented in original list)
energy_investment_names = {
    # 'Investment|Energy Supply|CO2 Transport and Storage': 'Inv|CO2 T&S',
    # 'Investment|Energy Supply|Electricity': 'Inv|Elec',
    # 'Investment|Energy Supply|Heat': 'Inv|Heat',
    # 'Investment|Energy Supply|Hydrogen': 'Inv|H2',
    # 'Investment|Energy Supply|Liquids': 'Inv|Liquids',
    # 'Investment|Energy Supply|Other': 'Inv|Other',
    # 'Investment|Energy Supply|Electricity|Biomass|w/ CCS': 'Inv|Elec|Biomass|w/ CCS',
    # 'Investment|Energy Supply|Electricity|Biomass|w/o CCS': 'Inv|Elec|Biomass|w/o CCS',
    # 'Investment|Energy Supply|Electricity|Coal|w/ CCS': 'Inv|Elec|Coal|w/ CCS',
    # 'Investment|Energy Supply|Electricity|Coal|w/o CCS': 'Inv|Elec|Coal|w/o CCS',
    # 'Investment|Energy Supply|Electricity|Gas|w/ CCS': 'Inv|Elec|Gas|w/ CCS',
    # 'Investment|Energy Supply|Electricity|Gas|w/o CCS': 'Inv|Elec|Gas|w/o CCS',
    # 'Investment|Energy Supply|Electricity|Oil|w/ CCS': 'Inv|Elec|Oil|w/ CCS',
    # 'Investment|Energy Supply|Electricity|Oil|w/o CCS': 'Inv|Elec|Oil|w/o CCS',
    # 'Investment|Energy Supply|Electricity|Solar': 'Inv|Elec|Solar',
    # 'Investment|Energy Supply|Electricity|Wind': 'Inv|Elec|Wind',
    # 'Investment|Energy Supply|Electricity|Geothermal': 'Inv|Elec|Geothermal',
    # 'Investment|Energy Supply|Electricity|Hydro': 'Inv|Elec|Hydro',
    # 'Investment|Energy Supply|Electricity|Nuclear': 'Inv|Elec|Nuclear',
    # 'Investment|Energy Supply|Electricity|Transmission and Distribution': 'Inv|Elec|T&D',
}

# Primary energy (all commented in original list)
primary_energy_names = {
    # 'Primary Energy|Biomass': 'PE|Biomass',
    # 'Primary Energy|Biomass|w/ CCS': 'PE|Biomass|w/ CCS',
    # 'Primary Energy|Biomass|w/o CCS': 'PE|Biomass|w/o CCS',
    # 'Primary Energy|Coal': 'PE|Coal',
    # 'Primary Energy|Coal|w/ CCS': 'PE|Coal|w/ CCS',
    # 'Primary Energy|Coal|w/o CCS': 'PE|Coal|w/o CCS',
    # 'Primary Energy|Gas': 'PE|Gas',
    # 'Primary Energy|Gas|w/ CCS': 'PE|Gas|w/ CCS',
    # 'Primary Energy|Gas|w/o CCS': 'PE|Gas|w/o CCS',
    # 'Primary Energy|Geothermal': 'PE|Geothermal',
    # 'Primary Energy|Hydro': 'PE|Hydro',
    # 'Primary Energy|Nuclear': 'PE|Nuclear',
    # 'Primary Energy|Ocean': 'PE|Ocean',
    # 'Primary Energy|Oil': 'PE|Oil',
    # 'Primary Energy|Oil|w/ CCS': 'PE|Oil|w/ CCS',
    # 'Primary Energy|Oil|w/o CCS': 'PE|Oil|w/o CCS',
    # 'Primary Energy|Other': 'PE|Other',
    # 'Primary Energy|Secondary Energy Trade': 'PE|Secondary Energy Trade',
    # 'Primary Energy|Solar': 'PE|Solar',
    # 'Primary Energy|Wind': 'PE|Wind',
    # 'Primary Energy|Non-Biomass Renewables': 'PE|Non-Bio Renewables',
}

# Final energy by carriers
final_energy_by_carriers_names = {
    'Final Energy|Electricity': 'FE|Electricity',
    'Final Energy|Gases': 'FE|Gases',
    'Final Energy|Heat': 'FE|Heat',
    'Final Energy|Liquids': 'FE|Liquids',
    'Final Energy|Solids': 'FE|Solids',
    # 'Final Energy|Solids|Biomass': 'FE|Solids|Biomass',
    # 'Final Energy|Solids|Biomass|Traditional': 'FE|Solids|Biomass|Trad',
    # 'Final Energy|Solids|Coal': 'FE|Solids|Coal',
    # 'Final Energy|Other Sector': 'FE|Other Sector',
}

# Final energy by sources
final_energy_by_sources_names = {
    'Final Energy|Geothermal': 'FE|Geothermal',
    'Final Energy|Solar': 'FE|Solar',
    'Final Energy|Hydrogen': 'FE|Hydrogen',
}

# Finals by sector
finals_by_sector_names = {
    'Final Energy|Industry': 'FE|Industry',
    'Final Energy|Non-Energy Use': 'FE|Non-Energy Use',
    'Final Energy|Residential and Commercial': 'FE|Res & Com',
    'Final Energy|Transportation': 'FE|Transportation',
    # 'Final Energy|Agriculture': 'FE|Agriculture',
    # 'Final Energy|Bunkers': 'FE|Bunkers',
    # 'Final Energy|Commercial': 'FE|Commercial',
    # 'Final Energy|Residential': 'FE|Residential',
    # 'Final Energy|Transportation (w/ bunkers)': 'FE|Transport (w/ bunkers)',
    # 'Final Energy|Other Sector': 'FE|Other Sector',
    # 'Final Energy|Non-Energy Use|Coal': 'FE|Non-Energy Use|Coal',
    # 'Final Energy|Non-Energy Use|Gas': 'FE|Non-Energy Use|Gas',
    # 'Final Energy|Non-Energy Use|Oil': 'FE|Non-Energy Use|Oil',
    # 'Final Energy|Non-Energy Use|Biomass': 'FE|Non-Energy Use|Biomass',
}

# Final energy by sector for electricity
finals_by_sector_electricity_names = {
    'Final Energy|Industry|Electricity': 'FE|Ind|Electricity',
    'Final Energy|Residential and Commercial|Electricity': 'FE|ResCom|Electricity',
    'Final Energy|Transportation|Electricity': 'FE|Transport|Electricity',
}

# Secondary energy (Electricity)
secondary_energy_electricity_names = {
    'Secondary Energy|Electricity|Biomass': 'SE|Elec|Biomass',
    'Secondary Energy|Electricity|Coal': 'SE|Elec|Coal',
    'Secondary Energy|Electricity|Gas': 'SE|Elec|Gas',
    'Secondary Energy|Electricity|Oil': 'SE|Elec|Oil',
    'Secondary Energy|Electricity|Geothermal': 'SE|Elec|Geothermal',
    'Secondary Energy|Electricity|Hydro': 'SE|Elec|Hydro',
    'Secondary Energy|Electricity|Nuclear': 'SE|Elec|Nuclear',
    'Secondary Energy|Electricity|Solar': 'SE|Elec|Solar',
    'Secondary Energy|Electricity|Wind': 'SE|Elec|Wind',
    'Secondary Energy|Electricity|Ocean': 'SE|Elec|Ocean',
    # 'Secondary Energy|Electricity|Biomass|w/ CCS': 'SE|Elec|Biomass|w/ CCS',
    # 'Secondary Energy|Electricity|Biomass|w/o CCS': 'SE|Elec|Biomass|w/o CCS',
    # 'Secondary Energy|Electricity|Coal|w/ CCS': 'SE|Elec|Coal|w/ CCS',
    # 'Secondary Energy|Electricity|Coal|w/o CCS': 'SE|Elec|Coal|w/o CCS',
    # 'Secondary Energy|Electricity|Gas|w/ CCS': 'SE|Elec|Gas|w/ CCS',
    # 'Secondary Energy|Electricity|Gas|w/o CCS': 'SE|Elec|Gas|w/o CCS',
    # 'Secondary Energy|Electricity|Oil|w/o CCS': 'SE|Elec|Oil|w/o CCS',
    # 'Secondary Energy|Electricity|Non-Biomass Renewables': 'SE|Elec|Non-Bio Renewables',
    # 'Secondary Energy|Electricity|Solar|CSP': 'SE|Elec|Solar|CSP',
    # 'Secondary Energy|Electricity|Solar|PV': 'SE|Elec|Solar|PV',
    # 'Secondary Energy|Electricity|Wind|Offshore': 'SE|Elec|Wind|Offshore',
    # 'Secondary Energy|Electricity|Wind|Onshore': 'SE|Elec|Wind|Onshore',
}

# Secondary energy (Non-Electric)
secondary_energy_non_electric_names = {
    'Secondary Energy|Gases': 'SE|Gases',
    'Secondary Energy|Hydrogen': 'SE|Hydrogen',
    'Secondary Energy|Liquids': 'SE|Liquids',
    'Secondary Energy|Solids': 'SE|Solids',
    # 'Secondary Energy|Hydrogen|Electricity': 'SE|Hydrogen|Electricity',
    # 'Secondary Energy|Hydrogen|Fossil': 'SE|Hydrogen|Fossil',
    # 'Secondary Energy|Hydrogen|Fossil|w/ CCS': 'SE|Hydrogen|Fossil|w/ CCS',
    # 'Secondary Energy|Hydrogen|Fossil|w/o CCS': 'SE|Hydrogen|Fossil|w/o CCS',
    # 'Secondary Energy|Liquids|Biomass': 'SE|Liquids|Biomass',
    # 'Secondary Energy|Liquids|Biomass|w/ CCS': 'SE|Liquids|Biomass|w/ CCS',
    # 'Secondary Energy|Liquids|Biomass|w/o CCS': 'SE|Liquids|Biomass|w/o CCS',
    # 'Secondary Energy|Liquids|Gas': 'SE|Liquids|Gas',
    # 'Secondary Energy|Liquids|Gas|w/o CCS': 'SE|Liquids|Gas|w/o CCS',
    # 'Secondary Energy|Liquids|Oil': 'SE|Liquids|Oil',
}

# Residential final energy (all commented in original list)
residential_final_energy_names = {
    # 'Final Energy|Residential and Commercial|Residential|Cooling': 'FE|Res|Cooling',
    # 'Final Energy|Residential and Commercial|Residential|Electricity': 'FE|Res|Electricity',
    # 'Final Energy|Residential and Commercial|Residential|Gases': 'FE|Res|Gases',
    # 'Final Energy|Residential and Commercial|Residential|Heat': 'FE|Res|Heat',
    # 'Final Energy|Residential and Commercial|Residential|Heating|Space': 'FE|Res|Heating|Space',
    # 'Final Energy|Residential and Commercial|Residential|Hydrogen': 'FE|Res|Hydrogen',
    # 'Final Energy|Residential and Commercial|Residential|Liquids': 'FE|Res|Liquids',
}

# Commercial final energy (all commented in original list)
commercial_final_energy_names = {
    # 'Final Energy|Residential and Commercial|Commercial|Cooling': 'FE|Com|Cooling',
    # 'Final Energy|Residential and Commercial|Commercial|Electricity': 'FE|Com|Electricity',
    # 'Final Energy|Residential and Commercial|Commercial|Gases': 'FE|Com|Gases',
    # 'Final Energy|Residential and Commercial|Commercial|Heat': 'FE|Com|Heat',
    # 'Final Energy|Residential and Commercial|Commercial|Heating|Space': 'FE|Com|Heating|Space',
    # 'Final Energy|Residential and Commercial|Commercial|Hydrogen': 'FE|Com|Hydrogen',
    # 'Final Energy|Residential and Commercial|Commercial|Liquids': 'FE|Com|Liquids',
    # 'Final Energy|Residential and Commercial|Commercial|Solids': 'FE|Com|Solids',
    # 'Final Energy|Residential and Commercial|Commercial|Solids|Biomass': 'FE|Com|Solids|Biomass',
    # 'Final Energy|Residential and Commercial|Commercial|Solids|Coal': 'FE|Com|Solids|Coal',
}

# Residential and commercial final energy (combined)
residential_commercial_final_energy_names = {
    'Final Energy|Residential and Commercial|Electricity': 'FE|ResCom|Electricity',
    'Final Energy|Residential and Commercial|Gases': 'FE|ResCom|Gases',
    'Final Energy|Residential and Commercial|Heat': 'FE|ResCom|Heat',
    'Final Energy|Residential and Commercial|Liquids': 'FE|ResCom|Liquids',
    'Final Energy|Residential and Commercial|Hydrogen': 'FE|ResCom|Hydrogen',
    'Final Energy|Residential and Commercial|Solids': 'FE|ResCom|Solids',
    # 'Final Energy|Residential and Commercial|Cooling': 'FE|ResCom|Cooling',
    # 'Final Energy|Residential and Commercial|Heating': 'FE|ResCom|Heating',
    # 'Final Energy|Residential and Commercial|Heat|Space': 'FE|ResCom|Heat|Space',
    # 'Final Energy|Residential and Commercial|Solids|Biomass': 'FE|ResCom|Solids|Biomass',
    # 'Final Energy|Residential and Commercial|Solids|Biomass|Traditional': 'FE|ResCom|Solids|Biomass|Trad',
    # 'Final Energy|Residential and Commercial|Solids|Coal': 'FE|ResCom|Solids|Coal',
    # 'Final Energy|Residential and Commercial|Other': 'FE|ResCom|Other',
}

# Final energy transport by mode (all commented in original list)
transport_mode_final_energy_names = {
    # 'Final Energy|Transportation|Domestic Aviation': 'FE|Transport|Dom Aviation',
    # 'Final Energy|Transportation|Domestic Shipping': 'FE|Transport|Dom Shipping',
    # 'Final Energy|Transportation|Bus': 'FE|Transport|Bus',
    # 'Final Energy|Transportation|Light-Duty Vehicle': 'FE|Transport|LDV',
    # 'Final Energy|Transportation|Truck': 'FE|Transport|Truck',
    # 'Final Energy|Transportation|Aviation': 'FE|Transport|Aviation',
    # 'Final Energy|Transportation|Aviation|Passenger': 'FE|Transport|Aviation|Passenger',
    # 'Final Energy|Transportation|Freight': 'FE|Transport|Freight',
    # 'Final Energy|Transportation|Freight|Electricity': 'FE|Transport|Freight|Electricity',
    # 'Final Energy|Transportation|Freight|Hydrogen': 'FE|Transport|Freight|Hydrogen',
    # 'Final Energy|Transportation|Freight|Liquids': 'FE|Transport|Freight|Liquids',
    # 'Final Energy|Transportation|Freight|Other': 'FE|Transport|Freight|Other',
    # 'Final Energy|Transportation|Maritime': 'FE|Transport|Maritime',
    # 'Final Energy|Transportation|Maritime|Freight': 'FE|Transport|Maritime|Freight',
    # 'Final Energy|Transportation|Other': 'FE|Transport|Other',
    # 'Final Energy|Transportation|Passenger': 'FE|Transport|Passenger',
    # 'Final Energy|Transportation|Passenger|Electricity': 'FE|Transport|Passenger|Electricity',
    # 'Final Energy|Transportation|Passenger|Gases': 'FE|Transport|Passenger|Gases',
    # 'Final Energy|Transportation|Passenger|Hydrogen': 'FE|Transport|Passenger|Hydrogen',
    # 'Final Energy|Transportation|Passenger|Liquids': 'FE|Transport|Passenger|Liquids',
    # 'Final Energy|Transportation|Rail': 'FE|Transport|Rail',
    # 'Final Energy|Transportation|Rail|Freight': 'FE|Transport|Rail|Freight',
    # 'Final Energy|Transportation|Rail|Passenger': 'FE|Transport|Rail|Passenger',
    # 'Final Energy|Transportation|Road': 'FE|Transport|Road',
    # 'Final Energy|Transportation|Road|Freight': 'FE|Transport|Road|Freight',
    # 'Final Energy|Transportation|Road|Passenger': 'FE|Transport|Road|Passenger',
    # 'Final Energy|Transportation|Road|Passenger|2W&3W': 'FE|Transport|Road|Passenger|2W&3W',
    # 'Final Energy|Transportation|Road|Passenger|4W': 'FE|Transport|Road|Passenger|4W',
    # 'Final Energy|Transportation|Road|Passenger|Bus': 'FE|Transport|Road|Passenger|Bus',
}

# Final energy transport by carrier
transport_carrier_final_energy_names = {
    'Final Energy|Transportation|Electricity': 'FE|Transport|Electricity',
    'Final Energy|Transportation|Gases': 'FE|Transport|Gases',
    'Final Energy|Transportation|Hydrogen': 'FE|Transport|Hydrogen',
    'Final Energy|Transportation|Liquids': 'FE|Transport|Liquids',
    'Final Energy|Transportation|Solids': 'FE|Transport|Solids',
    # 'Final Energy|Transportation|Other': 'FE|Transport|Other',
    # 'Final Energy|Transportation|Liquids|Biomass': 'FE|Transport|Liquids|Biomass',
    # 'Final Energy|Transportation|Liquids|Oil': 'FE|Transport|Liquids|Oil',
}

# Final energy industry by carrier
industry_carrier_final_energy_names = {
    'Final Energy|Industry|Electricity': 'FE|Ind|Electricity',
    'Final Energy|Industry|Gases': 'FE|Ind|Gases',
    'Final Energy|Industry|Heat': 'FE|Ind|Heat',
    'Final Energy|Industry|Hydrogen': 'FE|Ind|Hydrogen',
    'Final Energy|Industry|Liquids': 'FE|Ind|Liquids',
    'Final Energy|Industry|Other': 'FE|Ind|Other',
    'Final Energy|Industry|Solids': 'FE|Ind|Solids',
    # 'Final Energy|Industry|Solids|Biomass': 'FE|Ind|Solids|Biomass',
    # 'Final Energy|Industry|Solids|Coal': 'FE|Ind|Solids|Coal',
}

# Final energy industry by subsector (all commented in original list)
industry_subsector_final_energy_names = {
    # 'Final Energy|Industry|Cement': 'FE|Ind|Cement',
    # 'Final Energy|Industry|Cement|Electricity': 'FE|Ind|Cement|Electricity',
    # 'Final Energy|Industry|Cement|Gases': 'FE|Ind|Cement|Gases',
    # 'Final Energy|Industry|Chemicals': 'FE|Ind|Chemicals',
    # 'Final Energy|Industry|Chemicals|Ammonia': 'FE|Ind|Chemicals|Ammonia',
    # 'Final Energy|Industry|Chemicals|Ammonia|Gases': 'FE|Ind|Chemicals|Ammonia|Gases',
    # 'Final Energy|Industry|Chemicals|Ammonia|Hydrogen': 'FE|Ind|Chemicals|Ammonia|Hydrogen',
    # 'Final Energy|Industry|Chemicals|Ammonia|Liquids': 'FE|Ind|Chemicals|Ammonia|Liquids',
    # 'Final Energy|Industry|Chemicals|Ammonia|Solids': 'FE|Ind|Chemicals|Ammonia|Solids',
    # 'Final Energy|Industry|Chemicals|Ammonia|Solids|Fossil': 'FE|Ind|Chemicals|Ammonia|Solids|Fossil',
    # 'Final Energy|Industry|Chemicals|Electricity': 'FE|Ind|Chemicals|Electricity',
    # 'Final Energy|Industry|Chemicals|Gases': 'FE|Ind|Chemicals|Gases',
    # 'Final Energy|Industry|Chemicals|Heat': 'FE|Ind|Chemicals|Heat',
    # 'Final Energy|Industry|Chemicals|Hydrogen': 'FE|Ind|Chemicals|Hydrogen',
    # 'Final Energy|Industry|Chemicals|Liquids': 'FE|Ind|Chemicals|Liquids',
    # 'Final Energy|Industry|Chemicals|Solids': 'FE|Ind|Chemicals|Solids',
    # 'Final Energy|Industry|Chemicals|Solids|Bioenergy': 'FE|Ind|Chemicals|Solids|Bioenergy',
    # 'Final Energy|Industry|Chemicals|Solids|Fossil': 'FE|Ind|Chemicals|Solids|Fossil',
    # 'Final Energy|Industry|Non-ferrous metals': 'FE|Ind|Non-ferrous metals',
    # 'Final Energy|Industry|Non-ferrous metals|Electricity': 'FE|Ind|Non-ferrous metals|Electricity',
    # 'Final Energy|Industry|Non-ferrous metals|Gases': 'FE|Ind|Non-ferrous metals|Gases',
    # 'Final Energy|Industry|Non-ferrous metals|Liquids': 'FE|Ind|Non-ferrous metals|Liquids',
    # 'Final Energy|Industry|Non-ferrous metals|Solids': 'FE|Ind|Non-ferrous metals|Solids',
    # 'Final Energy|Industry|Non-ferrous metals|Solids|Bioenergy': 'FE|Ind|Non-ferrous metals|Solids|Bioenergy',
    # 'Final Energy|Industry|Non-ferrous metals|Solids|Fossil': 'FE|Ind|Non-ferrous metals|Solids|Fossil',
    # 'Final Energy|Industry|Steel': 'FE|Ind|Steel',
    # 'Final Energy|Industry|Steel|Electricity': 'FE|Ind|Steel|Electricity',
    # 'Final Energy|Industry|Steel|Hydrogen': 'FE|Ind|Steel|Hydrogen',
    # 'Final Energy|Industry|Steel|Liquids': 'FE|Ind|Steel|Liquids',
    # 'Final Energy|Industry|Steel|Solids': 'FE|Ind|Steel|Solids',
    # 'Final Energy|Industry|Steel|Solids|Bioenergy': 'FE|Ind|Steel|Solids|Bioenergy',
    # 'Final Energy|Industry|Steel|Solids|Fossil': 'FE|Ind|Steel|Solids|Fossil',
}

# CO2 Emissions from transport (all commented in original list)
CO2_emissions_transport_names = {
    # 'Emissions|CO2|Energy|Demand|Transportation|Freight': 'CO2|Transport|Freight',
    # 'Emissions|CO2|Energy|Demand|Transportation|Passenger': 'CO2|Transport|Passenger',
    # 'Emissions|CO2|Energy|Demand|Transportation': 'CO2|Transport',
}

# --- Combine all renaming dictionaries ---
all_vars_names = {}
all_vars_names.update(capacity_additions_names)
all_vars_names.update(overall_capacity_names)
all_vars_names.update(emissions_names)
all_vars_names.update(CO2_emissions_names)
all_vars_names.update(carbon_sequestration_names)
all_vars_names.update(land_use_sequestration_names)
all_vars_names.update(carbon_dioxide_removal_names)
all_vars_names.update(timeseries_variables_names)
all_vars_names.update(energy_investment_names)
all_vars_names.update(primary_energy_names)
all_vars_names.update(final_energy_by_carriers_names)
all_vars_names.update(final_energy_by_sources_names)
all_vars_names.update(finals_by_sector_names)
all_vars_names.update(finals_by_sector_electricity_names)
all_vars_names.update(secondary_energy_electricity_names)
all_vars_names.update(secondary_energy_non_electric_names)
all_vars_names.update(residential_final_energy_names)
all_vars_names.update(commercial_final_energy_names)
all_vars_names.update(residential_commercial_final_energy_names)
all_vars_names.update(transport_mode_final_energy_names)
all_vars_names.update(transport_carrier_final_energy_names)
all_vars_names.update(industry_carrier_final_energy_names)
all_vars_names.update(industry_subsector_final_energy_names)
all_vars_names.update(CO2_emissions_transport_names)


# # 4) Plotting Functions

# In[17]:


# --------------------------
# Set up the style parameters
# --------------------------
sns.set()
sns.set_style("white")
sns.set_context("talk")
# sns.set_palette("colorblind")
plt.rcParams['figure.dpi']= 100
plt.rc("savefig", dpi=150)
plt.rc("font", size=14)
# Name of the scenarios on plots
scenario_names = {
    'NDC_EI_DERP2_HD': 'D2_NDC',
    'HD_ER_RCP85_1_CDD_30_20': 'D1_ER_1RCP85_CDD_30_20',
    'HD_ER_RCP85_2_CDD_30_20': 'D1_ER_2RCP85_CDD_30_20',
    'HD_ER_RCP85_3_CDD_30_20': 'D1_ER_3RCP85_CDD_30_20',
    'HD_ER_RCP85_4_CDD_30_20': 'D1_ER_4RCP85_CDD_30_20',
    'HD_ER_RCP85_5_CDD_30_20': 'D1_ER_5RCP85_CDD_30_20',
    'HD_ER_RCP85_1_CDD_20_10': 'D1_ER_1RCP85_CDD_20_10',
    'HD_ER_RCP85_2_CDD_20_10': 'D1_ER_2RCP85_CDD_20_10',
    'HD_ER_RCP85_3_CDD_20_10': 'D1_ER_3RCP85_CDD_20_10',
    'HD_ER_RCP85_4_CDD_20_10': 'D1_ER_4RCP85_CDD_20_10',
    'HD_ER_RCP85_5_CDD_20_10': 'D1_ER_5RCP85_CDD_20_10',
    'HD_IR_RCP26_1_CDD_20_10_nCAP': 'D4_IR_1RCP26_CDD_20_10_nCAP',
    'HD_IR_RCP26_1_CDD_30_20_nCAP': 'D4_IR_1RCP26_CDD_30_20_nCAP',
    'HD_IR_RCP85_1_CDD_20_10_nCAP': 'D4_IR_1RCP85_CDD_20_10_nCAP',
    'HD_ER_RCP85_1_CDD_20_10_nCAP': 'D4_IR_1RCP85_CDD_20_10_nCAP',

    'HD_IR_RCP85_1_CDD_30_20_nCAP': 'D4_IR_1RCP85_CDD_30_20_nCAP',
    'HD_IR_RCP85_5_CDD_30_20_nCAP': 'D4_IR_5RCP85_CDD_30_20_nCAP',

}



# Dictionary for the colors based on scenario
colours = {
    'HD_ER_RCP85_1_CDD_20_10': '#FF7F00',  # orange
    # 'HD_ER_RCP85_1_CDD_30_20': 'blue',
    # 'HD_ER_RCP85_2_CDD_20_10': 'magenta',
    # 'HD_ER_RCP85_2_CDD_30_20': 'green',
    # 'HD_ER_RCP85_3_CDD_20_10': 'red',
    # 'HD_ER_RCP85_3_CDD_30_20': 'orange',
    # 'HD_ER_RCP85_4_CDD_20_10': 'pink',
    # 'HD_ER_RCP85_4_CDD_30_20': 'purple',
    # 'HD_ER_RCP85_5_CDD_20_10': 'grey',
    # 'HD_ER_RCP85_5_CDD_30_20': 'brown',

    'HD_IR_RCP85_1_CDD_20_10_nCAP': '#1F78B4',  # blue
    'HD_ER_RCP85_1_CDD_20_10_nCAP': '#1F78B4',  # blue
    
    # 'HD_IR_RCP26_1_CDD_20_10_nCAP': 'lightgreen',     
    # 'HD_IR_RCP26_1_CDD_30_20_nCAP': 'darkgreen',      
    # 'HD_IR_RCP85_1_CDD_30_20_nCAP': 'darkviolet',     
    # 'HD_IR_RCP85_5_CDD_30_20_nCAP': 'goldenrod',      

    'NDC_EI_DERP2_HD': '#000000',  # black
    # '#008000',  # green
}

# Dictionary for line styles based on model
model_linestyles = {
    'GCAM 7.0': '-',           # solid
    'TIAM_Grantham': '--',     # dashed
    'FRIDAv2.1': ':',          # dotted
    'PROMETHEUS': '-.',        # dash-dot
}


# Define a safe function to sanitise the variable name for saving files
def sanitize_filename(filename):
    return filename.replace("|", "_").replace("/", "_").replace("*", "")


# In[18]:


# Define regions of interest
regions_of_interest = ["World"]

# Define scenarios of interest
scenarios_of_interest = [
'HD_ER_RCP85_1_CDD_20_10',
#  'HD_ER_RCP85_1_CDD_30_20',
#  'HD_ER_RCP85_2_CDD_20_10',
#  'HD_ER_RCP85_2_CDD_30_20',
#  'HD_ER_RCP85_3_CDD_20_10',
#  'HD_ER_RCP85_3_CDD_30_20',
#  'HD_ER_RCP85_4_CDD_20_10',
#  'HD_ER_RCP85_4_CDD_30_20',
#  'HD_ER_RCP85_5_CDD_20_10',
#  'HD_ER_RCP85_5_CDD_30_20',
#  'HD_IR_RCP26_1_CDD_20_10_nCAP',
#  'HD_IR_RCP26_1_CDD_30_20_nCAP',

 # 'HD_IR_RCP85_1_CDD_20_10_nCAP',
 'HD_ER_RCP85_1_CDD_20_10_nCAP',

#  'HD_IR_RCP85_1_CDD_30_20_nCAP',
#  'HD_IR_RCP85_5_CDD_30_20_nCAP',
 'NDC_EI_DERP2_HD'
]

# Define models of interest
models_of_interest = ["GCAM 7.0", 'FRIDAv2.1',
                      'TIAM_Grantham', 
                      ]

# Define variables to plot
variables_to_plot = timeseries_variables 

# # Then call the function with your predefined lists
# plot_timeseries_by_region(
#     df=your_dataframe,  # Your pyam DataFrame
#     variables=variables_to_plot,
#     all_vars_names=all_vars_names,
#     regions=regions_of_interest,
#     scenarios=scenarios_of_interest,
#     models=models_of_interest
# )

# # ALTERNATIVE: Plot with all scenarios but specific regions
# # --------------------------------------------------------
# plot_timeseries_by_region(
#     df=your_dataframe,
#     variables=variables_to_plot,
#     all_vars_names=all_vars_names,
#     regions=regions_of_interest,
#     # No scenarios specified - will use all available
#     models=models_of_interest
# )

# # ALTERNATIVE: Focus on a single region with all models
# # ----------------------------------------------------
# plot_timeseries_by_region(
#     df=your_dataframe,
#     variables=variables_to_plot,
#     all_vars_names=all_vars_names,
#     regions=["World"],
#     scenarios=scenarios_of_interest
#     # No models specified - will use all available
# )


#  # 5) Polar charts to show differences

# In[19]:


groups = {
    # 'secondary_energy_non_electric': secondary_energy_non_electric,

    'Installed Electricity Capacity': overall_capacity_electricity,
    'Carbon Capture and Storage': carbon_sequestration,
    'Final Energy by Carriers': final_energy_by_carriers,
    'Final Energy by Sources': final_energy_by_sources,
    'Final Energy by Sector': finals_by_sector,
    'Electricity Use by Sector': finals_by_sector_electricity,
    'Electricity Generation by Source': secondary_energy_electricity,
    'Buildings Energy Demand': residential_commercial_final_energy,
    'Transport Energy by Carrier': transport_carrier_final_energy,
    'Industry Energy by Carrier': industry_carrier_final_energy,

}



# In[20]:


# First, prepare your data with baseline comparisons
baseline_scenario = 'NDC_EI_DERP2_HD'

# Create the df_with_changes DataFrame 
if 'baseline_value' not in df.data.columns:
    # Create a DataFrame with baseline values
    baseline_df = df.data[df.data['scenario'] == baseline_scenario].copy()
    baseline_df = baseline_df.rename(columns={'value': 'baseline_value'})
    baseline_df = baseline_df[['model', 'region', 'variable', 'year', 'baseline_value']]

    # Merge with original data and calculate changes
    merged_df = pd.merge(df.data, baseline_df, on=['model', 'region', 'variable', 'year'], how='left')
    merged_df['delta'] = merged_df['value'] - merged_df['baseline_value']
    merged_df['percentage_change'] = (merged_df['delta'] / merged_df['baseline_value']) * 100

    # Replace infinite values (from division by zero) with NaN
    merged_df.replace([np.inf, -np.inf], np.nan, inplace=True)

    # Store the enhanced DataFrame
    df_with_changes = merged_df
else:
    df_with_changes = df.data


# In[21]:


df_with_changes.query('scenario == "HD_ER_RCP85_1_CDD_20_10" & region == "World" & variable == "Final Energy|Industry|Electricity"').head(2040)


# In[22]:


# Find rows where percentage_change is NaN
missing_percentage = df_with_changes[df_with_changes['percentage_change'].isna()]

# Categorize the reason for missing data
missing_percentage['reason'] = 'Unknown'
missing_percentage.loc[missing_percentage['baseline_value'].isna(), 'reason'] = 'No Baseline Data'
missing_percentage.loc[(missing_percentage['baseline_value'] == 0) & 
                       (missing_percentage['reason'] == 'Unknown'), 'reason'] = 'Division by Zero'

# Count missing values by reason
missing_counts = missing_percentage['reason'].value_counts()
print("Missing percentage change counts by reason:")
print(missing_counts)

# Examine missing data for a specific scenario/region/variable combination
specific_missing = missing_percentage.query('scenario == "HD_ER_RCP85_1_CDD_20_10" & region == "World" & variable == "Final Energy|Industry|Electricity"')
print("\nMissing data for specific combination:")
print(specific_missing[['model', 'year', 'value', 'baseline_value', 'reason']])


# In[23]:


# For all models calculate the share of Final Energy|Electricity of total Final Energy
# Calculate electricity share of total final energy
electricity_var = 'Final Energy|Electricity'
total_var = 'Final Energy'

# Extract data for both variables
electricity_df = df.filter(variable=electricity_var).data
total_df = df.filter(variable=total_var).data

# Rename value columns for clarity
electricity_df = electricity_df.rename(columns={'value': 'electricity_value'})
total_df = total_df.rename(columns={'value': 'total_value'})

# Merge the dataframes
merged = pd.merge(
    electricity_df[['model', 'scenario', 'region', 'year', 'electricity_value']],
    total_df[['model', 'scenario', 'region', 'year', 'total_value']],
    on=['model', 'scenario', 'region', 'year'],
    how='inner'
)

# Calculate the share
merged['electricity_share'] = (merged['electricity_value'] / merged['total_value']) * 100

# Handle any division by zero or invalid values
merged['electricity_share'].replace([np.inf, -np.inf], np.nan, inplace=True)

# Quick look at the results
print("Electricity share summary statistics by model:")
print(merged.groupby('model')['electricity_share'].describe())

# Check for any missing or problematic values
print("\nMissing electricity share values by model:")
print(merged[merged['electricity_share'].isna()].groupby('model').size())


# In[24]:


df_share = merged.query("region == 'World' & scenario == ['HD_ER_RCP85_1_CDD_20_10', 'HD_IR_RCP85_1_CDD_20_10_nCAP', 'NDC_EI_DERP2_HD'] & year == [2040, 2070, 2100]")



#%%

unc_dir = "../data/outputs/processed/with_elec_cap/plot_test/uncertainty"  

frida_unc_data = {}
frida_unc_data['Capacity|Electricity'] = {}

for scen in scenarios_of_interest:
    frida_unc_data['Capacity|Electricity'][scen] = {}
    
    for pct in ['5th', '95th']:
        df_in = pd.read_csv(f'{unc_dir}/FRIDA_{scen}_{pct}.csv')
        df_in = df_in.loc[df_in['Variable'] == 'Capacity|Electricity'].loc[:, '1980':'2150']
        frida_unc_data['Capacity|Electricity'][scen][pct] = df_in.values[0,:]/1000 # TW

 
perc_unc_file = "../data/outputs/for_supplement/perc_cap_dif.csv"   
df_perc_unc = pd.read_csv(perc_unc_file)

var_dict = {
     'Biomass':'Capacity|Biomass',
     'Wind':'Capacity|Electricity|Wind',
     'Solar':'Capacity|Electricity|Solar',
     'Oil':'Capacity|Oil',
     'Nuclear':'Capacity|Electricity|Nuclear',
     'Hydro':'Capacity|Electricity|Hydro',
     'Geothermal':'Capacity|Geothermal',
     'Gas':'Capacity|Gas',
     'Coal':'Capacity|Coal',
     }


# In[25]:


# =======================================
#  Heat- & Drought illustrative dashboard  
# =======================================

# ----------------------------------------------------------------
# 0.  (OPTIONAL) manual display-name overrides
#     ------------------------------------------------------------
#  • Uncomment & edit to rename scenarios / models in the legend
# ----------------------------------------------------------------
scenario_display = {
    "HD_ER_RCP85_1_CDD_20_10"     : "D1_ER",
    "HD_IR_RCP85_1_CDD_20_10_nCAP": "D4_IR",
    "HD_ER_RCP85_1_CDD_20_10_nCAP": "D4_IR",
    "NDC_EI_DERP2_HD"             : "D2_NDC",
}
# model_display = {
#     "GCAM 7.0"       : "GCAM",
#     "TIAM_Grantham"  : "TIAM",
#     "FRIDAv2.1"      : "FRIDA",
#     "PROMETHEUS"     : "PROM"
# }
# ----------------------------------------------------------------
# 1.  basic style helpers
# ----------------------------------------------------------------
model_linestyles = {
    "GCAM 7.0":        "-",
    "TIAM_Grantham":   "--",
    "FRIDAv2.1":       ":",
    "PROMETHEUS":      "-."
}
def _display_name(var: str, name_map: Dict[str, str]) -> str:
    return name_map.get(var, var.split("|")[-1])
def _model_markers(models: List[str]) -> Dict[str, str]:
    # base = ["P", "^", "s", "D", "v", "<", ">", "o"]
    base = ["P", "X", "s", "D", "v", "<", ">", "o"]
    return {m: base[i % len(base)] for i, m in enumerate(models)}

# ----------------------------------------------------------------
# 2.  individual panels
# ----------------------------------------------------------------
def plot_total_capacity_ax(df, *, ax, region, models, scenarios,
                           all_vars, colours, frida_unc=False, frida_unc_data):
    """Top-left panel – Total electricity capacity in TW."""
    dfv = (df.filter(variable="Capacity|Electricity", region=region)
             .filter(model=models).filter(scenario=scenarios))
    if dfv.empty:
        ax.text(.5, .5, "no data", ha="center", va="center"); ax.axis("off"); return

    for m in models:
        ls = model_linestyles.get(m, "-")
        for s in scenarios:
            seri = dfv.filter(model=m, scenario=s)
            if seri.empty: continue
            ts = (seri.timeseries().reset_index()
                       .melt(id_vars=["model","scenario","region","variable","unit"],
                             var_name="year", value_name="value"))
            ts["year"]  = pd.to_numeric(ts["year"], errors="coerce")
            ts["value"] = ts["value"] / 1_000   # → TW
            ax.plot(ts["year"], ts["value"],
                    color=colours.get(s, "black"), linestyle=ls, lw=2)

            if m == 'FRIDAv2.1' and frida_unc == True:
                ax.fill_between(ts["year"], frida_unc_data['Capacity|Electricity'][s]['5th'],
                        frida_unc_data['Capacity|Electricity'][s]['95th'],
                        color=colours.get(s, "black"), alpha=0.15, lw=0)
            

    # ax.set_xlim(2025, 2100)
    ax.set_xlim(1980, 2150)
    ax.set_xlabel("Year", fontsize=10)
    ax.set_ylabel("TW",  fontsize=10)
    ax.tick_params(axis="both", labelsize=10)
    ax.set_title("Total Electricity Capacity", fontsize=14, pad=6)
    ax.grid(True, ls="--", alpha=.3)
    

# ................................................................
def plot_elec_share_ax(ax, df_share, *, region,
                       base_scenario, compare_scenarios,
                       years, colours, m_mark,
                       bar_color="#bdbdbd", whisker_color="black", jitter=0.12):
    """Top-right panel – electricity share bars + dots."""
    years = [int(y) for y in (years if hasattr(years, "__iter__") else [years])]
    df_r  = df_share[df_share["region"] == region]

    stats = (df_r[df_r["scenario"] == base_scenario]
             .loc[lambda d: d["year"].isin(years)]
             .groupby("year")["electricity_share"]
             .agg(["mean", "min", "max"])
             .reindex(years))
    if stats["mean"].isna().all():
        ax.axis("off"); return

    means, x_pos = stats["mean"], np.arange(len(years))
    lowers, uppers = means - stats["min"], stats["max"] - means

    ax.bar(x_pos, means, yerr=[lowers, uppers],
           capsize=5, color=bar_color, edgecolor=bar_color,
           error_kw={"elinewidth":1.5, "ecolor":whisker_color, "capsize":5},
           width=.6, zorder=2)

    for s_idx, scen in enumerate(compare_scenarios):
        df_s = df_r[df_r["scenario"] == scen]
        if df_s.empty: continue
        for m_idx, model in enumerate(sorted(df_s["model"].unique())):
            df_m = df_s[(df_s["model"] == model) & (df_s["year"].isin(years))]
            offset = (-1)**s_idx * (jitter + m_idx*0.02)
            ax.scatter(x_pos + offset,
                       df_m.sort_values("year")["electricity_share"],
                       marker=m_mark[model], s=70, alpha=.7,
                       color=colours.get(scen, "black"),
                       edgecolors="dimgrey", linewidths=.3, zorder=3)

    ax.set_xticks(x_pos); ax.set_xticklabels(years, fontsize=10)
    ax.set_ylabel("(%)", fontsize=10)
    ax.tick_params(axis="y", labelsize=10)
    ax.set_title("Electricity Share in FE Compared to Current Trends", fontsize=14, pad=6)
    ax.grid(True, ls="--", alpha=.3)

# ................................................................
def plot_single_polar_ax(dfc, *, ax, region, year, variables,
                         models, scenarios, all_vars,
                         colours, m_mark,
                         var_label_fs=10, r_tick_fs=10, title_fs=14,
                         frida_unc = False, frida_unc_data):
    """One polar chart (bottom row)."""
    sub = (dfc[(dfc["region"]==region) & (dfc["year"]==year) &
               (dfc["variable"].isin(variables)) &
               (dfc["model"].isin(models)) &
               (dfc["scenario"].isin(scenarios))])
    if sub.empty:
        ax.text(.5, .5, "no data", ha="center", va="center"); ax.axis("off"); return

    sub["disp"] = sub["variable"].map(lambda v: _display_name(v, all_vars))
    # var_list, ang = sorted(sub["disp"].unique()), None
    var_list = var_dict.keys()
    ang = np.linspace(0, 2*np.pi, len(var_list), endpoint=False)
    pv = sub.pivot_table(index=["model","scenario"], columns="disp",
                         values="percentage_change", aggfunc="first")

    # limit = pv.loc[:, var_list].stack().abs().max(skipna=True) or 100
    # limit = 50 * math.ceil((limit*1.1)/50)
    # ax.set_ylim(-limit, limit)


    for m in models:
        mk = m_mark[m]
        for s in scenarios:
            print(s)
            
            if (m,s) not in pv.index: continue
            # vals, mask = pv.loc[(m,s), var_list], None
            # mask = vals.notna()
            # if mask.any() and m != 'FRIDAv2.1':
            #     ax.scatter(ang[mask], vals[mask],
            #                marker=mk, s=90, alpha=.75,
            #                color=colours.get(s, "grey"),
            #                edgecolors="dimgrey", linewidths=.3)
                
            if m == 'FRIDAv2.1' and frida_unc == True:
                
                for v_i, var in enumerate(var_list):
                    
                    med_val = df_perc_unc.loc[(df_perc_unc['Variable'] == var_dict[var]) &
                                              (df_perc_unc['Scenario'] == s) &
                                              (df_perc_unc['Percentile'] == 50)
                                              ][str(year)].values[0]
                    
                    ax.scatter(ang[v_i], med_val,
                               marker=mk, s=90, alpha=.75,
                               color=colours.get(s, "grey"),
                               edgecolors="dimgrey", linewidths=.3)
                    
                    unc_vals = np.asarray([
                        df_perc_unc.loc[(df_perc_unc['Variable'] == var_dict[var]) &
                            (df_perc_unc['Scenario'] == s) &
                            (df_perc_unc['Percentile'] == 5)
                            ][str(year)].values[0],
                        df_perc_unc.loc[(df_perc_unc['Variable'] == var_dict[var]) &
                            (df_perc_unc['Scenario'] == s) &
                            (df_perc_unc['Percentile'] == 95)
                            ][str(year)].values[0],
                        
                        ])
                    ax.plot(np.repeat(ang[v_i], 2), unc_vals, 
                            color=colours.get(s, "grey"), alpha=.75)

                    print(f'{s} {var}: Median {med_val}, 5th {unc_vals[0]}, 95th {unc_vals[1]}')

    l1, l2 = ax.get_ylim()
    
    limit = np.amax((np.abs(l1), np.abs(l2)))

    # print(limit)
    
    ax.set_xticks(ang); ax.set_xticklabels(var_list, fontsize=var_label_fs)
    yt = mticker.MaxNLocator(nbins=5, prune="both").tick_values(-limit, limit)
    ax.set_yticks(yt); ax.set_yticklabels([f"{t:.0f}%" for t in yt], fontsize=r_tick_fs)
    ax.grid(True, ls="--", alpha=.6)
    # ax.axhline(0, color="grey", lw=1)
    # ax.axhline(0, color="grey")
    ax.plot(np.linspace(0, 2*np.pi, 100), np.zeros(100), color='grey', lw=1)

    ax.set_title(str(year), y=1.10, fontsize=title_fs)

# ----------------------------------------------------------------
# 3.  master plot
# ----------------------------------------------------------------
def create_cap_elec_polar_dashboard(
        *, df, df_changes, df_share,
        region, years_bottom,
        scenarios, models, baseline_scenario,
        all_vars_names, scenario_names, groups,
        colours,                      
        save_dir="../figures/combined_panels/",
        figsize=(20,12), share_years=(2040,2070,2100)):

    # manual legend overrides – use if dicts uncommented
    scen_disp = globals().get("scenario_display", {})
    mod_disp  = globals().get("model_display", {})

    m_mark  = _model_markers(models)
    scen_no_base = [s for s in scenarios if s != baseline_scenario]

    pathlib.Path(save_dir).mkdir(parents=True, exist_ok=True)
    fig = plt.figure(figsize=figsize)
    gs  = gridspec.GridSpec(2, 3, figure=fig,
                            height_ratios=[1,1], width_ratios=[1,1,1],
                            hspace=.45, wspace=.25)

    # --- top-left ---------------------------------------------------------
    ax_ts = fig.add_subplot(gs[0, :])
    plot_total_capacity_ax(df, ax=ax_ts, region=region,
                           models=models, scenarios=scenarios,
                           all_vars=all_vars_names, colours=colours,
                           frida_unc=True, frida_unc_data=frida_unc_data)

    # --- top-right --------------------------------------------------------
    # ax_share = fig.add_subplot(gs[0, 2])
    # plot_elec_share_ax(ax_share, df_share, region=region,
    #                    base_scenario=baseline_scenario,
    #                    compare_scenarios=scen_no_base,
    #                    years=share_years,
    #                    colours=colours, m_mark=m_mark)

    # --- bottom row -------------------------------------------------------
    p_vars = groups["Installed Electricity Capacity"]
    for col, yr in enumerate(years_bottom):
        axp = fig.add_subplot(gs[1, col], projection="polar")
        plot_single_polar_ax(df_changes, ax=axp, region=region, year=yr,
                             variables=p_vars, models=models,
                             scenarios=scen_no_base,
                             all_vars=all_vars_names,
                             colours=colours, m_mark=m_mark,
                             frida_unc=True, frida_unc_data=frida_unc_data)

    # row title
    fig.text(.52, .48, "Electricity Capacity by Technology Compared to Current Trends",
             ha="center", va="bottom", fontsize=14)

    # --- legend -----------------------------------------------------------
    scen_handles = [mlines.Line2D([], [], color=colours[s], marker="o",
                                  ls="None", ms=8,
                                  label=scen_disp.get(s, scenario_names.get(s,s)))
                    for s in scen_no_base]

    bar_patch = mpatches.Patch(facecolor="#bdbdbd", edgecolor="#bdbdbd",
                               label=scen_disp.get(baseline_scenario,
                                                   scenario_names.get(baseline_scenario,
                                                                      baseline_scenario)))

    model_handles = [mlines.Line2D([], [], color="black",
                                   marker=m_mark[m], ls="None", ms=8,
                                   label=mod_disp.get(m, m.replace("_"," ")))
                     for m in models]

    line_handles = [mlines.Line2D([], [], color="black",
                                  ls=model_linestyles.get(m,"-"), lw=2.5,
                                  label=mod_disp.get(m, m.replace("_"," ")))
                    for m in models]

    handles_all = scen_handles + [bar_patch] + model_handles + line_handles
    fig.legend(handles=handles_all,
               ncol=len(handles_all),
               bbox_to_anchor=(.5,.03), loc="lower center",
               fontsize=9, frameon=True,
               title="Scenario               |               Model marker               |               Model line")

    # --- title & save -----------------------------------------------------
    fig.suptitle("Heatwaves and Drought Illustrative Scenarios",
                 fontsize=18, fontweight="bold", y=.975)
    fig.tight_layout(rect=[0,.07,1,.94])

    png = f"{save_dir}/dashboard_cap_elec_{region.replace(' ','_')}.png"
    pdf = png.replace(".png", ".pdf")
    fig.savefig(png, dpi=150, bbox_inches="tight")
    fig.savefig(pdf, dpi=300, bbox_inches="tight",
                metadata={"Title":"", "Subject":"", "Creator":"", "Producer":""})
    plt.close(fig)
    print("saved:", pathlib.Path(png).name, "&", pathlib.Path(pdf).name)


# In[26]:


create_cap_elec_polar_dashboard(
    df=df,
    df_changes=df_with_changes,
    df_share=df_share,
    region="World",
    years_bottom=[2040, 2070, 2100],
    scenarios=scenarios_of_interest,
    models=models_of_interest,
    baseline_scenario=baseline_scenario,
    all_vars_names=all_vars_names,
    scenario_names=scenario_names,
    groups=groups,
    colours=colours,              
    share_years=[2040, 2070, 2100]
)

