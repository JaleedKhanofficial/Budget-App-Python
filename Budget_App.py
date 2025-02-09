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
        return sum(item["amount"] for item in self.ledger)
    
    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False
    
    def check_funds(self, amount):
        return amount <= self.get_balance()
    
    def __str__(self):
        title = f"{self.name:*^30}\n"
        items = "".join(f"{item['description'][:23]:23}{item['amount']:7.2f}\n" for item in self.ledger)
        total = f"Total: {self.get_balance():.2f}"
        return title + items + total


def create_spend_chart(categories):
    total_spent = {category.name: sum(-item['amount'] for item in category.ledger if item['amount'] < 0) for category in categories}
    total = sum(total_spent.values())
    percentages = {name: (spent / total * 100) // 10 * 10 for name, spent in total_spent.items()}
    
    chart = "Percentage spent by category\n"
    for i in range(100, -1, -10):
        chart += f"{i:>3}| " + "  ".join("o" if percentages[name] >= i else " " for name in total_spent) + "  \n"
    
    chart += "    " + "-" * (3 * len(categories) + 1) + "\n"
    
    max_length = max(len(name) for name in total_spent)
    names = [name.ljust(max_length) for name in total_spent]
    for i in range(max_length):
        chart += "     " + "  ".join(name[i] for name in names) + "  \n"
    
    return chart.rstrip("\n")

food = Category('Food')
food.deposit(1000, 'deposit')
food.withdraw(10.15, 'groceries')
food.withdraw(15.89, 'restaurant and more food for dessert')
clothing = Category('Clothing')
food.transfer(50, clothing)
print(food)
categories = [food, clothing]
print(create_spend_chart(categories))