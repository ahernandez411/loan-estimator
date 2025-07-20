import os

class EnvReader:
    def __init__(self):
        self.apr = float(os.getenv("APR", 7.99))
        self.amount = float(os.getenv("AMOUNT", 7000))
        self.months = int(os.getenv("MONTHS", 72))
        self.down_payment = float(os.getenv("DOWN_PAYMENT", 1000))

        self.extra_payment_months = {}

        raw_extra_month_amount = os.getenv("EXTRA_MONTH_AMOUNT")
        if raw_extra_month_amount and ":" in raw_extra_month_amount:
            month_num_str, amount_str = raw_extra_month_amount.split(":")
            month_num = int(month_num_str.strip())
            amount = float(amount_str.strip())

            self.extra_payment_months[month_num] = amount
