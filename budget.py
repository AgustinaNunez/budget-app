class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []
        self.total_spent = 0

    def __str__(self):
        operations = self.name.center(30, "*") + "\n"
        for operation in self.ledger:
            operations += f"{operation['description'][:23].ljust(23)}{format(operation['amount'], '.2f').rjust(7)}\n"
        operations += f"Total: {format(self.get_balance(), '.2f')}"
        return operations

    def deposit(self, amount, description=''):
        self.ledger.append({'amount': amount, 'description': description})

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': description})
            self.total_spent += amount
            return True
        return False

    def transfer(self, amount, category):
        if self.withdraw(amount, description=f'Transfer to {category.name}'):
            category.deposit(amount, description=f'Transfer from {self.name}')
            return True
        return False

    def check_funds(self, amount):
        return self.get_balance() >= amount

    def get_balance(self):
        balance = 0
        for operation in self.ledger:
            balance += operation['amount']
        return balance

    def get_total_spent(self):
        return self.total_spent


def create_spend_chart(categories):
    return 'Percentage spent by category' \
        + bars_chart(categories, categories_heights(categories)) \
        + categories_names(categories)

def categories_heights(categories):
    total_spent = sum([category.get_total_spent() for category in categories])
    percentages = []
    for category in categories:
        percentage = int(category.get_total_spent() * 10 / total_spent) * 10
        percentages.append({'category': category.name, 'percentage': percentage})
    return percentages

def bars_chart(categories, percentages):
    output = ''
    bars = [i for i in range(0, 110, 10)]
    bars.reverse()
    for i in range(len(bars)):
        o_points = ''
        for percentage in percentages:
            o_points += ' o ' if percentage['percentage'] >= bars[i] else '   '
        output += "\n{:3d}|".format(bars[i]) + o_points
    output += '\n    ' + ('-' * len(categories) * 3) + '-'
    return output

def categories_names(categories):
    output = ''
    large_name = max([len(category.name) for category in categories])
    names = ['{: <{width}}'.format(category.name, width=large_name)
        for category in categories]
    for i in range(large_name):
        line = '\n     '
        for j in range(len(names)):
            line += names[j][i] + '  '
        output += line
    return output
