from datetime import datetime, date, timedelta
from collections import UserList
import pickle

from util_func import *
import sort


class Contact:

    id = 0
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
        self.id = Contact.id
        Contact.id += 1

    @property
    def value(self):
        return [self.name, self.phone_number, self.email, self.address, self.birthday, self.notes._value]
    
    @property
    def value_id(self):
         return [self.id, self.name, self.phone_number, self.birthday, self.email, self.address, self.notes._value]
    
    def edit_attribute(self, attribute, new_value):
        if attribute == 'name':
            self.name = new_value
        elif attribute == 'phone number' : 
            self.phone_number = new_value
        elif attribute == 'email' : 
            self.email = new_value
        elif attribute.find('address') >= 0: 
            self.address = new_value
        elif attribute == 'birthday date' : 
            self.birthday = new_value
        elif attribute.find('notes') >= 0: 
            self.notes.value = new_value
        
class Book(UserList):  

    def add_contact(self, contact):
        self.data.append(contact)

    def existing_contact_names(self):
        contact_names = [contact.name for contact in self.data]
        return contact_names

    def find_contacts_of_names(self, contact_to_find):
        contacts_to_find = []
        for contact in self.data:
            if contact_to_find in contact.name:
                contacts_to_find.append(contact)
        
        return contacts_to_find
    
    def find_nearest_birthday_people(self, number_of_days):
        today = datetime.today().date()
        today_future_date = today + timedelta(days=number_of_days)
        contacts_within_timeframe = []
        
        for contact in self.data:
            split_char = contact.birthday[2]
            birthday_of_contact = contact.birthday.split(split_char)
            birthday_of_contact = date(int(birthday_of_contact[2]), 
                                       int(birthday_of_contact[1]), 
                                       int(birthday_of_contact[0]))
            birthday_of_contact = birthday_of_contact.replace(year = today.year)
            if today <= birthday_of_contact <= today_future_date:
                contacts_within_timeframe.append(contact)

        return contacts_within_timeframe
    
    def find_contacts_by_id(self, find_id):
        found_contacts = []
        for contact in self.data:
            if find_id == contact.id:
                found_contacts.append(contact)
        
        return found_contacts
    
    def find_contacts_by_name(self, name):
        found_contacts = []
        for contact in self.data:
            if name == contact.name:
                found_contacts.append(contact)
        return found_contacts
    
    def delete_contact_by_id(self, id):
        contact_index = 0
        for contact in self.data:
            if contact.id == id:
                self.data.pop(contact_index)
            contact_index += 1
        return contact
    
    def find_contact_by_notes(self, notes):
        found_contacts = []
        for contact in self.data:
            if contact.notes.value.lower().find(notes.lower()) >= 0:
                found_contacts.append(contact)
        
        return found_contacts
    
    def tags_in_book(self):
        for contact in self.data:
            if contact.notes._tags:
                return True
    

class Notes:

    def __init__(self, value) -> None:
        self._value = value
        self._tags = set()
    
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
            return ', '.join([str(tag) for tag in self._tags])
        return f'There are no tags.'
        
    @tags.setter
    def tags(self, new_tag_values):
        if new_tag_values:
            for tag in new_tag_values:
                self._tags.add(tag.strip())
   
    def delete(self):
        if self._value:
            self._value = None
            return "Notes have been deleted."
        return "There are not notes."
    
    def add_tags(self, new_tag):
        for tag in new_tag:
            self._tags.update(tag.strip())



