# import modules
from time import sleep # to slow down display of some menu options to improve menu
import json # for file handling of accounts
import sys  # to exit running of code when logout function called

customer = None # initialise global variable customer (avoids needing to pass into each function as this variable will be used in most functions)

# ----- CLASS DEFINING (Bank accounts, customers)

class CaledoniaBankAccount():
    
    # constructor defining attributes of bank accounts that will be used by all types of account
    def __init__(self, name, sort_code, account_number, interest_rate, balance):
        self.name = name
        self.sort_code = sort_code
        self.account_number = account_number
        self.interest_rate = interest_rate
        self.balance = balance
    
    # overwrite print() function for bank account objects
    def __str__(self):
        return (f'Account Holder: {self.name}\n'
                f'Sort Code: {self.sort_code}\n'
                f'Account Number: {self.account_number}\n'
                f'Interest Rate: {self.interest_rate:.2%}\n'
                f'Balance: £{self.balance:.2f}')
        
    def deposit(self):
        # loop until valid input is entered
        while True:
            try:
                amount = float(input('Enter the amount you would like to deposit: £'))
                if (amount > 0):
                    self.balance += amount
                    print(f'\nSuccessfully deposited £{amount:.2f}')
                    break # break the loop when the entered value is valid
                else:
                    print ('Invalid amount. Amount must be greater than 0.')
            except ValueError: # displays valueerror if the input is not convertible to float (if string has been entered)
                print('You entered an invalid data type. Please re-enter a number.')      
    
    # Withdraw cash from bank account
    def withdraw(self):
        while True:
            try:
                # display balance for user before withdrawing cash
                self.check_balance()
                amount = float(input('Enter the amount you would like to withdraw:'))
                if amount <= self.balance and amount > 0:
                    self.balance -= amount # reduce balance by withdrawn amount
                    break
                else:
                    # execute if balance insufficient
                    print (f'\nFailed to withdraw {amount}. Insufficient funds in your account.')
                    print(f'\nSelect one of the following:\n1: Re-enter an amount less than {self.balance}\n2: Return to Customer Homepage')
                    user_input = get_input(1,2)
                    if user_input == 2:
                        break # break out of while loop if user opts to return to customer homepage
                    else:
                        # continue to next iteration of loop
                        continue
            except ValueError:
                # execute if wrong datatyep entered
                print('\nInvalid input. Please re-enter a positive number  ')

    # displays the balance of the chosen account (to two decimal places)
    def check_balance(self):
        print(f'\nAccount Balance: {'£':s}{self.balance:.2f}')
        sleep(3)

    # calculates and adds interest ot the selected account
    def AddInterest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest


class SavingsAccount(CaledoniaBankAccount):
    # init constructor defines fixed sort code and fixed interest rate for the account type. balance initially set to 0
    def __init__(self, name, account_number):
        super().__init__(name, 1, account_number, 0.05, 0) # use super() to inherit attributes from parent class
        
    def __str__(self):
        return (f'\n------Savings Account Details:\n\n{super().__str__()}')  # Use the __str__ from the base class



class CurrentAccount(CaledoniaBankAccount):
    # init constructor defines fixed sort code and fixed interest rate for the account type. balance initially set to 0
    def __init__(self, name, account_number):
        super().__init__(name, 2, account_number, 0.01, 0)
    
    # display type of account before calling __str__ in parent class
    def __str__(self):
        return (f'\n------Current Account Details:\n\n{super().__str__()}')  # Use the __str__ from the base class



class MortgageAccount(CaledoniaBankAccount):
    def __init__(self, name, account_number):
        super().__init__(name, 3, account_number, 0.08, 0)
    
    # display type of account before calling __str__ in parent class
    def __str__(self):
        return (f'\n------Mortgage Account Details:\n\n{super().__str__()}')  # Use the __str__ from the base class
    
    # different apply interest function for mortgages as interest is deducted, not added, from this account
    def ApplyInterest(self):
        self.balance -= self.balance * self.interest_rate
        print('Interest deducted.')
    
    def CapitalRepayment(self, current_ac_balance, monthly_repayment = 500):
        # mortgage repayment set by default but can be changed by passing a different value when calling the function
        # only carry out transaction if the current account has enough funds
        if current_ac_balance < monthly_repayment:
            print('\nYou do not have enough funds to pay your monthly dues.\nPlease deposit more cash into your current account before making a monthly repayment. ')
        else:
            self.balance -= monthly_repayment
            customer.current_account.balance -= monthly_repayment
            print('Successfully paid your monthly mortgage payment.')
            
        # check if the mortgage is fully paid off:
        if self.balance <= 0:
            print('Congratulations! You have successfully paid off your mortgage!!')
            # add the overpayment back to the current account
            customer.current_account.balance += ((self.balance)**2)**0.5  # squared and rooted to ensure positive number is added to the current account
            self.balance = 0 # ensure that the mortgage is not put into negative balance from overpayment


