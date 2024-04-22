
## Project 3 - Association Rule Mining

### Implemented a version of the A-Priori algorithm to extract association rules from NYC dataset

## Authors
<ul>
    <li>Ajit Sharma Kasturi (ak5055)</li>
    <li>Samhit Chowdary Bhogavalli (sb4845)</li>
</ul>

## Files

<ul>
    <li>
        proj3
        <ul>
            <li>
                Apriori.py
            </li>
            <li>
                AssociationRule.py
            </li>
            <li>
                constants.py
            </li>
            <li>
                Dataset.py
            </li>
            <li>
                INTEGRATED-DATASET.csv
            </li>
            <li>
                Itemset.py
            </li>
            <li>
                main.py
            </li>
            <li>
                output.txt
            </li>
            <li>
                preprocess.py
            </li>
            <li>
                utils.py
            </li>
            <li>
                README.md
            </li>
            <li>
                .gitgnore
            </li>
            <li>
                requirements.txt
            </li>
        </ul>
    </li>
</ul>

## Design

* Apriori.py:
  * Contains Apriori class which is for executing various steps of A-Priori algorithm
* constants.py:
   * Contains all the constants used all over the project
* AssociationRule.py:
  * Contains AssociationRule which is used for storing association rules in the form of lhs => rhs where lhs and rhs are instances of Itemset class
* Dataset.py:
  * Contains Dataset class which is used to load INTEGRATED-DATASET.csv file.
  * It has set of items and market baskets
* Itemset.py:
  * Contains Itemset class which is used for storing various items.
  * It has functions for merging different itemsets efficiently (bitwise operations)
* main.py:
   * Main entry point of our program.
   * Uses the Apriori class to extract all association rules for a given file, minimum_support and minimum_confidence.
* preprocess.py:
  * Contains the logic to convert raw dataset to cleaned INTEGRATED-DATASET.csv file. 
* utils.py:
  * Just has small utility functions 

## Choice of Dataset

For thie project, we choose a dataset of [NYC Motor Vehicle Collisions](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95/about_data). This dataset contains all the information about recent automobile accidents in New York. Each row in this dataset provides information about a particular accident in New York. Its has lot information regarding the accident like Borough in which the accident occured, Date and time, no. of people injured, different classes of injured people (cyclists, motorcyclists ...etc), it also has similar information on no. of people killed in the accident and also contains the contributing factor of the accident. we chose this dataset to gain insightful information about accidents in the city we live and this can also be usefull to people by provide information on more accident-prone areas 

## Dataset Preprocessing

* There are a lot of columns with a lot of specific information which is not helpful for us. So we dropped every column except BOROUGH, CONTRIBUTING FACTOR VEHICLE 1, CRASH DATE, NUMBER OF PERSONS INJURED and the list of columns mentioning the type of injured people.  
* We removed all the rows that are having any of the above-mentioned columns as NaN.
* Since we are trying to do analysis of the injuries happened during the accidents, we dropped the rows having zero injuries and zero kills.
* "CONTRIBUTING FACTOR VEHICLE 1" colum took 62 different values, we used some manual effort and some help from chatgpt to put those 62 values to 5 buckets (specific mapping can found in constants.py file).
* Since date is too specific we extracted month from the date, and we further put the months into 4 different buckets. If month is less than or equal to 3, it is Q1. if it is less than or equal to 6, it is Q2. if it is less than or equal to 9, it is Q3. rest of all the month are Q4.
* We also added a different column called "time_map" by extracting hour information from date. It is Morning if the hours is between 5 and 11. It is Afternoon, if the hour is between 13 and 15. It is Evening, if the hour is between 16 and 19. rest of the hours fall in night
* We also created a new column called "injured_bucket". This takes motorists_injured if a motorcyclist is injured in the accident. It takes cyclists_or_pedestrians_injured if a cyclist or a pedestrian is injured in the accident.

#### Note: Code for the complete transformation is present in preprocess.py (please refer in case of any confusion)

## How to run

