class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        balance = 0
        for transaction in self.ledger:
            balance += transaction["amount"]
        return balance

    def transfer(self, amount, another_category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {another_category.name}")
            another_category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def __str__(self):
        title = f"{self.name.center(30, '*')}\n"
        total = 0
        transactions = ""
        for item in self.ledger:
            transactions += (
                f"{item['description'][:23]:23}" + f"{item['amount']:>7.2f}" + "\n"
            )
            total += item["amount"]
        output = title + transactions + "Total: " + str(total)
        return output

    def get_withdraws(self):
        withdraws = 0
        for item in self.ledger:
            if item["amount"] < 0:
                withdraws += abs(item["amount"])
        return withdraws


def create_spend_chart(categories):
    category_names = []
    category_spends = []
    percentages = []
    category_totals = 0

    for category in categories:
        category_names.append(category.name)
        category_spends.append(category.get_withdraws())
        category_totals += category.get_withdraws()

    for spend in category_spends:
        percentage = int((spend / category_totals) * 100)
        percentages.append(percentage)

    # start render graph
    graph = "Percentage spent by category\n"

    for i in range(100, -10, -10):
        line = f"{i:3}| "
        for percentage in percentages:
            if percentage >= i:
                line += "o  "
            else:
                line += "   "
        graph += line + "\n"

    graph += "    " + "-" * (3 * (len(categories)) + 1) + "\n"

    largest_name = max([len(name) for name in category_names])
    for i in range(largest_name):
        line = "     "
        for name in category_names:
            if i < len(name):
                line += f"{name[i]}  "
            else:
                line += "   "
        if i < largest_name - 1:
            graph += line + "\n"
        else:
            graph += line

    return graph
