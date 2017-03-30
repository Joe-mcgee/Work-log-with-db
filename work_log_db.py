import datetime
from peewee import *

MENU_OPTIONS = ('(A)dd Entry', '(S)earch Entries', '(D)isplay Entries', '(Q)uit')
MENU_CHOICES = ('A', 'S', 'D', 'Q')
VALIDATOR = ('Y', 'N') 
entry_counter = 0
SEARCH_OPTIONS = ('by (D)ate', 'by (T)ime Spent', 'by (E)xact Search', 'by (P)attern', 'by (N)ame')
SEARCH_CHOICES = ('D', 'T', 'E', 'P', 'N')

db = SqliteDatabase('worklog.db')

class Entry(Model):
    name = CharField(max_length=255)
    task_name = CharField(max_length=255)
    time = CharField()
    date = DateTimeField()
    note = CharField()
    
    class Meta:
        database = db

def print_menu():
    for option in MENU_OPTIONS:
        print('> {}'.format(option))
        
def menu_choice():
    while True:
        try:
            choice = input('What would you like to do?: ')
            choice.upper()
            
            if choice not in MENU_CHOICES:
                raise ValueError
        
        except (ValueError, TypeError):
            print('please select a valid option')
        
        else:
            break
    return choice

def menu(selection):
    
    if selection == 'A':
        return add_entry()
    
    if selection == 'S':
        return search_entries()
    
    if selection == 'D':
        return display_records()
    
    if selection == 'Q':
        return quit()
    
def display_entries(entries):
    for entry in entries:
        print(' Name: {}\n'.format(entry.name), 'Task Name: {}\n'.format(entry.task_name),
              'Note: {}\n'.format(entry.note), 'Time: {}\n'.format(entry.time),
              'Date: {}\n'.format(entry.date))
        print('')
        
def date_grab():
    while True:
        try:
            date = date_entry()
            date_validate(date)
            date= date_enterer(date)
            
        except ValueError:
            print('pleae enter a valid date.')
            
        else:
            return date

def search_date(date):
    entries = Entry.select().order_by(Entry.date.desc()).where(Entry.date.contains(date))
    return entries

def search_navigation():
    title = print('How would you like to search?')
    return title

def print_search_menu():
    for option in SEARCH_OPTIONS:
        print('> {}'.format(option))
        
def search_selection():
    choice = input('Please select search type: ')
    choice.upper()
    return choice

def search_validation(choice):
    try:
        if choice not in SEARCH_CHOICES:
            raise ValueError
    except (ValueError, TypeError):
        print("Your selection isn't a part of the menu")
            
    else:
        return choice

def search_time(time):
    entries = Entry.select().where(Entry.time.contains(time))
    return entries

def string_search():
    search = input('what would you like to search?')
    return search

def check_names(search):
    entry_name_match = Entry.select().where(Entry.name.contains(search))
    return entry_name_match
    
def check_task_name(search):
    entry_task_name = Entry.select().where(Entry.task_name.contains(search))
    return entry_task_name

def check_entry_time(search):
    entry_time = Entry.select().where(Entry.time.contains(search))
    return entry_time
    
def check_entry_date(search):
    entry_date = Entry.select().where(Entry.date.contains(search))
    return entry_date

def check_entry_note(search):
    entry_note = Entry.select().where(Entry.note.contains(search))
    return entry_note

def search_return_extender(entry_name, entry_task_name, entry_time, entry_date, entry_note):
    entries =[]
    args = [entry_name, entry_task_name, entry_time, entry_date, entry_note]
    for arg in args:
        entries.extend(arg)
    return entries

def search_return_filter(entries):
    clean_entries = []
    for entry in entries:
        if entry not in clean_entries:
            clean_entries.append(entry)
    return clean_entries
    
        
def string_search_return(search):   
    entry_name = check_names(search)
    entry_task_name = check_task_name(search)
    entry_time = check_entry_time(search)
    entry_date = check_entry_date(search)
    entry_note = check_entry_note(search)
    return entry_name, entry_task_name, entry_time, entry_date, entry_note
 