# CLASS FOR STORING CUSTOMER DETAILS (LOGIN AND REGISTER FUNCTIONS)
class Customer():
    # init constructor defning attributes for customer class
    def __init__(self, customer_id = '', name = '', password = ''):
        self.customer_id = customer_id
        self.name = name
        self.password = password
        
        #add instance of each bank account to customer object (set account number to -1 to indicate account is not active yet.)
        self.savings_account = SavingsAccount(self.name, account_number=-1)
        self.current_account = CurrentAccount(self.name, account_number=-1)
        self.mortgage_account = MortgageAccount(self.name, account_number=-1)





#  ----------- FUNCTIONS

def WelcomePage():
    print(f'\n{'Welcome to Caledonia Bank':{'-'}^{50}}\n')
    print('\nPlease select one of the following:\n\n1:  Log in (Existing Customers Only)\n2:  Register (New Customers Only)')

    # ask for user input until user enters valid input
    valid = False
    while valid == False:
        user_input = get_input(1, 2)
        if user_input == 1:
            # load all customer login details to check against login details
            customer_records = LoadCustomerRecords()
            login(customer_records)
            valid = True
        elif user_input == 2:
            register()
            valid = True
        else:
            print('\nYour input was invalid. Try again.')




def LoadCustomerRecords():
    with open('customer_records.txt', 'r', encoding='utf-8') as inp:
            customer_records = {} # initialise empty dictionary to be populated from file
            for row in inp:
                stored_id, stored_details = row.split(': ',1) # split into id and customer details
                stored_id = int(stored_id)
                stored_name, stored_password = stored_details[1:-2].split(', ', 1) # split customer details into name and password
                stored_name = stored_name.replace("'", "")
                stored_password = stored_password.replace("'", "") # removes single quotation marks
                
                customer_records[stored_id] = [stored_name, stored_password] # adds each customer records to customer_records dictionary as they are read in from the file.
    return customer_records




def login(customer_records):
    global customer # set customer object as a global variable 
    print(f'\n{'Login to your Caledonian Bank Account':{'-'}^{50}}\n')
    # ADD TRY: .... EXCEPT TO HANDLE WRONG DATA BEING PUT INTO THIS 
    while True:
        try:
            customer_id = int(input('Customer ID: '))
            password = input('Password: ')
            break # break out of while loop if login details follow valid format
        except ValueError:
            print('Invalid input. Customer ID must be an integer.')
    
    # check if login details match the stored records (passed into function as 'customer_records')
    while True:
        if customer_id in customer_records:
            if password == customer_records[customer_id][1]:
                print('Successfully logged in.')
                customer = Customer(customer_id, customer_records[customer_id][0], customer_records[customer_id][1])
                RetrieveAccount() # Retrieve state of accounts for logged in customer
                CustomerHomepage()
                break
            else:
                print('Incorrect password. Please try again.')
                login(customer_records)
        elif customer_id == 0 and password.lower() == 'admin':
            customer = 'admin'
            AdminMenu()
        else:
            print('Invalid Customer ID. Please try again.')
            login(customer_records)



