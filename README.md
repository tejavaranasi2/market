# Portfolio Mangement(CP_v1 and LP_v1)
We use LP, Convex Programming, and basic probability modeling to find alphas that maximize return based on a risk profile.

# Organisation of the directory:
- data (contains all scripts that are responsible for fetching data)
- strats (contains folders each with a strategy)
   - CP_v1 (version 1.0 of convex programming)
   - LP_v1 (version 1.0 of convex programming)

# Running the code:
To run a particular strategy, follow these steps:
  - Navigate to the directory
  - A folder named cfg(configuration) has all the relevant factors and support provided by the strategy(a sample has been provided for refercene)
  - Run the file named strat.py by changing the appropriate cfg file

# Understanding the output:
Code, as of 30 Nov 2023, only generates alphas and prints them to the console. Reading them should be important in the case of 
CP_v1 and LP_v1 as they just represent the LONG position that is recommended by the model

# Testing and development
For grading purposes, all the plots and data that were generated as part of testing have been left intact and are in no way 
required to understand/develop the code(These extra portions will be removed once the project has been graded)
In our realization, the slowest part of the whole pipeline is the data extraction from Yfinance. These are the areas where we have alredy 
begun to work.
  - working on changing the data input API(real-time)
  - creating an appropriate interface to connect an exchange

#Bugs and Comments:
Please feel free to reach tejavaranasi2003@gmail.com for any comments on this project.
