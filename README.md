# Round_Rock_Electric_Company_Comparison

This is a python program to check and compare average monthly charges between electric companies in Round Rock, Tx. This program works with your previous useage history in Round Rock so make sure that you have that information on hand. 

You can either eneter the information in manually or you can provide two text files:

1) A text file that has your monthly kWh useage separated by commas
2) A text file of Electric companies and the information they provide on their Electricity Facts Label (EFL). 
  - The format for each line will be:   
  `<Company Name>, <base charge>, <energy_charge>, <discount kW threshold>, <discount amount>`

Provided are two example files and those exmaple files are what is passed into `main()`. Just create new files in a similar format, save them, and then pass the name into `main()` and it should work just fine. 

> Note: I did not error check this so make sure the information and the order is correct and accurate. 

## How to Run
basically this is how it'll work:

1. head to either/both:  
  - https://www.powertochoose.org/
  - https://www.choosetexaspower.org/electricity-rates/round-rock/
2. Enter your Zipcode
3. Search/filter based on your needs
4. Look at prospective company's EFL file. Enter that information into the txt file as seen in the example file
5. Look at previous Round Rock electric bills to get at least the last 9-12 months of useage. Since this works on averages, the more data you have the better. Enter that into another text file as seen in the example file
6.Have python installed and then run `python rr_energy.py`. It's as easy as that!
7. The python file will produce detailed information into a txt file as well as tell you in the console which company it thinks would be the cheapest

> Note: This **does not** take into account things like solar panel discounts/useage, clean energy useage, any night/weekend no-charge benefits, etc. This just takes the raw, basic kw/hr charge information and tells you what might be the best one for you based on that information alone. 
