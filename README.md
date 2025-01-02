# League of Legends Tournament Analysis

This project aims to provide a toolset to analyze sign-up responses for VLN Draft S1. This should help our team captain prioritize potential players based on specific criteria such as role preference, rank, and champ pool. 

## Features
**Data Parsing**: Read and preprocess tournament sign-up data from a spreadsheet.
**Role Analysis**: Identify players' primary and secondary roles.
**Rank Evaluation**: Compare player ranks to create a skill-based priority list
**Custom Filters**: Filter and rank players based on user-defined criteria.
**Export Options**: Save prioritized lists for easy sharing.

## Getting Started

### Prereqs
- Python 3.7+
- Required Python packages (install via `requirements.txt`)
    - `pandas`
    - `sys`

### Installation
1. Clone this repository: 
    ```
    git clone git@github.com:silasejohn/VLN-Draft-Analysis.git
    ```

2. Install dependencies: 
    ```
    pip install -r requirements.txt
    ```
3. Place the updated sign-up response spreadsheet (`data.csv`) in the data/ folder

### Usage
1. Run the format script to format the csv
    ```
    python format.py
    ```
2. Run the analysis script to analyze the csv
     ```
    python analyze.py
    ```
3. Export / Run Locally to Visualize Results
4. Use the "draft tool" to maintain priorities on players left in draft

## Customization / Config
....

## Acknowledgments
Special thanks to GepettosPuppet 

### Other
Create Virtual Environment: `python3.9 -m venv [name]-env`
Activate Virtual Environment: `source [name]-env/bin/activate`
Install Dependency List: `pip3 install -r requirements.txt`
Deactivate Virtual Environment: `deactivate`

#### TODO
1. look through raw spreadsheet + read qualitative descriptions ~> assign a bool value of "consideration"
2. look through primary / secondary rank descriptions ~> assign a bool value of "consider_secondary_role"
3. create selenium scripts for league of graphs, op.gg, and rewind.lol to access more quantitative scouting info
4. COOL PRINT OUTPUT + DYNAMIC PRINT OUTPUT
