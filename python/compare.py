#%%
import pandas as pd
from typing import Callable
import matplotlib.pyplot as plt
import numpy as np
#%%
params = {'csv_path':'F:\\github\\super-comparison\\csv\\fees.csv',
          'au_int_split':0.5}
#%%
def calculate_line(fund: pd.Series, split: float=0.5) -> Callable:
    intercept = fund['Fixed p.a']
    grad_manage = fund['% of AUM']
    grad_invest = split * fund['Aus shares'] + (1-split) * fund['Int shares']
    cap = float(fund['Admin fee cap'])

    if pd.isnull(cap):
        cap = 0
    
    x_break = (cap - intercept) / grad_manage if grad_manage > 0 else 0

    return lambda x: intercept + \
                        (x <= x_break) * (grad_manage + grad_invest) * x + \
                        (x >  x_break) * (cap         + grad_invest  * x )
#%%
#%%
def main(kwargs):
    #%%
    # List of super funds and their fees are stored in a local csv file
    csv_path = kwargs.get('csv_path')
    with open(csv_path, 'r') as file:
        data = pd.read_csv(file)
    #%%
    # Linear calculation
    split = kwargs.get('au_int_split')
    data['function'] = data.apply(calculate_line, axis=1)
    #%%
    x_values = np.linspace(0,100000,5)
    plt.figure(figsize=(8,6))
    for _, row in data.iterrows():
        y_values = [row['function'](x) for x in x_values]
        plt.plot(x_values, y_values, label=row['Name'])

    # row = data.loc[0]
    # y_values = [row['function'](x) for x in x_values]
    # plt.plot(x_values, y_values, label=row['Name'])


    plt.legend()
    plt.title("Total fees for super funds")
    plt.xlabel("Assets under management ($)")
    plt.ylabel("Total fees ($)")
    plt.show()
    #%%


if __name__ == "__main__":
    main(params)