def main():
    MENU_TEXT = """\nMenu:\n1. Create a new contact\n2. Edit contact\n3. Find nearest birthday people\n4. Display all contacts\n5. Find contacts\n6. Delete contact\n7. Find notes\n8. Sort or find contacts by tags\n9. Sort folders in the path\n10. Save information as a file\n11. Load data from a file\n0. Exit bot-assistant\n"""
    THERE_ARE_NO_CONTACTS_TEXT = f'{TextColor.RED}There no contacts yet. Please create a new contact.{TextColor.RESET}'

    CREATE_NEW_CONTACT_TEXT = "\nTo create a new contact I will ask you for a name, phone number, email addrees, address, birthday date, notes.\nContact can't be created without a name.\n"
    EDIT_TEXT = """\nChoose attribute to edit:\n1. Name\n2. Phone number\n3. Birthday date\n4. Email address\n5. Address\n6. Notes\n7. Tags\n"""

    contacts = Book()

    while True:
        print(MENU_TEXT)
        menu_choice = valid_choice_menu_edit_find('menu')
        if not menu_choice:
            print(not_valid_message('choice'))
            continue

        if menu_choice == '0':
            break
        
        if menu_choice == '1':
            print(CREATE_NEW_CONTACT_TEXT)

            input_name = valid_name('name')
            input_phone_number = valid_phone_number('phone number', contacts)
            input_birthday = valid_birthday('birthday date')
            input_email = valid_email('email address')
            input_address = input(f'{TextColor.YELLOW}Please enter address: {TextColor.RESET}')
            input_notes = Notes(input(f"{TextColor.YELLOW}Please enter notes: {TextColor.RESET}"))
            
            new_contact = [Contact(input_name, input_address, input_phone_number, input_email, input_birthday, input_notes)]
            
            input_tags = input(f"{TextColor.YELLOW}Would you like to add tags to this contact? (Please separate them by comma)\nTags: {TextColor.RESET}").lower().strip()
            if input_tags:
                new_contact[0].notes.tags = input_tags.split(',')

            contacts.add_contact(new_contact[0])

            print(f"{TextColor.GREEN}\nContact has been created.{TextColor.RESET}")
            display_contacts(new_contact)

        if menu_choice == '2':
            if contacts:
                name_of_contact_to_edit = valid_name('name to edit')
                found_contacts =  list(filter(lambda x: name_of_contact_to_edit in x, contacts.existing_contact_names()))
                if len(found_contacts) > 1:
                    print("There are several contacts in the book.")
                    found_contacts = contacts.find_contacts_of_names(name_of_contact_to_edit)
                    display_contacts(found_contacts)
                    id_of_the_contact_to_edit = input(f"{TextColor.YELLOW}\nChoose ID: {TextColor.RESET}")
                    contact_to_edit = [contact for contact in found_contacts if contact.id == int(id_of_the_contact_to_edit)]
                    display_contacts(contact_to_edit)
                if len(found_contacts) == 1:
                    contact_to_edit = contacts.find_contacts_of_names(name_of_contact_to_edit)
                    display_contacts(contact_to_edit)
                if len(found_contacts) == 0:
                    print(f'{TextColor.MAGENTA}There is no contact named {name_of_contact_to_edit}.{TextColor.RESET}')
                    continue

            else:
                print(THERE_ARE_NO_CONTACTS_TEXT)
                continue

            print(EDIT_TEXT)
            
            edit_choice = valid_choice_menu_edit_find('edit')
            
            command, arg = get_attribute_to_edit(edit_choice)
            
            if arg == 'phone number':
                new_value_of_attribute = command(arg, contacts)

            elif arg == "":
                
                show_input_tag(contact_to_edit[0])
                continue 
                    
            else:
                new_value_of_attribute = command(arg)
            

            contact_to_edit[0].edit_attribute(arg, new_value_of_attribute)

            display_contacts(contact_to_edit)
        
        if menu_choice == '3':
            if contacts:
                days_within_to_search_birthday_people = int(get_valid_number_of_days())
                contacts_within_timeframe = contacts.find_nearest_birthday_people(days_within_to_search_birthday_people)
                if contacts_within_timeframe:
                    display_contacts(contacts_within_timeframe)
                print(f'{TextColor.MAGENTA}There are no coming birthdays in the nearest {days_within_to_search_birthday_people} days.{TextColor.RESET}')
            else:
                print(THERE_ARE_NO_CONTACTS_TEXT)
                continue

        if menu_choice == '4':
            if contacts:
                display_contacts(contacts)
            
            else:
                print(THERE_ARE_NO_CONTACTS_TEXT)
                continue
        
        if menu_choice == '5':
            if contacts:
                print("How do you want to find contacts?\n1. By ID\n2. By name")
                edit_contact_choice = valid_choice_menu_edit_find('find')

                if edit_contact_choice == '1':
                    id_to_find = get_valid_id_to_find(contacts)
                    found_contacts = contacts.find_contacts_by_id(id_to_find)
                    display_contacts(found_contacts)
                    continue

                if edit_contact_choice == '2':
                    
                    while True:
                        name_to_find = valid_name('name')
                        found_contacts = contacts.find_contacts_by_name(name_to_find)
                        if found_contacts:
                            display_contacts(found_contacts)
                            break
                        print(f'{TextColor.MAGENTA}There is no contact with such named {name_to_find}.{TextColor.RESET}\nWould you like to try again?\n1. Yes\n2. No')
                        decision_to_try_again = valid_choice_menu_edit_find('find')
                        if decision_to_try_again == 2:
                            break
        
            else:
                print(THERE_ARE_NO_CONTACTS_TEXT)
                continue
                
        if menu_choice == '6':
            if contacts:
                display_contacts(contacts)
                print('Which contact would you like to delete?')
                id_to_delete = int(get_valid_id_to_find(contacts))
                deleted_contact = [contacts.delete_contact_by_id(id_to_delete)]
                print(f"{TextColor.GREEN}The following contact has been deleted from the book:{TextColor.RESET}")
                display_contacts(deleted_contact)

            else:
                print(THERE_ARE_NO_CONTACTS_TEXT)
        
        if menu_choice == '7':
            if contacts:
                notes_to_find = input(f"{TextColor.YELLOW}Please enter notes you would like to find: {TextColor.RESET}")
                if not notes_to_find:
                    display_contacts(contacts)
                    continue
                found_contacts = contacts.find_contact_by_notes(notes_to_find)
                display_contacts(found_contacts)
            else:
                print(THERE_ARE_NO_CONTACTS_TEXT)
        
        if menu_choice == '9':
            folder_to_sort = get_valid_path()
            sort.sort_files_to_folders(folder_to_sort)
            print(f"{TextColor.GREEN}\nFolder is sorted. Go check it!{TextColor.RESET}")
        
        if menu_choice == '8':
            if contacts:
                find_sort_contacts_by_tags(contacts)
                continue
            print(THERE_ARE_NO_CONTACTS_TEXT)
        
        if menu_choice == '10':
            if contacts:
                with open('book_with_contacts.bin', "wb") as fh:
                    pickle.dump(contacts, fh)
                    print(f"{TextColor.GREEN}File has been saved.{TextColor.RESET}")
                    continue
            print(THERE_ARE_NO_CONTACTS_TEXT)
        if menu_choice == '11':
            contacts = load_data_from_file()
            print(f"{TextColor.GREEN}Data has been loaded!{TextColor.RESET}")
            display_contacts(contacts)

if __name__ == '__main__':
    main()         