def AdminMenu():
    print(f'\n{'Admin View - Caledonia Bank':{'-'}^{50}}\n\n\n1: View all Caledonia Bank Accounts\n2: View all Customer Records\n3: Erase All Stored Data\n4: Logout')
    
    user_input = get_input(1,4)
    
    #view all accounts
    if user_input == 1:
        print('\n------- All Bank Accounts:')
        
        # get accounts data from file
        try:
            with open('Accounts.json', 'r', encoding='utf-8') as infile:
                # avoid error when file is empty -> sets to empty dict if empty
                file_content = infile.read()
                if file_content:
                    accounts_data = json.loads(file_content) # load using json module
                else:
                    accounts_data = {}
        
        
            # check the accounts exist before trying to print them
            if accounts_data == {}:
                print('There are no account records stored.') 
            else:
                # iterate over all customers accounts
                for customer_id, accounts in accounts_data.items():
                    # if a customer has not activated/ created any account, do not display their accounts
                    if accounts['current_account']['account_number'] == -1 and accounts['savings_account']['account_number'] == -1 and accounts['mortgage_account']['account_number'] == -1:
                        continue
                    else:
                        print(f'\nCustomer ID: {customer_id}')
                    for account_type, account_details in accounts.items():
                        # if account number is set to -1 (indicating account has not been created/ activated), do not display this account  
                        if account_details['account_number'] == -1:
                            continue  # Skip the account if the account number is -1
                        print(f'\n      {account_type.capitalize()}:')
                        # display all attributes fo the account
                        for key, value in account_details.items():
                            

                            # convert format of interest rate from decimal to percentage to diaplay in terminal
                            if key == 'interest_rate':
                                value = f'{value * 100:.2f}%'
                            
                            # add '£' when displaying the balance
                            if key == 'balance':
                                value = f'£{value}'
                            print(f'            {key.replace('_', ' ').capitalize()}: {value}')
        except FileNotFoundError:
                    print('The customer records file cannot be found.')
    
    # View all customer records
    if user_input == 2:
        print('\n------- All Customer Records:')
        all_customer_records = LoadCustomerRecords()
        if all_customer_records == {}:
            print('There area no customer records stored.')
        else:
            # iterate over each key:value pair
            for cust_id, cust_details in all_customer_records.items():
                print(f'\nCustomer ID: {cust_id}\nFull Name: {cust_details[0]}\nPassword: {cust_details[1]}')
            
    if user_input == 3:
        # Clear all data stored in the files:
        with open ('Accounts.json', 'w') as out:
            out.write('')
        with open ('last_account_no.txt', 'w') as out:
            out.write('')
        with open ('customer_records.txt', 'w') as out:
            out.write('')
        with open ('last_customer_id.txt', 'w') as out:
            out.write('')
        
    if user_input == 4:
        logout()



def RetrieveAccount():
    # read in json data from accounts file
    with open('Accounts.json', 'r', encoding='utf-8') as infile:
            # avoid error when file is empty -> sets to empty dict if empty
            file_content = infile.read()
            if file_content:
                accounts_data = json.loads(file_content)
            else:
                accounts_data = {}
    
    # look for customers id number in the accounts data.
    if str(customer.customer_id) in accounts_data:
        #if record of accounts exists for this customer, import data stored in json file and store as object
        
        #import stored current account data
        customer.current_account.account_number = accounts_data[str(customer.customer_id)]['current_account']['account_number']
        customer.current_account.balance = accounts_data[str(customer.customer_id)]['current_account']['balance']
        customer.current_account.interest_rate = accounts_data[str(customer.customer_id)]['current_account']['interest_rate']
        
        # import stored savings account data
        customer.savings_account.account_number = accounts_data[str(customer.customer_id)]['savings_account']['account_number']
        customer.savings_account.balance = accounts_data[str(customer.customer_id)]['savings_account']['balance']
        customer.savings_account.interest_rate = accounts_data[str(customer.customer_id)]['savings_account']['interest_rate']
        
        # import stored mortgage account data
        customer.mortgage_account.account_number = accounts_data[str(customer.customer_id)]['mortgage_account']['account_number']
        customer.mortgage_account.balance = accounts_data[str(customer.customer_id)]['mortgage_account']['balance']
        customer.mortgage_account.interest_rate = accounts_data[str(customer.customer_id)]['mortgage_account']['interest_rate']



