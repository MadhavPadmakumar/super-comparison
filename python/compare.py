#%%
import pandas as pd
from typing import Callable
import matplotlib.pyplot as plt
import numpy as np
#%%
params = {'csv_path':'F:\\github\\super-comparison\\csv\\fees.csv',
          'au_int_split':0.4}
#%%
def calculate_line(fund: pd.Series, split: float=0.5) -> Callable:
    intercept = fund['Fixed p.a']
    grad_manage = fund['% of AUM']/100
    grad_invest = split * fund['Aus shares']/100 + (1-split) * fund['Int shares']/100
    cap = float(fund['Admin fee cap'])

    # No admin fee cap; handle separately to avoid inf/nan values
    if pd.isnull(cap):
        return lambda x: intercept + (grad_manage + grad_invest) * x 
    else:
        x_break = (cap - intercept) / grad_manage if grad_manage > 0 else 0
        return lambda x: intercept + \
                            (x <= x_break) * (grad_manage + grad_invest) * x + \
                            (x >  x_break) * (cap         + grad_invest  * x )
#%%
#%%
def main(params):
    #%%
    # List of super funds and their fees are stored in a local csv file
    csv_path = params.get('csv_path')
    with open(csv_path, 'r') as file:
        data = pd.read_csv(file)
    #%%
    # Linear calculation 
    split = params.get('au_int_split')
    data['function'] = data.apply(calculate_line, axis=1)
    #%%
    limit = 10000
    x_values = np.linspace(0, limit, int(limit / 10))

    # Store y-values for each row
    y_data = {}
    for index, row in data.iterrows():
        y_data[index] = [row['function'](x) for x in x_values]

    # Determine which rows are in the lowest few at any x_value
    valid_indices = set()
    for i in range(len(x_values)):
        y_sorted = sorted((y_data[idx][i], idx) for idx in y_data)  # Sort by y-value
        lowest = {idx for _, idx in y_sorted[:2]}  # Get lowest few indices
        valid_indices.update(lowest)  # Track all rows that were in the lowest indices

    # Plot only valid rows
    plt.figure(figsize=(8, 6))
    for index in valid_indices:
        plt.plot(x_values, y_data[index], label=data.loc[index, 'Name'])

    plt.legend()
    plt.title("Total fees for super funds")
    plt.xlabel("Assets under management ($)")
    plt.ylabel("Total fees ($)")
    plt.show()
    #%%


if __name__ == "__main__":
    main(params)


#%% Testing
qsuper_function = data[data['Name'] == 'Qsuper']['function'].iloc[0]
aware_function = data[data['Name'] == 'Aware Super']['function'].iloc[0]
cfs_function = data.iloc[19]['function']

# TODO: Read directly from the google sheet table, set aus-int ratio to 0.4, 
# ensure that for x = 10k, 50k, 100k, 250k, 500k, f(x) = the table entry for each fund
#%%