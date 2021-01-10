# Bioresources market information

This is code for Ofwat's bioresources market information work. 

There are four key Python scripts: 

1. **Bioresources_market_information.py**: This is the main script to consolidate and format water companies' published bioresources market information. It is this script that generates the data that Ofwat uses to produce its [dashboard](https://www.ofwat.gov.uk/regulated-companies/markets/bioresources-market/bioresources-market-information/)


2. **Bio_analysis_STC.py**: This is produces summary, descriptative statitics. 


3. **Bio_analysis_pairings.py**: This produces the distance between each Sludge Treatment Center. 


4. **Bioresources_market_info_functions.py**: This contains a number of bespoke functions used by the other scripts. 


All of the outputs from the above scripts are saved in a SQL database in the outputs folder.