def register():
    print(f'\n{'Register with Caledonia Bank':{'-'}^{50}}\n')
    # get user details for customer records
    first_name = input('Enter your first name: ')
    last_name = input('Enter your last name: ')
    name = first_name.capitalize() + ' ' + last_name.capitalize()
    password = input('Enter your password: ')
    
    try:
        with open('last_customer_id.txt', 'r', encoding='utf-8') as file:
            # Read the last id number assigned from the file (this ensures that no id is used twice)
            last_id = int(file.read().strip())
    except FileNotFoundError:
        # execute if file doesnt exist
        print('\nERROR: File containing the last used customer ID number not found. New account will be assigned 1 as the customer ID by default')
        last_id = 0
    except ValueError:
        # execute if value read in from file is not convertible to int ( ie. if file is empty)
        print('\nERROR: Value stored as last customer ID used was not a number. New account will be assigned 1 as the customer ID by default.')
        last_id = 0

    customer_id = last_id + 1 # makes sure each ID is unique
    
    #create instance of class (global variable)
    new_customer = Customer(customer_id, name, password)
    
    #write new id list to file
    with open('last_customer_id.txt', 'w', encoding='utf-8') as out:
        out.write(str(customer_id))           

    #store customer record as dict with id as key and name and password as values in a list. store in .txt file.
    new_customer_record = {new_customer.customer_id : [new_customer.name, new_customer.password]}
    
    with open('customer_records.txt', 'a', encoding='utf-8') as out:
        out.write(f"{list(new_customer_record.keys())[0]}: {new_customer_record[list(new_customer_record.keys())[0]]}\n")
        
    # when a new customer registers, create a record for them in the accounts file with empty entries to be populated when accounts are created

    print(f'\n\nYou successfully registered as a customer with Caledonia Bank!\n\nYour customer details:\n\nCustomer ID: {customer_id}\nName: {name}\nPassword: {password}\n\nYou will now be redirected to the home page.')
    sleep(4)
    
    WelcomePage()



def CustomerHomepage():
    print(f'\n{'Customer Homepage':{'-'}^{50}}\n')
    print('Logged in as {}.'.format(customer.name))
    print('\nPlease select one of the following options:\n1: View state of all of your accounts\n2: Open A New Account\n3: Select one of your accounts to interact with\n4: Apply Interest to all accounts\n\n5: Logout')
    
    valid = False
    logged_out = False
    # keep running the customer homepage until customer decides to log out
    while valid == False or logged_out == False:
        user_input = get_input(1, 5) # function to get input in range given and handle errors
        
        if user_input == 1:
            valid = True
            ViewCustomerAccounts()
        elif user_input == 2:
            valid = True
            CreateAccount()
        elif user_input == 3:
            valid = True
            DepositWithdrawBalance()
        elif user_input == 4:
            valid = True
            #add interest to all accounts that exist (where account number doesn't equal -1).
            if customer.current_account.account_number != -1:
                customer.current_account.AddInterest()
            if customer.savings_account.account_number != -1:
                customer.savings_account.AddInterest()
            if customer.mortgage_account.account_number != -1:
                customer.mortgage_account.ApplyInterest() # different function used for the mortgage as teh interest is deducted from it (it is added in the other cases)
        elif user_input == 5:
            valid = True
            logged_out = True
            logout()
            break # break out of loop when user logs out.
        
        else:
            print('Invalid input. Try again...')


def logout():
    print('\nLogging out...')
    sleep(1)
    
    
    # program should only try to write customer details to file if a customer is logged in. If admin logged in, skip the write to file as no customer records have been changed.
    if customer != 'admin':
        # read in records of accounts
        with open('Accounts.json', 'r', encoding='utf-8') as infile:
            # avoid error when file is empty
            file_content = infile.read()
            accounts_data = json.loads(file_content)
    
        # update stored record for the current user:
        accounts_data[str(customer.customer_id)] = {
            "current_account": {
                "account_number": int(customer.current_account.account_number),
                "balance": customer.current_account.balance,
                "interest_rate": customer.current_account.interest_rate
            },
            "savings_account": {
                "account_number": int(customer.savings_account.account_number),
                "balance": customer.savings_account.balance,
                "interest_rate": customer.savings_account.interest_rate
            },
            "mortgage_account": {
                "account_number": int(customer.mortgage_account.account_number),
                "balance": customer.mortgage_account.balance,
                "interest_rate": customer.mortgage_account.interest_rate
            }
        }
        
        # write updated records back into accounts.json
        with open('Accounts.json', 'w', encoding='utf-8') as out:
            json.dump(accounts_data, out, indent=4)
    
    sys.exit() # stops program when user logs out



