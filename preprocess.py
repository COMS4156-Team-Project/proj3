import sys
import pandas as pd
from constants import COLS_TO_REMOVE, CATEGORY_MAPPING, INJURED_KILLED_COLS

def get_cmdline_args():
    if len(sys.argv) != 2:
        sys.exit("REQUIRED FORMAT: python preprocess.py [raw dataset file path]")

    return sys.argv[1]


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


def injured_list_map(row):
    ans = []
    if int(row['NUMBER OF PEDESTRIANS INJURED']) > 0 or int(row['NUMBER OF CYCLIST INJURED']) > 0:
        ans.append('cyclists_or_pedestrians_injured')

    if int(row['NUMBER OF MOTORIST INJURED']) > 0:
        ans.append('motorists_injured')

    if len(ans) == 0:
        ans.append('none_injured')

    return ','.join(ans)


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
    df['injured_bucket'] = df.apply(injured_list_map, axis=1)

    # Bucketize time map into Morning, Evening, Night, Afternoon
    df['time_map'] = df['CRASH TIME'].apply(time_map)

    # Drop empty values of injured bucket
    df = df[df['injured_bucket'] != 'none_injured']

    # Remove no longer used columnss and nan vals
    df = df.drop(columns=[*INJURED_KILLED_COLS, 'CRASH DATE', 'CRASH TIME', 'NUMBER OF PERSONS INJURED', 'NUMBER OF PERSONS KILLED'])
    df = df.reset_index(drop=True)

    # Get quarter for month
    df['QUARTER'] = df['MONTH'].apply(lambda x: month_to_quarter(int(x)))

    # Remove month column since we have quarter
    df = df.drop(columns=['MONTH'])
    df = df.reset_index(drop=True)

    # Save to csv file
    print(f"Saving preprocessed data to file {dest_file_path}")
    df.to_csv(dest_file_path, index=False)








