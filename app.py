# -*- coding: utf-8 -*-

## Challenge 2 - Loan Qualifier Application
## This is a command line application to match applicants with qualifying loans.
## The initial code is provided by Berkeley Fintech BootCamp.
## The code is modified by Kevin BaRoss.

# The first part of the code will indicate which file will be imported into the system.
import sys
import fire
import questionary

from pathlib import Path

# Import the file to use to load and save the csv file(s).
from qualifier.utils.fileio import load_csv, save_csv

# Import the function to calculate monthly debt ratio and loan to value ratio from the calculators file.
from qualifier.utils.calculators import (
    calculate_monthly_debt_ratio,
    calculate_loan_to_value_ratio,
)

# Import functions to filter different financial data to match applicants with the qualifying loans.
from qualifier.filters.max_loan_size import filter_max_loan_size
from qualifier.filters.credit_score import filter_credit_score
from qualifier.filters.debt_to_income import filter_debt_to_income
from qualifier.filters.loan_to_value import filter_loan_to_value

# This function will ask for the file path to the latest banking data and load the CSV file.
def load_bank_data():
    
    # This will be the dialogue to ask the user to enter the file path to the banking data they want to use.
    csvpath = questionary.text("Enter a file path to a rate-sheet (.csv):").ask()
    csvpath = Path(csvpath)

    # If the file does not exist, the error message will appear.
    if not csvpath.exists():
        sys.exit(f"Oops! Can't find this path: {csvpath}")

    # If correct path is provided, the system will load that file to use in the filtering process later on in the system.
    return load_csv(csvpath)

# This function will output the prompt dialog to ask for the information of the applicant.
def get_applicant_info():
    
    # These are the sets of dialogs (questions) to get applicant's information.
    credit_score = questionary.text("What's your credit score?").ask()
    debt = questionary.text("What's your current amount of monthly debt?").ask()
    income = questionary.text("What's your total monthly income?").ask()
    loan_amount = questionary.text("What's your desired loan amount?").ask()
    home_value = questionary.text("What's your home value?").ask()

    # This is to indicate the data type for each variable, whether it is an integer or a float.
    credit_score = int(credit_score)
    debt = float(debt)
    income = float(income)
    loan_amount = float(loan_amount)
    home_value = float(home_value)

    # This will return the applicant information based on the information input by the user.
    return credit_score, debt, income, loan_amount, home_value

# This function will indicate which loan(s) the user qualifies for.
def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):
    
    """Determine which loans the user qualifies for.

    Loan qualification criteria is based on:
        - Credit Score
        - Loan Size
        - Debit to Income ratio (calculated)
        - Loan to Value ratio (calculated)

    Args:
        bank_data (list): A list of bank data.
        credit_score (int): The applicant's current credit score.
        debt (float): The applicant's total monthly debt payments.
        income (float): The applicant's total monthly income.
        loan (float): The total loan amount applied for.
        home_value (float): The estimated home value.

    """

    # Calculate the monthly debt ratio
    monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)
    print(f"The monthly debt to income ratio is {monthly_debt_ratio:.02f}")

    # Calculate loan to value ratio
    loan_to_value_ratio = calculate_loan_to_value_ratio(loan, home_value)
    print(f"The loan to value ratio is {loan_to_value_ratio:.02f}.")

    # Run qualification filters
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)

    # This statement prints how many loans match the user's preference.
    print(f"Found {len(bank_data_filtered)} qualifying loans")

    # The loan(s) that passes through all the filters will be returned at the end of the function.
    return bank_data_filtered


# This function will save the qualifying loans to a CSV file.
def save_qualifying_loans(qualifying_loans):

    # This will ask the user whether he/she wants to save the qualifying loans.
    want_to_save = questionary.text("Do you want to save your qualifying loans? Please enter Yes or No only.").ask()

    if want_to_save == "yes":

        # If the user wants to save the qualifying loan, the confirmation message will appear.
        print("OK. You want to save your qualifying loans.")

        # After that, the user has to enter the path that he/she wants the file to be saved.
        where_to_save = questionary.text("Please enter the output file path:").ask()
        csvpath = Path(where_to_save)

        # Then, the system will save the file with the header listed below.
        header = ["Lender", "Max Loan Amount", "Max Loan-to-Value (LTV)", "Max Debt-to-Income (DTI)", "Minimum Credit Score", "Interest Rate (%)"]
        save_csv(csvpath, qualifying_loans,header)

    else:

        # If the user does not want to save the file, the confirmation message will appear.
        print("You don't want to save your qualifying loans.")


# This is the main function for running the script.
def run():

    # Print Header and Project Detail
    print("==========================")
    print("Loan Qualifier Application")
    print("==========================")
    print("This program will match applicants with qualifying loans")
    print("By Kevin BaRoss")
    print("--------------------------")

    # Load the latest Bank data
    bank_data = load_bank_data()

    # Get the applicant's information
    credit_score, debt, income, loan_amount, home_value = get_applicant_info()

    # Find qualifying loans
    qualifying_loans = find_qualifying_loans(
        bank_data, credit_score, debt, income, loan_amount, home_value
    )

    # This if-statement indicates that if there is no qualifying loans, the program will be closed.
    if len(qualifying_loans) == 0:
        print("Since there is no qualifying loans. The program will now be closed.")
    else:
    # If there is more than one qualifying loan in the list, the system will save the qualifying loans
        save_qualifying_loans(qualifying_loans)

# This is to call the Fire package
if __name__ == "__main__":
    fire.Fire(run)
