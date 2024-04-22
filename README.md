
## Project 3 - Association Rule Mining

### Implemented a version of the A-Priori algorithm to extract association rules from data

## Authors
<ul>
    <li>Ajit Sharma Kasturi</li>
    <li>Samhit Chowdary Bhogavalli</li>
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

## Data Preprocessing



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

## Code Design and Logic
<p>We used SOLID design principles to write a clean and maintainable code. We performed the Iterative Set Expansion (ISE) algorithm discussed in class. In our logic, we handled ignoring non-HTML files by checking the fileFormat attribute of the json data returned by google search engine upon querying it. However, the queries that we send to Google is not limiting the document types that we receive. </p>
<ol>
  <li>The iterative set expansion algorithm is implemented as follows:
  <ul>
    <li>First we begin with reading the following parameters (in the below order) from the user:
            <ul>
		     <li>
		     Model flag[-gemini/-spanbert]
		     </li>
	             <li>
	             Google Custom Search Engine JSON API Key
	             </li>
	             <li>
	             Google Engine ID
	             </li>
	             <li>
	             Google Gemini API key
	             </li>
	             <li>
	             An integer r between 1 and 4, indicating the relation to extract: 1 is for Schools_Attended, 2 is for Work_For, 3 is for Live_In, and 4 is for Top_Member_Employees
	             </li>
	             <li>
	             Extraction Confidence threshold
	             </li>
	             <li>
	             Seed query q
	             </li>
	             <li>
	             An integer  k  greater than 0, indicating the number of tuples that we request in the output
	             </li>
			</ul>    
    </li>
    <li>By calling our SearchEngine class (which is a wrapper for calling Google search engine API and processing the result) with the seed query argument, we extract the top 10 links from Google.</li>
    <li>For each link, we scrape the HTML content and extract textual content from it. If the total number of extracted characters is greater than 10000, we only consider the top 10000 characters extracted. </li>
    <li>We then use the spacy library to get sentences from text and then annotate them with the entities mentioned in the ENTITIES_OF_INTEREST constant. </li>
    <li>From the relation given in the input, we can identify the entity pairs of interest and get list of tuples from the annotated sentences using the following format (SUBJECT entity, OBJECT entity, tokenized sentence containing this subject and object). We only consider the candidate sentences which have this subject-object pairs and discard the rest.</li>
    <li> We then performing the following: (dependening on whether we use Spanbert or Gemini):
	   <ul>
		   <li>
			   For Spanbert:
			   <ul>
				   <li>
					   We pass the list of (Subject, Object, Tokenized sentence) tuples to our Spanbert wrapper (which internally calls the actual Spanbert) to get a list of tuples with confidence greater than or equal to the confidence threshold parameter provided in the input. 
				   </li>
			   </ul>
		   </li>
		   <li>
			   For Gemini:
			   <ul>
				   <li>
					   We need not tokenize sentence in this case. We engineered a prompt which has the candidate sentence in it and pass that prompt to Gemini asking us to return relation tuples in a fixed format. Then Gemini provides us with those list og tuples (provided as string) and we later parse it to get the extracted tuples from Gemini.
				   </li>
				   <li>
					   Sample prompt:  <br><br>
                        <i> I will give you a paragraph and relationship types as input, you have to analyze the paragraph properly and extract all examples of the mentioned relationship types that you can find in the paragraph. <br> <br>
Relationship types: Employee of. 
Paragraph: Google CEO Sundar Pichai Appointed To Alphabet Board Of Directors <br> <br>
Please give outputs in [Subject:_:Relationship:_:Object] format. </i> <br> <br>
				   </li>
			   </ul>
		   </li>
	  </ul>
  </li>
    <li>Once we get the extracted tuples, if the number of tuples is at least k, we break the loop. If it is less than k,  we get the tuple with highest confidence not queried before, make a seed query from it by concatenating subject and object and use this as a starting query in the current iteration. We do this till the number of tuples extracted is greater than or equal to k. (We also stop if there are no further tuples to query.)</li>
    </li>
  Corner case handlings:
  <ul> 
  <li>We made sure to remove duplicate tuples in the list of extracted tuples and also made sure the seed queries are different in each iteration.</li>
  <li>If no seed tuple extracted with good confidence is left to query, we stop the program immediately mentioning the reason.</li>
  <li>If the number of command line arguments is incorrect, we stop the program gracefully mentioning the reason for exit and the correct command line arguments format.</li>
  <li>
  We only query sentences to Gemini or Spanbert that contain all of our required entities.
  </li>
  </ul>
 </li>
</ol>


