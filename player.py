# Import libraries
from random import randrange

# Define globals

BUYERBATNA = {"min":100000, "max": 200000}
SELLERBATNA = {"min":50000, "max": 150000}

class Player:

    def __init__(self, role):
        self.role = role
        self.batna = (
            randrange(BUYERBATNA["min"], BUYERBATNA["max"])
            if self.role == "buyer" 
            else randrange(SELLERBATNA["min"], SELLERBATNA["max"])
        )
        self.zopa_min = BUYERBATNA["min"] if self.role == "buyer" else SELLERBATNA["min"]
        self.zopa_max = BUYERBATNA["max"] if self.role == "buyer" else SELLERBATNA["max"]
        

    def calculate_no_deal(self):
        if self.role == "seller":
            amount = 0.99 * self.value
        elif self.role == "buyer":
            amount = 1.01 * self.value
        else:
            raise ValueError("Unknown role: role can be 'seller' or 'buyer'")
        percentage = 1

        return {"amount": amount, "percentage": percentage}

    def calculate_ewbg(self):
        return (
            self.rs["amount"] * (self.rs["percentage"]/100) +
            self.ora["amount"] * (self.ora["percentage"]/100) +
            self.ps["amount"] * (self.ps["percentage"]/100) +
            self.no_deal["amount"] * (self.no_deal["percentage"]/100)
        )

    def calculate_offer(self, enemy, prev_turn, enemy_prev_turn, strategies):

        pass
