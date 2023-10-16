from string import digits, punctuation
from prettytable import PrettyTable
import re

class Validator:
    @staticmethod
    def can_be_empty(func):
        def wrapper(self, value):
            if value != "":
                return func(self, value)
            else:
                return True
        return wrapper
    def valid_as_name(self, text):
        if len(text) < 2 or len(text) > 20:
            return False
        for digit in digits + punctuation:
            if digit in text:
                return False
        return True
    @can_be_empty
    def valid_as_adress(self, text):
        return True
    @can_be_empty
    def valid_as_phone_number(self, text):
        phone_number_patterns = [
            r'\+\d{1,4} \d{3} \d{2} \d{2} \d{2}',
            r'\+\d{1,4}-\d{3}-\d{2}-\d{2}-\d{2}',
            r"\+\d{10,12}",
        ]
        return any( [bool(re.fullmatch( ptrn, text )) for ptrn in phone_number_patterns] )
    @can_be_empty
    def valid_as_email(self, text):
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        return bool(re.fullmatch( email_pattern, text ))
    @can_be_empty
    def valid_as_birthday(self, text):
        days_count = {
            "January": 31,
            "February": 29,
            "March": 31,
            "April": 30,
            "May": 31,
            "June": 30,
            "July": 31,
            "August": 31,
            "September": 30,
            "October": 31,
            "November": 30,
            "December": 31,
        }
        if len(text.split()) != 2:
            return False
        days = int(text.split()[0])
        month = text.split()[1].lower().title()

        if (month not in days_count) or (days < 1 or days > days_count[month]):
            return False
        return True
    def valid_input( self, validator, text, error_text ):
        value = input(text)
        while not validator(value):
            print( error_text )
            value = input(text)
        return value

class Person:
    def __init__(self, 
                    name: str, 
                    adress: str = None, 
                    phone_number: str = None, 
                    email: str = None,
                    birthday: str = None
                ):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.adress = adress
        self.birthday = birthday
    @property
    def row(self):
        return [self.name, self.phone_number, self.email, self.adress, self.birthday]
    def __repr__(self):
        return f"Person({self.name}, {self.adress}, {self.phone_number}, {self.email}, {self.birthday}"

class Helper:
    def __init__(self):
        self.peoples = []
    def create(self):
        validator = Validator()

        name = validator.valid_input( validator.valid_as_name, "Enter name:", "You have entered the wrong name, please recheck and try again." )
        phone_number = validator.valid_input( validator.valid_as_phone_number, "Enter phone number:", "You have entered the wrong phone number, please recheck and try again." )
        email = validator.valid_input( validator.valid_as_email, "Enter email adress:", "You have entered the wrong email, please recheck and try again." )
        adress = validator.valid_input( validator.valid_as_adress, "Enter your adress:", "You have entered the wrong adress, please recheck and try again." )
        birthday = validator.valid_input( validator.valid_as_birthday, "Enter your birthday date(ex. 23 May):", "You have entered the wrong birthday date, please recheck and try again." )
        
        new_person = Person( name, adress, phone_number, email, birthday )
        self.peoples.append( new_person )
    def edit_attribute_menu(self, contact):
        # Добавить кнопку отмены
        validator = Validator()
        text = """Choose attribute to edit:\n1. Name\n2. Phone\n3. Email\n4. Adress\n5. Birthday\n6. Cancel\n"""
        attribute = input(text)
        if attribute == "1":
            contact.name = validator.valid_input( validator.valid_as_name, "Enter name:", "You have entered the wrong name, please recheck and try again." )
        elif attribute == "2":
            contact.phone_number = validator.valid_input( validator.valid_as_phone_number, "Enter phone number:", "You have entered the wrong phone number, please recheck and try again." )
        elif attribute == "3":
            contact.email = validator.valid_input( validator.valid_as_email, "Enter email adress:", "You have entered the wrong email, please recheck and try again." )
        elif attribute == "4":
            contact.adress = validator.valid_input( validator.valid_as_adress, "Enter your adress:", "You have entered the wrong adress, please recheck and try again." )
        elif attribute == "5":
            contact.birthday = validator.valid_input( validator.valid_as_birthday, "Enter your birthday date(ex. 23 May):", "You have entered the wrong birthday date, please recheck and try again." )
        print( "Changes has been saved" )
    def edit(self):
        text = "Enter contact name to edit: "
        contact_name = input(text)
        founded = list(filter( lambda con: contact_name.lower() in con.name.lower(), self.peoples ))
        if len(founded) == 1:
            self.edit_attribute_menu( founded[0] )
        else:
            table = PrettyTable()
            table.field_names = ["№", "Name"]
            for index, con in enumerate(founded):
                table.add_row( (index, con.name) )
            print( table )
            number = input("Choose number contact to change: ")
            if number.isdigit() and int(number) < len(founded):
                self.edit_attribute_menu( founded[int(number)] )
            # ------------- ВЕРНУТСЯ В ГЛАВНЫЙ ЦИКЛ
    def find_by_coming_birthday(self, days_count):
        # ПОЛНОСТЬЮ ПЕРЕПИСАТТЬ 
        goal_peoples = []
        for person in self.peoples:
            if person.birthday.day - datetime.now().day == days_count:
                goal_peoples.append( person )
        return goal_peoples
    def find_by_coming_birthday_menu( self ):
        ans = int(input("Enter days count: "))
        while ans.isdigit() and ans < 0:
            print( "You can enter only positive value" )
            ans = int(input("Enter days count: "))
        print( self.find_by_coming_birthday_menu( ans ) )
    def display_contacts(self):
        table = PrettyTable()
        table.field_names = ["Name", "Phone", "Email", "Adress", "Birthday"]
        for con in self.peoples:
            table.add_row( con.row )
        print( table )
    def menu(self):
        while True:
            menu_text = """1. Create new contact\n2. Edit contact\n3. Find by coming birthday\n4. Display contacts\n0. Exit\n"""
            ans = input(menu_text)
            if ans == "1":
                self.create()
            elif ans == "2":
                self.edit()
            elif ans == "3":
                self.find_by_coming_birthday_menu()
            elif ans == "4":
                self.display_contacts()
            else:
                return

h = Helper()
h.menu()
