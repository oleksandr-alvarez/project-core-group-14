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
        if len(text) < 2 or len(text) > 20: # Домовились, що Даша знімить верхнє обмеження
            return False
        for digit in digits + punctuation:
            if digit in text:
                return False
        return True
    
    @can_be_empty
    def valid_as_address(self, text): 
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
                    address: str = None, 
                    phone_number: str = None, 
                    email: str = None,
                    birthday: str = None,
                    notes: str = None
                ):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.birthday = birthday
        self.notes = notes

    @property
    def row(self):
        return [self.name, self.phone_number, self.email, self.address, self.birthday, self.notes._value]
    
    
    def __repr__(self):
        return f"Person {self.name}, {self.address}, {self.phone_number}, {self.email}, {self.birthday}"
    

class Notes:

    def __init__(self, value) -> None:
        self._value = value
        self._tags = None
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value): 
        if new_value:
            self._value = new_value

    @property
    def tags(self):
        if self._tags:
            return self._tags
        return f'There are no tags.'
        
    @tags.setter
    def tags(self, new_tag_values):
        if new_tag_values:
            self._tags = new_tag_values
    
    def delete(self):
        if self._value:
            self._value = None
            return "Notes have been deleted."
        return "There are not notes."




class Helper:    

    def __init__(self):
        self.people = []
        self.validator = Validator()
        self._attributes = ['name', 'phone number', 'email address', 'address', 'birthday date', 'notes']
    
    def _message(self, attribute, valid_input = True):
        
        if valid_input:
            return  f'Enter your {self._attributes[self._attributes.index(attribute)]}: ' if attribute != 'birthday date' else f'Enter your {self._attributes[self._attributes.index(attribute)]} (e.g., 23 May): '
        return f"You have entered invalid {self._attributes[self._attributes.index(attribute)]}. Please recheck and try again. "    

    def create(self):
        
        name = self.validator.valid_input( self.validator.valid_as_name, self._message('name'),  self._message('name', 0) )
        phone_number = self.validator.valid_input( self.validator.valid_as_phone_number, self._message('phone number'), self._message('phone number', 0))
        email = self.validator.valid_input( self.validator.valid_as_email, self._message('email address'), self._message('email address', 0) )
        address = self.validator.valid_input( self.validator.valid_as_address, self._message('address'), self._message('address', 0) )
        birthday = self.validator.valid_input( self.validator.valid_as_birthday, self._message('birthday date'), self._message('birthday date', 0)  )
        notes = Notes(input(self._message('notes')))

        new_person = Person( name, address, phone_number, email, birthday, notes )
        self.people.append( new_person )


    def edit_attribute_menu(self, contact):
        # Добавить кнопку отмены
        
        text = """Choose attribute to edit:\n1. Name\n2. Phone\n3. Email\n4. address\n5. Birthday\n6. Notes\n0. Cancel\nYour choice: """
        attribute = input(text)
        if attribute == "1":
            contact.name = self.validator.valid_input( self.validator.valid_as_name, self._message('name'),  self._message('name', 0) )
        elif attribute == "2":
            contact.phone_number = self.validator.valid_input( self.validator.valid_as_phone_number, self._message('phone number'), self._message('phone number', 0))
        elif attribute == "3":
            contact.email = self.validator.valid_input( self.validator.valid_as_email, self._message('email address'), self._message('email address', 0) )
        elif attribute == "4":
            contact.address =self.validator.valid_input( self.validator.valid_as_address, self._message('address'), self._message('address', 0) )
        elif attribute == "5":
            contact.birthday = self.validator.valid_input( self.validator.valid_as_birthday, self._message('birthday date'), self._message('birthday date', 0)  )
        elif attribute == "6":
            edit_delete_note_input = input('\n1. Edit note.\n2. Delete note.\nYour choice: ').strip()
            if edit_delete_note_input == '1':
                contact.notes.value = input('Please enter your new note: ')
            elif edit_delete_note_input == '2':
                contact.notes.delete()
        


    def edit(self):
        text = "Enter contact name to edit: "
        contact_name = input(text)
        found = list(filter( lambda con: contact_name.lower() in con.name.lower(), self.people ))

        if found:
            if len(found) == 1:
                self.edit_attribute_menu( found[0] )
                return 1
            else:
                table = PrettyTable()
                table.field_names = ["№", "Name"]
                for index, con in enumerate(found):
                    table.add_row( (index, con.name) )
                print( table )
                number = input("Choose number contact to change: ")
                if number.isdigit() and int(number) < len(found):
                    self.edit_attribute_menu( found[int(number)] )
                    return 1
                # ------------- ВЕРНУТСЯ В ГЛАВНЫЙ ЦИКЛ
        return 
        

    def delete_contact(self):
        name_to_delete = input("Enter the name of the contact you want to delete: ")
        matching_contacts = [person for person in self.people if person.name.lower() == name_to_delete.lower()]

        if not matching_contacts:
            print(f"No contact with the name '{name_to_delete}' found.")
        else:
            if len(matching_contacts) == 1:
                contact_to_delete = matching_contacts[0]
                self.people.remove(contact_to_delete)
                print(f"{contact_to_delete.name} has been deleted.")
            else:
                print("Contacts with the same name found. Please select the contact to delete:")
                table = PrettyTable()
                table.field_names = ["ID", "Name", "Phone"]
                for index, contact in enumerate(matching_contacts):
                    table.add_row([index, contact.name, contact.phone_number])
                print(table)
                contact_id = int(input("Enter the ID of the contact to delete: "))
                if 0 <= contact_id < len(matching_contacts):
                    contact_to_delete = matching_contacts[contact_id]
                    self.people.remove(contact_to_delete)
                    print(f"{contact_to_delete.name} has been deleted.")
                else:
                    print("Invalid ID. No contact has been deleted.")


    def find_by_coming_birthday(self, days_count):
        # ПОЛНОСТЬЮ ПЕРЕПИСАТТЬ 
        goal_people = []
        for person in self.people:
            if person.birthday.day - datetime.now().day == days_count:
                goal_people.append( person )
        return goal_people
    
    def find_by_coming_birthday_menu( self ):
        ans = int(input("Enter days count: "))
        while ans.isdigit() and ans < 0:
            print( "You can enter only positive value" )
            ans = int(input("Enter days count: "))
        print( self.find_by_coming_birthday_menu( ans ) )

    def display_contacts(self):
        table = PrettyTable()
        table.field_names = [attr.upper() for attr in self._attributes]
        for con in self.people:
            table.add_row( con.row )
        print( table )

    def search_contact(self):
        search_term = input("Enter a name or phone number to search for: ").strip().lower()
        results = []

        for contact in self.people:
            if search_term in contact.name.lower() or (contact.phone_number and search_term in contact.phone_number):
                results.append(contact)

        if results:
            table = PrettyTable()
            table.field_names = [attr.upper() for attr in self._attributes]
            for contact in results:
                table.add_row(contact.row)
            print("\nSearch results:")
            print(table)
        else:
            print(f"No contacts found for '{search_term}'.")    


    def menu(self):
        while True:
            menu_text = """Menu:\n1. Create a new contact\n2. Edit contact\n3. Find by coming birthday\n4. Display contacts\n5. Delete contact\n6. Search contacts\n0. Exit\nChoose a number: """
            ans = input(menu_text)
            if ans == "1":
                self.create()
                print('Contact has been created.')
            elif ans == "2":
                edit_success = self.edit()
                print("Changes have been saved") if edit_success else print('Contact not found. Please try again.')
            elif ans == "3":
                self.find_by_coming_birthday_menu()
            elif ans == "4":
                self.display_contacts()
            elif ans == "5":
                self.delete_contact()
            elif ans == "6":
                self.search_contact()    
            else:
                return

h = Helper()
h.menu()
