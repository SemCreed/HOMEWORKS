class BankAccount:
    def __init__(self, name: str, account_number: str, initial_balance: float = 0.0):
        self.name = name  # public attribute
        self._balance = initial_balance  # protected attribute
        self.__account_number = account_number  # private attribute
    
    def deposit(self, amount: float) -> None:
        if amount > 0:
            self._balance += amount
            print(f"Deposited ${amount:.2f}. New balance: ${self._balance:.2f}")
        else:
            print("Deposit amount must be positive")
    
    def withdraw(self, amount: float) -> None:
        if amount > 0:
            if amount <= self._balance:
                self._balance -= amount
                print(f"Withdrew ${amount:.2f}. New balance: ${self._balance:.2f}")
            else:
                print("Insufficient funds")
        else:
            print("Withdrawal amount must be positive")
    
    def get_balance(self) -> float:
        return self._balance
    
    def display_info(self) -> None:
        print(f"Account Name: {self.name}")
        print(f"Account Number: {self.__account_number}")
        print(f"Balance: ${self._balance:.2f}")


class SavingAccount(BankAccount):
    def __init__(self, name: str, account_number: str, interest_rate: float, initial_balance: float = 0.0):
        super().__init__(name, account_number, initial_balance)
        self.interest_rate = interest_rate  # annual interest rate as decimal (e.g., 0.05 for 5%)
    
    def apply_interest(self) -> None:
        interest = self._balance * self.interest_rate
        self._balance += interest
        print(f"Interest applied: ${interest:.2f}. New balance: ${self._balance:.2f}")
    
    def display_info(self) -> None:
        super().display_info()
        print(f"Interest Rate: {self.interest_rate * 100:.2f}%")


# Demonstration
if __name__ == "__main__":
    # Test BankAccount
    print("=== BankAccount Demo ===")
    account1 = BankAccount("John Doe", "ACC123456", 1000.0)
    account1.deposit(500.0)
    account1.withdraw(200.0)
    print(f"Current balance: ${account1.get_balance():.2f}")
    account1.display_info()
    
    print("\n=== SavingAccount Demo ===")
    # Test SavingAccount
    savings = SavingAccount("Jane Smith", "SAV789012", 0.05, 2000.0)  # 5% interest
    savings.display_info()
    savings.deposit(1000.0)
    savings.apply_interest()
    savings.display_info()