1. First, install Python 3.9:
```bash
sudo apt update
```
```bash
sudo apt install python3.9
```
```bash
sudo apt install python3.9-venv
```

2. Then, create a virtual environment running Python 3.9:
```bash
python3.9 -m venv dbproj
```

3. To ensure correct installation of Python 3.9 within your virtual environment:
```bash
source dbproj/bin/activate
python --version
```

The above should return 'Python 3.9.5'

10. Install Requirements of our project
```bash
cd proj3
pip install -r requirements.txt
```

11. Run our program
```bash
python main.py INTEGRATED-DATASET.csv 0.10 0.57
```

## Code Design and Logic
<p>
We used the association rules in our INTEGRATED-DATASET file, where each row in your file corresponds to one "market basket" and each column have different set of attributes whose union correspond to set of possible items.
We initially receive the INTEGRATED-DATASET file along with minimum support and minimum confidence as command line arguments.
Then we do the following:
</p>

<ul>
    <li>  
        First, we get all the frequent itemsets with minimum support by standard apriori algorithm.
        This logic is written in the get_all_itemsets_with_min_support function. This function basically
        does the following:
        <ul>
            <li>
                In this algorithm for discovering large itemsets, we perform multiple passes through the data. In the first pass, we count the support of individual items to determine which ones are large, i.e. have the least support. In each subsequent pass, we begin with a seed set of itemsets that were identified as large in the previous pass. We use this seed set to generate new potentially large itemsets, known as candidate itemsets, and then count the actual support for these candidate itemsets as we pass through the data. At the end of the pass, we determine which of the candidate itemsets are actually large, and those become the seed for the following pass. This process continues until no new large item sets are discovered.
            </li>
            <li>
                The apriori-gen utility function that we wrote takes as argument Lk-1, the set of all large (k- 1)-itemsets. It returns candidate set of all large k-itemsets. The
                function works as follows. First, in the join step, we join Lk-1 with Lk-1: insert into Ck
                select p.item,, p.item, ..., p.itemk-1, g.itemk-1 from Lk-1 P, Lk-1 where p.item, = qitems, .., pitemk-2 = g.itemk-2,
                p.itemk-1 < g.itemk-1.
            </li>
            <li>
                Next, in the prune step, we delete all itemsets c <span>&#x2208;</span> ck such that some (k-1)-subset of c is not in Lk-1.
                Our function need_to_prune does exactly this step.
            </li>
            <li>
                After k iterations, if we don't further generate any more frequent itemsetes with minimum support, we break the loop
                and return union of all the itemsets of sizes from 1 to k that we have obtained.
            </li>
        </ul>
    </li>
    <li>
        After we get set of all itemsets in min support, we iterate over each itemset, search all possible combinations of LHS and RHS parts
        of association rules, compute their confidence values and filter those association values with minimum confidence.
    </li>
    <li>
        We also did the following optimizations and corner case logic to our code:
        <ul>
            <li>We created an Itemset class which stores the set of items in form of a bitmask. This is efficient data structure for merge operations (it is simply bitwise-or of those bitmasks which has constant time complexity.) It also helps us iterate the subsets of bitmasks (for getting LHS and RHS efficiently.)</li>
            <li>We filtered some bad association rules specific to our dataset (For example, killed => injured etc.)</li>
            <li>We made sure to include those association rules which have length of LHS and RHS at least 1.</li>
        </ul>
    </li>
</ul>

## Observations and Results

