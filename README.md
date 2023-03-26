# Round_Rock_Electric_Company_Comparison

This is a python program to check and compare average monthly charges between electric companies in Round Rock, Tx. 

You can either eneter the information in manually or you can provide two text files:

1) A text file that has your monthly kWh useage separated by commas
2) A text file of Electric companies and the information they provide on their Electricity Facts Label (EFL). 
  - The format for each line will be:   
  `<Company Name>, <base charge>, <energy_charge>, <discount kW threshold>, <discount amount>`

Provided are two example files and those exmaple files are what is passed into `main()`. Just create new files in a similar format, save them, and then pass the name into `main()` and it should work just fine. 

> Note: I did not error check this so make sure the information and the order is correct and accurate. 

## How to Run
Have python installed and then run `python rr_energy.py`. It's as easy as that!