def ViewCustomerAccounts():
    print(f'\n{'Accounts View':{'-'}^{50}}\n')
    #check that account number is not set to -1 (indicating account has not been created)  and print all active accounts
    has_account = False
    if customer.savings_account.account_number != -1:
        print(customer.savings_account)
        has_account = True
    if customer.current_account.account_number != -1:
        has_account = True
        print(customer.current_account)
    if customer.mortgage_account.account_number != -1:
        has_account = True
        print(customer.mortgage_account)
    if has_account == False:
        print('You do not have any open accounts.\nIf you would like to open one, return to the Customer Homepage.')

    # MINI MENU: LOGOUT OR RETURN TO MENU
    valid = False   
    while valid == False:
        print('\n\nPlease select one of the following options:\n1: Return to Customer Homepage\n2: Log out')
        user_input = get_input(1,2)
        if user_input == 1:
            valid = True
            CustomerHomepage()
        elif user_input == 2:
            valid = True
            logout()
        else:
            print('Error: invalid input. Retry...')



def CreateAccount():
    print(f'\n{'Open a Caledonian Bank Account':{'-'}^{50}}\n')
    print('Types of bank account:\n1: Current Account\n2: Savings Account\n3: Mortgage')
    
    user_input = get_input(1, 3)
    
    #get last used account number to ensure no accounts are assigned the same account number
    try:
        with open('last_account_no.txt', 'r', encoding='utf-8') as inp:
            last_account_number = int(inp.read())
    except FileNotFoundError:
        print('\nERROR: File containing the last used account number not found. New account will be assigned 1 as the account number by default')
        last_account_number = 0
    except ValueError:
        print('\nERROR: Value stored as last account number used was not a number. New account will be assigned 1 as the account number by default.')
        last_account_number = 0
        
    with open('last_account_no.txt', 'w', encoding='utf-8') as out:
        out.write(str(last_account_number + 1)) # needs to be string to write to file.
        
        
    if user_input == 1:
        if customer.current_account.account_number == -1:
            customer.current_account.account_number = last_account_number + 1
            print('\nSuccessfully opened current account.')
            print(customer.current_account)
            sleep(2)
            # Add account to file with all account records:
            SaveAccountToFile(account_type='current')
        else:
            print(f'\nYou already hold a current account with Caledonia Bank.:\n{customer.current_account}')

        
    elif user_input == 2:
        # set account number on savings account to create it.
        if customer.savings_account.account_number == -1:
                
            customer.savings_account.account_number = last_account_number + 1
            print('\nYou have successfully created a savings account.\n')
            print(customer.savings_account)
            sleep(2)
            # Add account to file with all account records:
            SaveAccountToFile(account_type='savings')
        else:
            print(f'\nYou already hold a savings account with Caledonia Bank.:\n{customer.savings_account}')

        
    elif user_input == 3:
        # set account number on savings account to create it.
        customer.mortgage_account.account_number = last_account_number + 1
        valid = False # initialise variable to control while loop
        while valid == False:
            try:
                mortgage_value = float(input('Enter the value of your mortgage: £'))
                if mortgage_value > 0:
                    valid = True
                    customer.mortgage_account.balance = mortgage_value
                # allow a mortgages offered by caledonia bank for values up to £1 million
            except ValueError:
                print('Re-enter the value of your mortgage. Value must be a positive number.')
                
        
        print('\nYou have successfully created a mortgage account.\n')
        print(customer.mortgage_account)
        sleep(2)
        # Add account to file with all account records:
        SaveAccountToFile(account_type='mortgage')

    CustomerHomepage()



