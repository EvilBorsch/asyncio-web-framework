class CurrencyIsNotAdded(Exception):
    def __init__(self, curr_name):
        self.curr_name = curr_name

    def __str__(self):
        return f"Currency {self.curr_name} is not added"
