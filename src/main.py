import json
import os

from lib.env_reader import EnvReader

class Main:
    def __init__(self):
        envs = EnvReader()
        self.loan_amount = envs.amount
        self.loan_rate = envs.apr
        self.loan_months = envs.months
        self.large_payments = envs.extra_payment_months
        self.down_payment =  envs.down_payment


    def run(self):
        loan_stats = {}
        print("")
        print("#############################################")
        print("Loan Payment Simluator")
        print("#############################################")

        # Initial Values
        remaining_balance = self.loan_amount - self.down_payment
        annual_rate = self.loan_rate / 100
        months = self.loan_months

        print(f"Loan Amount before Down Payment: ${self.loan_amount:.2f}")
        print(f"Loan Amount: ${remaining_balance:.2f}")
        print(f"Down Payment: ${self.down_payment:.2f}")
        print(f"Annual Rate: {self.loan_rate}%")
        print(f"Loan Months: {months}")

        loan_stats["base"] = {
            "amount-before-down-payment": f"{self.loan_amount:.2f}",
            "amount-after-down-payment": f"{remaining_balance:.2f}",
            "amount-down-payment": f"{self.down_payment:.2f}",
            "annual-percentage-rate": f"{self.loan_rate:.2f}",
            "months-maximum": months
        }
        loan_stats["payment-months"] = {}


        # Convert annual rate to monthly
        monthly_rate = annual_rate / 12

        compound_rate = (1 + monthly_rate) ** months        
        numerator = monthly_rate * compound_rate
        denominator = compound_rate - 1
        fraction = numerator / denominator
        monthly_payment = remaining_balance * fraction
        
        print(f"Monthly Payment ${monthly_payment:.2f}")
        loan_stats["base"]["monthly-payment"] = f"${monthly_payment:.2f}"
        
        total_interest = 0
        actual_months = months

        for index in range(self.loan_months):
            month_number = index + 1

            extra_payment = 0
            if self.large_payments and month_number in self.large_payments:
                extra_payment = self.large_payments[month_number]

            print("")
            print(f"Payment Amounts on Month {month_number}")

            interest = remaining_balance * monthly_rate
            total_interest += interest
            principal = monthly_payment - interest
            if extra_payment > 0:
                print(f"Extra Large Payment: ${extra_payment:.2f}")
                principal = extra_payment - interest

            principal_interest = interest + principal
            
            remaining_balance = remaining_balance - principal
            remaining_balance = max(0, remaining_balance)

            if remaining_balance == 0:
                print(f"- Loan is paid off in {month_number-1} months!")
                loan_stats["base"]["months-actual"] = (month_number-1)
                actual_months = month_number - 1
                break

            print(f"- Payment Amount: ${principal_interest:.2f}")
            print(f"   - Principal: ${principal:.2f}")
            print(f"   - Interest: ${interest:.2f}")
            print(f"- Remaining: ${remaining_balance:.2f}")

            loan_stats["payment-months"][month_number] = {
                "amount": f"${principal_interest:.2f}",
                "interest": f"${interest:.2f}",
                "principal": f"${principal:.2f}",
                "remaining": f"${remaining_balance:.2f}"
            }
            if extra_payment > 0:
                loan_stats["payment-months"][month_number]["extra-payment"] = True

        print("")
        print("---------------------------------------------------")
        print("RESULTS")
        print("---------------------------------------------------")
        print(f"Total Interest Paid: ${total_interest:.2f}")
        print(f"Loan Amount before Down Payment: ${self.loan_amount:.2f}")
        print(f"Loan Amount: ${self.loan_amount - self.down_payment:.2f}")
        print(f"Down Payment: ${self.down_payment:.2f}")
        print(f"Annual Rate: {self.loan_rate}%")
        print(f"Loan Months: {months}")
        print(f"Actual Months: {actual_months}")
        
        loan_stats["base"]["total-interest-paid"] = f"${total_interest:.2f}"

        with open("files/loan-details.json", "w") as writer:
            json.dump(loan_stats, writer, indent=3, sort_keys=True)
        
        if os.path.exists(os.getenv("GITHUB_STEP_SUMMARY")):
            print("Add Results to Step Summary")
            with open(os.getenv("GITHUB_STEP_SUMMARY"), "a") as writer:
                print("---------------------------------------------------", file=writer)
                print("RESULTS", file=writer)
                print("---------------------------------------------------", file=writer)
                print(f"Total Interest Paid: ${total_interest:.2f}", file=writer)
                print(f"Loan Amount before Down Payment: ${self.loan_amount:.2f}", file=writer)
                print(f"Loan Amount: ${self.loan_amount - self.down_payment:.2f}", file=writer)
                print(f"Down Payment: ${self.down_payment:.2f}", file=writer)
                print(f"Annual Rate: {self.loan_rate}%", file=writer)
                print(f"Loan Months: {months}", file=writer)
                print(f"Actual Months: {actual_months}", file=writer)


        
if __name__ == "__main__":
    Main().run()