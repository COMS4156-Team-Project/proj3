
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
python main.py INTEGRATED-DATASET.csv 0.25 0.75
```

## Dataset description

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
                p.itemk-1 < g.itemk-1;
            </li>
            <li>
                Next, in the prune step, we delete all itemsets c <span>&#x2208;</span> ck such that some (k-1)-subset of c is not in Lk-1
                Our function need_to_prune does exactly this step.
            </li>
            <li>
                After k iterations, if we dont further generate any more frequent itemsetes with minimum support, we break the loop
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
            <li>We created an Itemset class which stores the set of items in form of a bitmask. This is efficient data structure for merge operations (it is simply bitwise or of those bitmask.) It also helps us iterate the subsets of bitmasks (for getting LHS and RHS efficiently.)</li>
            <li>We filtered some bad association rules specific to our dataset (For example, killed => injured etc.)</li>
            <li>We made sure to include those association rules which have length of LHS and RHS at least 1.</li>
        </ul>
    </li>
</ul>

## Observations and Results
<p></p>
<ul></ul>
