#%%
import pandas as pd
#%%
params = {'csv_path':'F:\\github\\super-comparison\\csv\\fees.csv',
          'au_int_split':0.5}
#%%
def calculate_line(fund: pd.Series, split: float=0.5) -> tuple[float,float]:
    pass
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
    #%%
    print(data)


if __name__ == "__main__":
    main(params)