from matplotlib import pyplot as plt
import sys
import pandas
import yaml
import seaborn as sns 

def config_reader(folder: str)-> dict:
    with open(f"{folder}/groups.yaml") as file:
      groups = yaml.safe_load(file.read())
    return groups

def read_table (folder: str)->pandas.DataFrame:
    data=pandas.read_csv(f"{folder}/data.txt", delimiter='\t', skiprows=7, index_col=1)
    data.drop(columns= "Date Time",inplace=True)
    return data 

def group_data (data: pandas.DataFrame, groups: dict) -> dict:
    grouped_data = {} #create a dictionary
    for group in groups:
        grouped_data[group] = data[groups[group]]
    return grouped_data

def plot_data (folder: str, grouped_data: dict):
    for group in grouped_data:
        df: pandas.DataFrame = grouped_data[group]
        df['mean'] = df.mean(axis=1)
        df['std'] = df.std(axis=1)
        sns.lineplot(data=df ,x=df.index, y='mean', label=group)
        plt.fill_between(df.index, 
                         df['mean']-df['std'], 
                         df['mean']+df['std'], 
                         alpha=0.05)
        plt.savefig(f"{folder}/lineplot.png")
        

def main():
    current_folder = "250123"
    data = read_table(current_folder)
    groups = config_reader(current_folder)
    grouped_data = group_data(data,groups)
    plot_data(current_folder, grouped_data)

if __name__ == '__main__':
    sys.exit(main())