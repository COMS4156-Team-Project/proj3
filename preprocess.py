import sys
import pandas as pd
from constants import COLS_TO_REMOVE, CATEGORY_MAPPING, MONTH_TO_WORD

def get_cmdline_args():
    if len(sys.argv) != 2:
        sys.exit("REQUIRED FORMAT: python preprocess.py [raw dataset file path]")

    return sys.argv[1]


def injured_map(x):
    x = int(x)
    if x == 1:
        return 'injured_1'
    return 'injured_>_1'


def killed_map(x):
    if x == 0:
        return 'none_killed'
    return 'few_killed'


def time_map(x):
    x = str(x).split(':')[0]
    if len(x) != 2:
        x = '0' + x

    if x >= '05' and x <= '11':
        return 'Morning'
    elif x >= '13' and x <= '15':
        return 'Afternoon'
    elif x >= '16' and x <= '19':
        return 'Evening'

    return 'Night'

def month_to_quarter(x):
    if x <=3:
        return 'Q1'
    elif x<=6:
        return 'Q2'
    elif x<=9:
        return 'Q3'
    return 'Q4'

if __name__ == '__main__':
    dataset_file_path = get_cmdline_args()
    dest_file_path = 'INTEGRATED-DATASET.csv'
    df = pd.read_csv(dataset_file_path)

    # Remove unnecessary columns
    df.drop(columns=COLS_TO_REMOVE, inplace=True)

    # Remove null rows
    df = df.dropna(subset=list(df.columns.values))

    # Remove rows where persons injured and killed sum > 0
    df = df[df['NUMBER OF PERSONS INJURED'] + df['NUMBER OF PERSONS KILLED'] > 0]

    # Remove unspecified accidents
    df = df[df['CONTRIBUTING FACTOR VEHICLE 1'] != 'Unspecified']

    # Discretize contributing factor into fewer buckets
    df['contributing_factor'] = df['CONTRIBUTING FACTOR VEHICLE 1'].apply(
        lambda x: CATEGORY_MAPPING.get(x, 'Miscellaneous'))

    # Convert date into datetime format
    df['CRASH DATE'] = pd.to_datetime(df['CRASH DATE'], format='%m/%d/%Y')

    # Extract the month from the date column
    df['MONTH'] = df['CRASH DATE'].dt.month

    # Remove unnecessary column
    df = df.drop(columns=['CONTRIBUTING FACTOR VEHICLE 1'])

    # Reset index
    df = df.reset_index(drop=True)

    # Bucketize injured map
    df['injured_bucket'] = df['NUMBER OF PERSONS INJURED'].apply(injured_map)

    # Bucketize killed map
    df['killed_bucket'] = df['NUMBER OF PERSONS KILLED'].apply(killed_map)

    # Bucketize time map into Morning, Evening, Night, Afternoon
    df['time_map'] = df['CRASH TIME'].apply(time_map)

    # Remove no longer used columns
    df = df.drop(columns=['CRASH DATE', 'CRASH TIME', 'NUMBER OF PERSONS INJURED', 'NUMBER OF PERSONS KILLED'])
    df = df.reset_index(drop=True)

    # # Convert months into actual names
    # df['MONTH'] = df['MONTH'].apply(lambda x: MONTH_TO_WORD[int(x)])

    df['QUARTER'] = df['MONTH'].apply(lambda x: month_to_quarter(int(x)))

    # Save to csv file
    print(f"Saving preprocessed data to file {dest_file_path}")
    df.to_csv(dest_file_path, index=False)