### Results:
* min_sup = 0.1
* min_conf = 0.57
```
==Frequent itemsets (min_sup=10.0%)
['motorists_injured'], 61.03%
['cyclists_or_pedestrians_injured'], 39.57%
['Driver Inattention/Distraction'], 36.98%
['Misc Human Errors'], 33.13%
['BROOKLYN'], 32.59%
['Night'], 30.67%
['QUEENS'], 29.03%
['Q3'], 26.96%
['Evening'], 26.74%
['Q4'], 26.25%
['Morning'], 24.74%
['Q2'], 24.55%
['Driver Inattention/Distraction', 'motorists_injured'], 23.14%
['Q1'], 22.24%
['Misc Human Errors', 'motorists_injured'], 20.76%
['BROOKLYN', 'motorists_injured'], 19.71%
['QUEENS', 'motorists_injured'], 19.68%
['motorists_injured', 'Night'], 19.68%
['MANHATTAN'], 18.84%
['Afternoon'], 17.85%
['Failure to Yield Right-of-Way'], 17.77%
['motorists_injured', 'Q3'], 16.68%
['motorists_injured', 'Q2'], 15.5%
['BRONX'], 15.42%
['motorists_injured', 'Morning'], 15.41%
['motorists_injured', 'Q4'], 15.36%
['motorists_injured', 'Evening'], 15.02%
['Driver Inattention/Distraction', 'cyclists_or_pedestrians_injured'], 14.0%
['motorists_injured', 'Q1'], 13.49%
['BROOKLYN', 'cyclists_or_pedestrians_injured'], 13.1%
['Misc Human Errors', 'cyclists_or_pedestrians_injured'], 12.6%
['BROOKLYN', 'Driver Inattention/Distraction'], 11.93%
['cyclists_or_pedestrians_injured', 'Evening'], 11.88%
['cyclists_or_pedestrians_injured', 'Night'], 11.19%
['QUEENS', 'Driver Inattention/Distraction'], 11.06%
['cyclists_or_pedestrians_injured', 'Q4'], 11.01%
['Driver Inattention/Distraction', 'Night'], 10.94%
['motorists_injured', 'Afternoon'], 10.92%
['MANHATTAN', 'cyclists_or_pedestrians_injured'], 10.74%
['BROOKLYN', 'Misc Human Errors'], 10.71%
['cyclists_or_pedestrians_injured', 'Q3'], 10.48%
['Failure to Yield Right-of-Way', 'cyclists_or_pedestrians_injured'], 10.27%
['Driver Inattention/Distraction', 'Evening'], 10.16%
['Driver Inattention/Distraction', 'Q3'], 10.13%
['BRONX', 'motorists_injured'], 10.1%
['Misc Human Errors', 'Night'], 10.09%
['BROOKLYN', 'Night'], 10.01%
==High-confidence association rules (min_conf=57.0%)
['QUEENS'] => ['motorists_injured'] (Conf: 67.79%, Supp: 19.68%)
['BRONX'] => ['motorists_injured'] (Conf: 65.54%, Supp: 10.1%)
['Night'] => ['motorists_injured'] (Conf: 64.15%, Supp: 19.68%)
['Q2'] => ['motorists_injured'] (Conf: 63.15%, Supp: 15.5%)
['Misc Human Errors'] => ['motorists_injured'] (Conf: 62.67%, Supp: 20.76%)
['Driver Inattention/Distraction'] => ['motorists_injured'] (Conf: 62.58%, Supp: 23.14%)
['Morning'] => ['motorists_injured'] (Conf: 62.28%, Supp: 15.41%)
['Q3'] => ['motorists_injured'] (Conf: 61.85%, Supp: 16.68%)
['Afternoon'] => ['motorists_injured'] (Conf: 61.22%, Supp: 10.92%)
['Q1'] => ['motorists_injured'] (Conf: 60.63%, Supp: 13.49%)
['BROOKLYN'] => ['motorists_injured'] (Conf: 60.48%, Supp: 19.71%)
['Q4'] => ['motorists_injured'] (Conf: 58.52%, Supp: 15.36%)
['Failure to Yield Right-of-Way'] => ['cyclists_or_pedestrians_injured'] (Conf: 57.81%, Supp: 10.27%)
['MANHATTAN'] => ['cyclists_or_pedestrians_injured'] (Conf: 57.04%, Supp: 10.74%)
```

### Observations

We observe the following relations from the above result:
* BRONX, QUEENS, BROOKLYN have comparatively higher accidents where motorcyclists were injured when compared to MANHATTAN.
* MANHATTAN have comparatively higher no. of accidents where pedestrians or cyclists were injured.
* More motorcyclists were injured during Night, Morning, Afternoon when compared with the no. of injuries at Midnight.