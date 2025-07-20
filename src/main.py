import json
import os

from lib.loan_terms import LoanTerms

class Main:
    def __init__(self):
        path_inputs = "files/input.json"
        data = {}
        with open(path_inputs, "r") as reader:
            data = json.load(reader)

        loan_terms = LoanTerms(data)
        self.loan_amount = loan_terms.amount
        self.loan_rate = loan_terms.rate
        self.loan_months = loan_terms.months


    def run(self):
        print("")
        print("#############################################")
        print("Loan Payment Simluator")
        print("#############################################")

        # Initial Values
        remaining_balance = self.loan_amount
        annual_rate = self.loan_rate / 100
        months = self.loan_months

        print(f"Loan Amount: ${remaining_balance:.2f}")
        print(f"Annual Rate: {self.loan_rate}%")
        print(f"Loan Months: {months}")


        # Convert annual rate to monthly
        monthly_rate = annual_rate / 12

        compound_rate = (1 + monthly_rate) ** months        
        numerator = monthly_rate * compound_rate
        denominator = compound_rate - 1
        fraction = numerator / denominator
        monthly_payment = remaining_balance * fraction
        
        print(f"Monthly Payment ${monthly_payment:.2f}")
        
        total_interest = 0
        for month_number in range(self.loan_months):
            print("")
            print(f"Payment Amounts on Month {month_number + 1}")

            interest = remaining_balance * monthly_rate
            total_interest += interest
            principal = monthly_payment - interest
            principal_interest = interest + principal
            
            remaining_balance = remaining_balance - principal
            remaining_balance = max(0, remaining_balance)

            print(f"- Payment Amount: ${principal_interest:.2f}")
            print(f"   - Principal: ${principal:.2f}")
            print(f"   - Interest: ${interest:.2f}")
            print(f"- Remaining: ${remaining_balance:.2f}")

        print(f"Total Interest Paid: ${total_interest:.2f}")


        


if __name__ == "__main__":
    Main().run()