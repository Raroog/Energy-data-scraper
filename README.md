Scraper created for downloading 3 different raports.
Scraper consists of 3 files for ETL phases and one main file to run the modules and take user input from command line.
The main file is just an example. It is possible to create files for specific raports. This case works with each raport.

There are 3 names for raports:

kse - https://www.pse.pl/dane-systemowe/funkcjonowanie-kse/raporty-dobowe-z-pracy-kse/wielkosci-podstawowe 

pse - https://www.pse.pl/dane-systemowe/funkcjonowanie-kse/raporty-dobowe-z-pracy-kse/generacja-mocy-jednostek-wytworczych 

tge - https://tge.pl/energia-elektryczna-rdn second table on the page.

The raports are created by downloading csvs or by scraping the page's html and putting the needed data back to table.
The extracted data is transformed and put in the end to csv files.


The script takes 3 arguments, first date, second date and raport name.
Dates has to be different, can't be dates from the future and follow dd-mm-yyyy format for example 20-11-2022.
For tge raport the data available is from last 3 months. 

To run the script and get the csv files with raport user has to:

- Open linux command line 
- cd into location of the files with scripts
- type: python main.py --date1 dd-mm-yyyy --date2 dd-mm-yyyy --raport kse/pse/tge
	for example:
		 python main.py --date1 19-07-2022 --date2 12-07-2022 --raport tge
		 This command will return csv file from 12-07-2022 - 19-07-2022 date range fro tge raport.

The created csv file will show up in the scraper folder.



