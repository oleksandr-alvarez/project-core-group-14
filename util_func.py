from string import digits, punctuation
from prettytable import PrettyTable
from datetime import datetime
import pickle

import os
import re


class PhoneAlreadyExists(ValueError):
    pass

class BirthdayDateOfInvalidFormat(ValueError):
    pass

class EmailIsInInvalidFormat(ValueError):
    pass


class TextColor:

    RED = '\033[31m'
    GREEN = '\033[32m'
    RESET = '\033[0m'
    MAGENTA = '\033[35m'
    YELLOW = '\033[33m'


def number_of_commands(menu_or_edit):
    if menu_or_edit == 'menu':
        return 12
    if menu_or_edit == 'edit':
        return 7
    if menu_or_edit == 'find':
        return 2
    if menu_or_edit == 'tags choice':
        return 4
    



TABLE_COLUMNS = ['name', 'phone number', 'birthday date', 'email address', 'address', 'notes']



def not_valid_message(contact_detail):
    return f"{TextColor.RED}{contact_detail.capitalize()} is not valid.{TextColor.RESET}"

def get_attribute_to_edit(valid_number):
    commands = {
        '1' : valid_name,
        '2' : valid_phone_number,
        "4" : valid_email,
        '5' : input,
        '3' : valid_birthday,
        '6' : input,
        '7' : show_input_tag,
    }

    arg_of_command = {
        '1' : 'name',
        '2' : 'phone number',
        "4" : 'email address',
        '5' : f'{TextColor.YELLOW}Please enter address: {TextColor.RESET}',
        '3' : 'birthday date',
        '6' : f'{TextColor.YELLOW}Please enter notes: {TextColor.RESET}',
        '7' : '',
    }

    return commands[valid_number], arg_of_command[valid_number]



def is_folder_empty(path):
    try:
        items = os.listdir(path)
        for item in items:
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path):
                return False
            elif os.path.isdir(item_path):
                
                if not is_folder_empty(item_path):
                    return False
        return True
    except OSError as e:
        print(f"{TextColor.RED}Error accessing the directory: {e}{TextColor.RESET}")
        return False


def get_valid_path():
    while True:
        path_to_folder = input(f"{TextColor.YELLOW}Please provide a valid path to non-empty folder that you would like to sort: {TextColor.RESET}")
        if not is_folder_empty(path_to_folder):
            return path_to_folder
        else:
            print(f"{TextColor.RED}The folder is empty.{TextColor.RESET}")
        
    
def get_valid_input(func):
    def wrapper(input_value, *args):
        while True:
            attributes = {
                    'name' : 'name',
                    'birthday date' : 'birthday date (e.g., 01-01-1990)',
                    'email address' : 'email address (e.g., name@gmail.com)',
                    'address' : 'address',
                    'phone number' : 'phone number (e.g., +3801234567)',
                    'notes' : "notes",
                    'name to edit': "contact's name to edit"
                }

            user_input = input(f"{TextColor.YELLOW}Please enter a valid {attributes[input_value]}: {TextColor.RESET}").strip().capitalize()

            try:
                result = func(user_input, *args)
                if result:
                    return user_input
                else:
                    print(not_valid_message(f'{input_value.capitalize()}'))  
            except (PhoneAlreadyExists, BirthdayDateOfInvalidFormat, EmailIsInInvalidFormat) as e:
                    print(f'{TextColor.RED}{e}{TextColor.RESET}')
            except:
                print(not_valid_message(f'{input_value.capitalize()}'))
         
    return wrapper

def get_valid_choice(func):
    def wrapper(menu_edit_find):
        while True:
            user_input = input(f"{TextColor.YELLOW}Make a valid choice: {TextColor.RESET}").strip()
            if func(user_input, menu_edit_find):
                return user_input
            print(not_valid_message('choice'.capitalize()))
    return wrapper


def get_valid_number_of_days():
    while True:
        number_of_days = input("Please enter number of day within which you want to see birthdays: ")
        if number_of_days:
            if re.match('^(0|[1-9]\d*)$', number_of_days):
                return number_of_days
            print(not_valid_message('number'))
            continue
        continue

def get_valid_id_to_find(book):
    while True:
        id_to_find = input(f"{TextColor.YELLOW}Please enter a valid ID: {TextColor.RESET}")
        if id_to_find:
            if re.match('^(0|[1-9]\d*)$', id_to_find):
                if 0 < int(id_to_find) + 1 <= len(book):
                    return int(id_to_find)
                print('There is no such ID in the book.')
                continue
                
            print(not_valid_message('number'))
        


@get_valid_choice
def valid_choice_menu_edit_find(user_choice, menu_edit_find):
    # not_valid_message_choice = not_valid_message('choice')
    if user_choice:
        try:
            if int(user_choice) in range(0, number_of_commands(menu_edit_find) + 1):
                return user_choice
            return 0
        except:
            return 0
    return 0

@get_valid_input
def valid_name(name, *args):
    if len(name) < 2:
        return False
    for char in digits + punctuation:
        if char in name:
            return False
    return name
    

@get_valid_input   
def valid_phone_number(phone_number, book):
    if phone_number:
        valid_phone_number_patterns = [
            r'\+\d{1,4} \d{3} \d{2} \d{2} \d{2}',
            r'\+\d{1,4}-\d{3}-\d{2}-\d{2}-\d{2}',
            r"\+\d{10,12}",
        ]
        if any([bool(re.fullmatch(ptrn, phone_number)) for ptrn in valid_phone_number_patterns]):
            if phone_number not in [contact.phone_number for contact in book.data]:
                return phone_number
            raise PhoneAlreadyExists('Phone number already exists.')
    else:
        return True

    