def SaveAccountToFile(account_type):
    # try to read data from the account.json. handle exception of filenotfound and set empty dictionary to populate
    try:
        with open('Accounts.json', 'r', encoding='utf-8') as infile:
            # avoid error when file is empty
            file_content = infile.read()
            if file_content:
                accounts_data = json.loads(file_content)
            else:
                accounts_data = {} # set to empty dictionary if cant be laoded from file
    except FileNotFoundError:
        accounts_data = {}
        print('The file containing records of accounts was not found. A new file will be created now. Any previously stored records are not retrievable.')

    # check customer account data is stored in file. this will only run when the customer opens their first account
    if str(customer.customer_id) not in accounts_data:
        # initialise record for currently logged in customer
        accounts_data[str(customer.customer_id)] = {
            "current_account": {
                "account_number": int(customer.current_account.account_number),
                "balance": customer.current_account.balance,
                "interest_rate": customer.current_account.interest_rate
            },
            "savings_account": {
                "account_number": int(customer.savings_account.account_number),
                "balance": customer.savings_account.balance,
                "interest_rate": customer.savings_account.interest_rate
            },
            "mortgage_account": {
                "account_number": int(customer.mortgage_account.account_number),
                "balance": customer.mortgage_account.balance,
                "interest_rate": customer.mortgage_account.interest_rate
            }
        }
    
    with open('Accounts.json', 'w', encoding='utf-8') as out:
        #   write accounts data to file when the account number of the account has been updated to indicate it is active.
        if account_type == 'current':
            # only account number needs updated (from -1 to indicate account is active)
            accounts_data[str(customer.customer_id)]['current_account']['account_number'] = customer.current_account.account_number
            json.dump(accounts_data, out, indent=4)
            
        if account_type == 'savings':
            # only account number needs updated (from -1 to indicate account is active)
            accounts_data[str(customer.customer_id)]['savings_account']['account_number'] = customer.savings_account.account_number
            json.dump(accounts_data, out, indent=4)
            
        if account_type == 'mortgage':
            # only account number needs updated (from -1 to indicate account is active)
            accounts_data[str(customer.customer_id)]['mortgage_account']['account_number'] = customer.savings_account.account_number
            json.dump(accounts_data, out, indent=4)
            


