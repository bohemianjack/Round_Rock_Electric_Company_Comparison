################
#   classes    #
################


#class to account for the standard monthly Oncore charges. 
#Oncor is the electric provider in Round Rock, so as long as you're looking in Round Rock, then this class will work. 
#Information obtained at this link: https://southernfederal.com/tducharges/ 
#Information accurate as of March 2023
class OncorEnergy:
    def __init__(self, monthly_base, consumption_charge) -> None:
        self.__monthly_base = monthly_base
        self.__consumption_charge = consumption_charge / 100
    
    def get_monthly_base(self) -> float:
        return self.__monthly_base
    
    def get_consumption_charge(self) -> float:
        return self.__consumption_charge


#Class for each electric company entered into the prompt
class ElectricCompany:
    def __init__(self, oncore_energy, company_name, monthly_usage, base_charge, energy_charge, discount_kw_use, discount_amount) -> None:
        self.__monthly_charges = []
        self.__total_charges_across_months = 0.0
        self.__average_monthly_charge = 0.0
        self.__company_name = company_name
        self.__monthly_usage = monthly_usage
        self.__oncore_energy = oncore_energy
        self.__base_charge = base_charge
        self.__energy_charge = energy_charge / 100
        self.__discount_kw_use = discount_kw_use  #typically about 1000KW, but feel free to change if need be
        self.__discount_amount = discount_amount

        #run internal methods
        self.set_monthly_charges()
        self.set_total_charges()
        self.set_average_charge()

    def get_charge_for_month(self, kwhr) -> float:
        charge_for_month = 0
        #if kwhr is >= discount, then set the discount amount
        if (kwhr >= self.__discount_kw_use):
            charge_for_month -= self.__discount_amount
        #calculate static monthly base charges from both company and provider
        charge_for_month += self.__oncore_energy.get_monthly_base() + self.__base_charge
        #get all kwhr charges from both company and provider
        charge_for_month += kwhr * (self.__oncore_energy.get_consumption_charge() + self.__energy_charge)
        return charge_for_month

    def set_monthly_charges(self) -> None:
        for kwhr in self.__monthly_usage:
            monthly_charge = self.get_charge_for_month(kwhr)
            #append to the private list for the current monthly charge
            self.__monthly_charges.append(monthly_charge)
            #add to the charge's running total
            self.__total_charges_across_months += monthly_charge

    def set_total_charges(self) -> None:
        self.__total_charges_across_months =  self.__total_charges_across_months

    def set_average_charge(self) -> None:
        self.__average_monthly_charge = sum(self.__monthly_charges) / len(self.__monthly_charges)

    def get_total_charges(self) -> float:
        return self.__total_charges_across_months
    
    def get_average_charge(self) -> float:
        return self.__average_monthly_charge
    
    def get_company_name(self) -> str:
        return self.__company_name
    
    def get_monthly_charges(self) -> list:
        return self.__monthly_charges


################
#   functions  #
################

def write_output_file(list_of_companies, total_kwhr_month_list):
    with open("rr_detailed_log.txt", "w") as f:
        for company in list_of_companies:
            f.write(f"Company Name: {company.get_company_name()}\n")

            for month_index in range(len(total_kwhr_month_list)):
                f.write(f"\tMonth {month_index + 1}'s charge for {total_kwhr_month_list[month_index]:.2f} kWh: ${company.get_monthly_charges()[month_index]:.2f}\n")
            f.write("\t----------------------------------------\n")
            f.write(f"\tTotal for the months provided:    ${company.get_total_charges():.2f}\n")
            f.write(f"\tAverage monthly cost for service: ${company.get_average_charge():.2f}\n\n")


#reads a provided text file with comma separated values within the same directory for monthly kwhr useage
def read_kwhr_monthly_usage(filename) -> list:
    with open(filename, "r") as f:
        for line in f:
            data = line.strip().split(",")
        return [float(x) for x in data]

#reads a provided text file with comma separated values within the same directory with company information
# each line should be of the form: <Company Name>, <base charge>, <energy_charge>, <discount kW threshold>, <discount amount>
def read_company_from_text_file(filename) -> list:
    list_of_companies = []
    with open(filename, "r") as f:
        for line in f:
            #all numeric values are converted into floats (indices 1-4)
            data = line.strip().split(",")
            for i in range(1, len(data)):
                data[i] = float(data[i])
            #append company info
            list_of_companies.append(data)

    return list_of_companies

#if user decides to you two separate text files for information
def user_files(oncore, kwhr_file, company_info_file):
    list_of_companies = []
    kwhr_information = read_kwhr_monthly_usage(kwhr_file)
    company_information = read_company_from_text_file(company_info_file)

    for company in company_information:
        electric_company = ElectricCompany(oncore, company[0], kwhr_information, company[1], company[2], company[3], company[4])
        list_of_companies.append(electric_company)
    
    return kwhr_information, list_of_companies
    

#if user decides to put in user input manually, then they will use this function:
def user_input(oncore):
    #create list of companies
    list_of_companies = []
    list_of_monthly_kwhr_usage = []
    #get user prompt
    kwhr_monthly_history_amount = int(input("How many months of kw/hr history do you have (for example: 12 for a year): "))

    #get monthly kwhr usage
    for month_index in range(kwhr_monthly_history_amount):
        monthly_kwhr = float(input(f"Put in kwhr usage for month {month_index + 1}: "))
        list_of_monthly_kwhr_usage.append(monthly_kwhr)

    #get each company information
    while True:
        company_name = input("\nWhat is the company name (press enter with no text to exit): ")
        if company_name == "":
            break

        base_charge = float(input("What does the company charge for a monthly base charge (put 0 if none)?: "))
        energy_charge = float(input("What is the per kWh charge (in cents [for example: enter 11.8077 for 11.8077¢ per kWh]): "))
        discount_kw_use = int(input("What is the kw you need to reach to get a discount (put 0 for no discount): "))
        if discount_kw_use > 0:
            discount_amount = float(input(f"What is the discount amount once you reach {discount_kw_use}?: "))
        else:
            discount_amount = 0
    
        company = ElectricCompany(oncore, company_name, list_of_monthly_kwhr_usage, base_charge, energy_charge, discount_amount, discount_kw_use)
        list_of_companies.append(company)

    return kwhr_monthly_history_amount, list_of_companies

#main driver
def main(file_list):
    #create Oncore object
    oncore = OncorEnergy(monthly_base=3.42, consumption_charge=3.58990)
    
    #check to see if any files names are passed
    if len(file_list) == 0:
        list_of_monthly_kwhr_usage, list_of_companies = user_input(oncore)
    else:
        list_of_monthly_kwhr_usage, list_of_companies = user_files(oncore, file_list[0], file_list[1])

    write_output_file(list_of_companies, list_of_monthly_kwhr_usage)

    #display the company with the lowest rate
    suggested_company = list_of_companies[0]
    print(f"\nSuggested Company: {suggested_company.get_company_name()}")
    print(f"\tTotal spent based on input usage: ${suggested_company.get_total_charges():.2f}")
    print(f"\tAverage monthly cost based on input usage: ${suggested_company.get_average_charge():.2f}\n\n")
    print("Check 'rr_detailed_log.txt' for more verbose breakdown of charges\n\n")




if __name__ == "__main__":
    #put your files in here if you decide to go this route, 0th index should be useage, 1st index should be company information
    file_list = ["example_kwhr_monthly_usage.txt", "example_company_info.txt"]
    
    main(file_list)
    