@get_valid_input    
def valid_email(email_address, *args):
    if email_address:
        valid_email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if bool(re.fullmatch(valid_email_pattern, email_address)):
            return email_address
        raise EmailIsInInvalidFormat("Email address is in invalid format.")
    return True
    

@get_valid_input   
def valid_birthday(birthday_date, *args):
    
    if birthday_date:
        valid_birthday_patterns = {
        "hyphen" : r'\d{1,2}\-\d{1,2}\-\d{1,4}$',
        "forward slash" : r'\d{1,2}\/\d{1,2}\/\d{1,4}$',
        "period" : r'\d{1,4}\.\d{1,2}\.\d{1,4}$',
        }

        split_characters = {
        "hyphen" : '-',
        "forward slash" : '/',
        "period" : '.',
        }

        for date_format_identifier,v in valid_birthday_patterns.items():
            if re.match(v, birthday_date):
                break
            else:
                raise BirthdayDateOfInvalidFormat('Birthday date is in invalid format. Please try again.')
        
        birthday_date_split = birthday_date.split(split_characters[date_format_identifier])

        possible_day_month_values = ["01", '02', '03', '04', '05', '06', '07', '08', '09']

        day = birthday_date_split[0]
        if day in possible_day_month_values:
            day = day[1]
        month = birthday_date_split[1]
        if month in possible_day_month_values:
            month = month[1]
        year = birthday_date_split[2]

        if 1900 <= int(year) <= datetime.today().year:
            if (
                ((month in ['1', '3', '5', '7', '8', '10', '12']) and (int(day) in range(0, 32))) 
                or ((month in ['4', '6', '9', '11']) and (int(day) in range(0, 31)))
                or ((month == '2') and (int(day) in ['28', '28']))
                ):
                return year, month, day
            raise BirthdayDateOfInvalidFormat('Birthday date is in invalid format. Please try again.')
        raise BirthdayDateOfInvalidFormat('Birthday date is in invalid format. Please try again.') 
    return True


def display_contacts(contacts):
    table = PrettyTable()
    field_names = [column.upper() for column in TABLE_COLUMNS]
    field_names.insert(0, 'ID')
    table.field_names = field_names
    for contact in contacts:
            table.add_row(contact.value_id)
    print(table)

def show_input_tag(contact):
    if contact.notes._tags:
        print(f"{TextColor.MAGENTA}Current tags are: {TextColor.RESET}", end="")
        print(contact.notes.tags)
        print(f'{TextColor.YELLOW}\nWhat would you like to do with tags?{TextColor.RESET}\n1. Delete\n2. Add\n3. Write new\n4. Changed my mind\n')
        delete_add_new_tags = valid_choice_menu_edit_find('tags choice')

        if delete_add_new_tags == '1':
            contact.notes.tags = None
            print(f'{TextColor.GREEN}Tags have been deleted.{TextColor.RESET}')
            return
    
        if delete_add_new_tags == '3':
            new_tag = input(f"{TextColor.YELLOW}Please enter new tags(separated by comma): {TextColor.RESET}").lower()
            new_tag = new_tag.split(',')
            contact.notes.tags = new_tag
            print(f'{TextColor.GREEN}Tags have been readded.{TextColor.RESET}')
            return
        if delete_add_new_tags == '4':
            return
    
    added_tag = input(f"{TextColor.YELLOW}Please enter tags to add (separated by comma): {TextColor.RESET}").lower()
    added_tag = added_tag.split(',')
    contact.notes.add_tags(added_tag)
    print(f'{TextColor.GREEN}Tags have been added.{TextColor.RESET}')

def find_sort_contacts_by_tags(book):
    if book.tags_in_book():
        print(f"{TextColor.YELLOW}Would you like to find or sort contacts by tags?{TextColor.RESET}\n1. Find by tag\n2. Sort contacts by tags\n")
        find_or_sort = valid_choice_menu_edit_find('find')
        contacts_without_tags = []
        contacts_with_tags = []
        tags_list = set()
        found_contacts = []

        for contact in book:
            if contact.notes._tags:
                contacts_with_tags.append(contact)
                tags_list.update(contact.notes._tags)
            else:
                contacts_without_tags.append(contact)
        
        if find_or_sort == '2':
        
            for tag in tags_list:
                print(f"{TextColor.MAGENTA}Tag: {tag}{TextColor.RESET}")
                
                for contact in contacts_with_tags:
                    if tag in contact.notes.tags:
                        found_contacts.append(contact)
                display_contacts(found_contacts)
                
            if contacts_without_tags:
                print(f'{TextColor.MAGENTA}Contacts without tags:{TextColor.RESET}')
                display_contacts(contacts_without_tags)

        elif find_or_sort == '1':
            tag_input_to_find = input(f"{TextColor.YELLOW}Please enter a valid tag: {TextColor.RESET}")
            for contact in contacts_with_tags:
                if tag_input_to_find in contact.notes.tags:
                    found_contacts.append(contact)
            print(f"{TextColor.MAGENTA}Tag: {tag_input_to_find}{TextColor.RESET}")
            display_contacts(found_contacts)
    else:
        print(f"{TextColor.RED}No contact has tags.{TextColor.RESET}")

def load_data_from_file():

    current_directory = os.getcwd()
    files_and_directories = os.listdir(current_directory)


    file_with_data = [file.split('\\')[-1] for file in files_and_directories if os.path.isfile(file) and file.split('\\')[-1].split('.')[-1] == 'bin']

    with open(file_with_data[0], "rb") as fh:
        unpacked = pickle.load(fh)
        return unpacked