def DepositWithdrawBalance():
    #check what accounts the customer has (account is ACTIVE when account number != -1)
    current = False
    savings = False
    mortgage = False

    if customer.current_account.account_number != -1:
        current = True
    if customer.savings_account.account_number != -1:
        savings = True
    if customer.mortgage_account.account_number != -1:
        mortgage = True
    
    # NO ACC.
    if current == False and savings == False and mortgage == False:
        print('\n\nYou do not have any accounts to interact with. Please open one.')
        CustomerHomepage()
        
    # ONLY CURRENT ACC.
    if current == True and savings == False and mortgage == False:
        print('\n\nYou have a current account.\nWhat action would you like to complete?\n1: Deposit\n2: Withdraw\n3: Display Balance')
        
        selection = get_input(1, 3) # call function that will handle exceptions are errors
        
        if selection == 1:
            customer.current_account.deposit()
        elif selection == 2:
            customer.current_account.withdraw()
        elif selection == 3:
            customer.current_account.check_balance()
        
        CustomerHomepage()
    
    # ONLY SAVINGS ACC.
    if savings == True and current == False and mortgage == False:
        print('\n\nYou have a savings account.\nWhat action would you like to complete?\n1: Deposit\n2: Withdraw\n3: Display Balance')
        
        selection = get_input(1, 3) # call function that will handle exceptions are errors
        
        if selection == 1:
            customer.savings_account.deposit()
        elif selection == 2:
            customer.savings_account.withdraw()
        elif selection == 3:
            customer.savings_account.check_balance()
        
        CustomerHomepage()
    
    
    # ONLY MORTGAGE ACC
    if mortgage == True and current == False and savings == False:
        print('\n\nYou have a mortgage account.\nWhat action would you like to complete?\n1: Monthly Capital Repayment\n2: Display Balance')
        
        selection = get_input(1, 2) # call function that will handle exceptions are errors
        if selection == 1:
            customer.mortgage_account.CapitalRepayment(customer.current_account.balance)
        elif selection == 2:
            customer.mortgage_account.check_balance()

        CustomerHomepage()
        
        
    # CURRENT & SAVINGS
    if current == True and savings == True and mortgage == False:
        print('\n\n Select one of your accounts:\n1: Current Account\n2: Savings Account')
        user_input = get_input(1, 2)
        if user_input == 1:
            print('\n\nYou have selected your current account.\n\nSelect an action:\n1: Deposit\n2: Withdraw\n3: Display Balance')
            selection = get_input(1, 3) # call function that will handle exceptions are errors
            if selection == 1:
                customer.current_account.deposit()
            elif selection == 2:
                customer.current_account.withdraw()
            elif selection == 3:
                customer.current_account.check_balance()
        
        if user_input == 2:
            print('\n\nYou have selected your savings account.\n\nSelect an action:\n1: Deposit\n2: Withdraw\n3: Display Balance')
            selection = get_input(1, 3) # call function that will handle exceptions are errors
            if selection == 1:
                customer.savings_account.deposit()
            elif selection == 2:
                customer.savings_account.withdraw()
            elif selection == 3:
                customer.savings_account.check_balance()

        CustomerHomepage()

    # CURRENT & MORTGAGE
    if current == True and savings == False and mortgage == True:
        print('\n\n Select one of your accounts:\n1: Current Account\n2: Mortgage Account')
        user_input = get_input(1, 3)
    
        if user_input == 1:
            print('\n\nYou have selected your current account.\n\nSelect an action:\n1: Deposit\n2: Withdraw\n3: Display Balance')
            selection = get_input(1, 3) # call function that will handle exceptions are errors
            if selection == 1:
                customer.current_account.deposit()
            elif selection == 2:
                customer.current_account.withdraw()
            elif selection == 3:
                customer.current_account.check_balance()
        
        if user_input == 2:
            
            print('\n\nYou have selected your mortgage account.\n\nSelect an action:\n1: Monthly Capital Repayment\n2: Display Balance')
            selection = get_input(1, 3) # call function that will handle exceptions are errors
            if selection == 1:
                customer.mortgage_account.CapitalRepayment(customer.current_account.balance)
            elif selection == 2:
                customer.mortgage_account.check_balance()

        CustomerHomepage()


    # SAVINGS AND MORTGAGE
    if current == False and savings == True and mortgage == True:
        print('\n\n Select one of your accounts:\n1: Savings Account\n2: Mortgage Account')
        user_input = get_input(1, 2)
        if user_input == 1:
            print('\n\nYou have selected your savings account.\n\nSelect an action:\n1: Deposit\n2: Withdraw\n3: Display Balance')
            selection = get_input(1, 3) # call function that will handle exceptions are errors
            if selection == 1:
                customer.savings_account.deposit()
            elif selection == 2:
                customer.savings_account.withdraw()
            elif selection == 3:
                customer.savings_account.check_balance()
        
        if user_input == 2:
            print('\n\nYou have selected your mortgage account.\n\nSelect an action:\n1: Deposit\n2: 2: Monthly Capital Repayment\n3: Display Balance')
            selection = get_input(1, 3) # call function that will handle exceptions are errors
            if selection == 1:
                customer.mortgage_account.CapitalRepayment(customer.current_account.balance)
            elif selection == 2:
                customer.mortgage_account.check_balance()

        CustomerHomepage()

    # CURRENT, SAVINGS & MORTGAGE
    if current == True and savings == True and mortgage == True:
        print('\n\n Select one of your accounts:\n1: Current Account\n2: Savings Account\n3: Mortgage Account')
        user_input = get_input(1, 3)
        
        if user_input == 1:
            print('\n\nYou have selected your savings account.\n\nSelect an action:\n1: Deposit\n2: Withdraw\n3: Display Balance')
            selection = get_input(1, 3) # call function that will handle exceptions are errors
            if selection == 1:
                customer.current_account.deposit()
            elif selection == 2:
                customer.current_account.withdraw()
            elif selection == 3:
                customer.current_account.check_balance()
        
        if user_input == 2:
            print('\n\nYou have selected your savings account.\n\nSelect an action:\n1: Deposit\n2: Withdraw\n3: Display Balance')
            selection = get_input(1, 3) # call function that will handle exceptions are errors
            if selection == 1:
                customer.savings_account.deposit()
            elif selection == 2:
                customer.savings_account.withdraw()
            elif selection == 3:
                customer.savings_account.check_balance()
        
        if user_input == 3:
            print('\n\nYou have selected your mortgage account.\n\nSelect an action:\n1: Deposit\n2: 2: Monthly Capital Repayment\n3: Display Balance')
            selection = get_input(1, 3) # call function that will handle exceptions are errors
            if selection == 1:
                customer.mortgage_account.CapitalRepayment(customer.current_account.balance)
            elif selection == 2:
                customer.mortgage_account.check_balance()

        CustomerHomepage()


# function to get an input for the menus (ensures user only enters one of options in the menu and handles any errors that may arise from user input). function created for this as it is used in all menus
def get_input(min, max):
    while True: # loop until input is valid
        try:
            user_input = int(input('Select an option: '))
            if min <= user_input <= max:
                return user_input
            else:
                print(f'\nYour selection was invalid. Please re-enter a number between {min} and {max}.')
        except ValueError:
            # if entered value is not an int:
            print('\nInvalid input. Please re-enter an integer.')






# --------- PROGRAM CODE 


# launch welcome menu to start application
WelcomePage()