def search_entries():
    search_navigation()
    print_search_menu()
    while True:
        try:
            choice = search_selection()
            search_validation(choice)
        
        except (ValueError, TypeError):
            print('please select a valid menu option')
        
        else:
            break
                  
    if choice == 'D':
        date = date_grab()
        entries = search_date(date)
        display_entries(entries)
        
    if choice == 'T':
        time = time_entry()
        entries = search_time(time)
        display_entries(entries)
     
    if choice == 'E':
        search = string_search()
        entry_name, entry_task_name, entry_time, entry_date, entry_note = string_search_return(search)
        entries = search_return_extender(entry_name, entry_task_name, entry_time, entry_date, entry_note)
        clean_entries = search_return_filter(entries)
        display_entries(clean_entries)
        
       
                    
    if choice == 'P':
        entries = []
        clean_entries = []
        print('Please input a regular expression to search for')
        reg_ex = input('What is the patter your looking for?: ')   
        entry_name = Entry.select().where(Entry.name.regexp(reg_ex))
        entry_task_name = Entry.select().where(Entry.task_name.regexp(reg_ex))
        entry_time = Entry.select().where(Entry.time.regexp(reg_ex))
        entry_date = Entry.select().where(Entry.date.regexp(reg_ex))
        entry_note = Entry.select().where(Entry.note.regexp(reg_ex))
        
        entries.extend(entry_name)
        entries.extend(entry_task_name)
        entries.extend(entry_time)
        entries.extend(entry_date)
        entries.extend(entry_note)
        
        for entry in entries:
            if entry not in clean_entries:
                clean_entries.append(entry)
        
        for entry in clean_entries:
            print(' Name: {}\n'.format(entry.name), 'Task Name: {}\n'.format(entry.task_name),
                  'Note: {}\n'.format(entry.note), 'Time: {}\n'.format(entry.time),
                  'Date: {}\n'.format(entry.date))
            print('')
    
    if choice == 'N':
        name = input('What name are you Searching for?: ')
        entries = Entry.select().where(Entry.name.contains(name))
        for entry in entries:
            print(' Name: {}\n'.format(entry.name), 'Task Name: {}\n'.format(entry.task_name),
                  'Note: {}\n'.format(entry.note), 'Time: {}\n'.format(entry.time),
                  'Date: {}\n'.format(entry.date))
            print('')
        
    return navigation()

def validation(object):
    while True:
        try:
            validator = input("Is '{}' correct? (Y, N): ".format(object))
            validator.upper()
            if validator not in VALIDATOR:
                raise ValueError
            
        except (ValueError, TypeError):
            print('Please select Y or N')
            
        else:
            return validator
                
def name_entry():
    name = input('Workers name: ')
    return name
        
def task_entry():
    task_name = input('Task name: ')
    return task_name
           
def time_entry():
    while True:
            try:
                time = input('How long was spent on such task (minutes)?: ')
                if not int(time):
                    raise ValueError
                
            except ValueError:
                print('time must be a numerical value')
            
            else:
                return time
    
def is_note():
    while True:
        try:
            note_check = input('is there an additional note you would like to add? (Y,N): ')
            note_check.upper()
            if note_check not in VALIDATOR:
                raise ValueError
                    
        except (ValueError, TypeError):
            print('Please select Y or N')
            
        else:
            return note_check

def note_entry():
    note = input('Note Adder: ')
    return note

def date_check():
    while True:
        try:
            date_check = input('Was this work done Today? (Y/N)?:')
            date_check.upper()
            if date_check not in VALIDATOR:
                raise ValueError
            
        except (TypeError, ValueError):
            print('please select a valid date')
        
        else:
            return date_check

def date_entry():
    print('When was this Work Completed?')
    date_str = input('type in as YYYY/MM/DD: ')
    return date_str

def date_validate(date_str):
    try:
        datetime.datetime.strptime(date_str, '%Y/%m/%d')
    except ValueError:
        print("this date doesn't exist")
    else:
        return date_str
               
def date_enterer(date_str):
    try:
        date_list = date_str.split('/')
        year= int(date_list[0])
        month = int(date_list[1])
        day = int(date_list[2])                        
        str_date= '{}-{}-{}'.format(year, month, day)
        my_date = datetime.date(*[int(i) for i in str_date.split('-')])
        date = my_date.strftime('%Y/%m/%d')
        
    except IndexError:
        print('not an indexable date')
        
    else:
        return date
     
def add_entry():
    print('Entry logger:')
    while True:
        name = name_entry()
        validator = validation(name)
        if validator == 'Y':
            break
        else:
            continue
   
    while True:
        task_name = task_entry()
        validator = validation(task_name)
        if validator == 'Y':
            break
        else:
            continue
           
    while True:
        time = time_entry()
        validator = validation(time)
        if validator == 'Y':
            break
        else:
            continue
    
    note_check = is_note()
    if note_check == 'Y':
        while True:
            note = note_entry()
            validator = validation(note)
            if validator == 'Y':
                break
            else:
                continue
                
    if note_check == 'N':
        note = 'None'
        
    is_today = date_check()
    if is_today == 'Y':
        date = datetime.datetime.today().strftime("%Y/%m/%d")
                
    if is_today == 'N':
        while True:
            try:
                date = date_entry()
                date_validate(date)
                date= date_enterer(date)
                
            except ValueError:
                print('pleae enter a valid date.')
                
            
            else:
                break
    
    return Entry.create(name=name, task_name=task_name, time=time, date=date, note=note), navigation()
        
def display_records():
    entries = Entry.select()
    
    for entry in entries:
        print(' Name: {}\n'.format(entry.name), 'Task Name: {}\n'.format(entry.task_name),
                          'Note: {}\n'.format(entry.note), 'Time: {}\n'.format(entry.time),
                          'Date: {}\n'.format(entry.date))
        print('')
    navigation()
            
def navigation():
    print('What would you like to do?')
    print_menu()
    selection = menu_choice()
    menu(selection)
        
if __name__ == '__main__':
    db.connect()
    db.create_tables([Entry], safe=True)
    navigation()
    