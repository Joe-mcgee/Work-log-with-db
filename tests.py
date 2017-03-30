import unittest
import unittest.mock as mock
import work_log_db
from work_log_db import SEARCH_CHOICES

import datetime

MOCKENTRY = {
    "name": "Joe Mcgee",
    "task_name": "Dishes",
    "time": "12",
    "note": "washed and dried",
    "date": "2017/03/29"
}

MOCKVALIDATOR = {
    "validator": "Y",
    'object_test': 'Apple'
    }

MOCKCHOICE = {
    "choice_A": "A",
    "choice_S": 'S',
    "choice_D": 'D',
    "choice_Q": 'Q'
    }

MOCKSEARCH = {
    'search': 'Joe Mcgee'
    }

MOCKTITLE = {
    'title': 'How would you like to search?'}

ENTRIES = [MOCKENTRY, MOCKENTRY]
class DBTests(unittest.TestCase):
    
    def set_up(self):
        work_log_db.db.connect()
        work_log_db.db.create_tables([work_log_db.Entry], safe=True)
        
    def test_table(self):
        assert work_log_db.Entry.table_exists()
        

class MenuTests(unittest.TestCase):
    
    def test_menu(self):
        pass
    
    @staticmethod
    def test_menu_choice():  
        with mock.patch('builtins.input', return_value=MOCKCHOICE["choice_A"]):
            assert work_log_db.menu_choice() == MOCKCHOICE['choice_A']      
   
            
class ValidationTest(unittest.TestCase):
        
    def test_validator(self):
        with mock.patch('builtins.input', return_value=MOCKVALIDATOR["validator"]):
            assert work_log_db.validation(object) == MOCKVALIDATOR['validator']
            

     
    def test_date_validate(self):
        with mock.patch('builtins.input', return_value=MOCKENTRY['date']):
            assert work_log_db.date_validate(MOCKENTRY['date']) == MOCKENTRY['date'] 
    @unittest.expectedFailure
    def test_date_validate_fail(self):
        with self.assertRaises(ValueError):
            work_log_db.date_validate("alkdjsfadlf")
    
    @staticmethod
    def test_is_note():
        with mock.patch('builtins.input', return_value=MOCKVALIDATOR['validator']):
            assert work_log_db.is_note() == MOCKVALIDATOR['validator']
    
    @staticmethod
    def test_date_check():
        with mock.patch('builtins.input', return_value=MOCKVALIDATOR['validator']):
            assert work_log_db.date_check() == MOCKVALIDATOR['validator']   
            
    def test_search_validation(self):
        self.assertEqual(work_log_db.search_validation(choice='D'), 'D')
    
    @unittest.expectedFailure
    def test_bad_validation(self):
        with self.assertRaises(ValueError):
            work_log_db.search_validation(choice='1')
            
            
class AddEntryTests(unittest.TestCase):
    @staticmethod
    def mock_entry():
        work_log_db.Entry.create(
            name=MOCKENTRY["name"],
            task_name=MOCKENTRY["task_name"],
            time=MOCKENTRY["time"],
            note=MOCKENTRY["note"],
            date=MOCKENTRY["date"]
        )
        
    
    def test_name(self):
        with mock.patch('builtins.input', return_value=MOCKENTRY["name"]):
            assert work_log_db.name_entry() == MOCKENTRY["name"]
    
    def test_task_name(self):
        with mock.patch('builtins.input', return_value=MOCKENTRY["task_name"]):
            assert work_log_db.task_entry() == MOCKENTRY["task_name"]
            
    def test_time_entry(self):
        with mock.patch('builtins.input', return_value=MOCKENTRY["time"]):
            assert work_log_db.time_entry() == MOCKENTRY["time"]
            
               
    def test_note_entry(self):
        with mock.patch('builtins.input', return_value=MOCKENTRY["note"]):
            assert work_log_db.note_entry() == MOCKENTRY["note"]
    
    def test_date_entry(self):
        with mock.patch('builtins.input', return_value=MOCKENTRY["date"]):
            assert work_log_db.date_entry() == MOCKENTRY["date"]
            
    def test_date_enterer(self):
        with mock.patch('builtins.input', return_value=MOCKENTRY["date"],):
            assert work_log_db.date_enterer(MOCKENTRY['date']) == MOCKENTRY['date']


class SearchDBTests(unittest.TestCase):
    @staticmethod
    def mock_entry():
        work_log_db.Entry.create(
            name=MOCKENTRY["name"],
            task_name=MOCKENTRY["task_name"],
            time=MOCKENTRY["time"],
            note=MOCKENTRY["note"],
            date=MOCKENTRY["date"]
        )
    
    @staticmethod   
    def test_date_grab():
        with mock.patch('builtins.input', return_value=MOCKENTRY["date"]):
            assert work_log_db.date_grab()== MOCKENTRY["date"]
    @staticmethod    
    def test_search_date():
        with mock.patch('builtins.input', return_value= MOCKENTRY):
            assert work_log_db.search_date(MOCKENTRY['date']) == MOCKENTRY
    @staticmethod   
    def test_search_time():
        with mock.patch('builtins.input', return_value= MOCKENTRY):
            assert work_log_db.search_time(MOCKENTRY['time']) == MOCKENTRY
    @staticmethod   
    def test_string_search():
        with mock.patch('builtins.input', return_value= MOCKSEARCH['search']):
            assert work_log_db.string_search() == MOCKSEARCH['search']
    
    def test_check_names(self):
        with mock.patch('builtins.input', return_value = MOCKENTRY):
            assert work_log_db.check_names(MOCKSEARCH['search']) == MOCKENTRY
     
    def test_check_task_name(self):
        with mock.patch('builtins.input', return_value = MOCKENTRY):
            assert work_log_db.check_task_name(MOCKSEARCH['search']) == MOCKENTRY
            
    def test_check_entry_time(self):
        with mock.patch('builtins.input', return_value = MOCKENTRY):
            assert work_log_db.check_entry_time(MOCKSEARCH['search']) == MOCKENTRY
            
    def test_check_entry_date(self):
        with mock.patch('builtins.input', return_value = MOCKENTRY):
            assert work_log_db.check_entry_date(MOCKSEARCH['search']) == MOCKENTRY
            
    def test_check_entry_note(self):
        with mock.patch('builtins.input', return_value = MOCKENTRY):
            assert work_log_db.check_entry_note(MOCKSEARCH['search']) == MOCKENTRY
    
    def test_search_selection(self):
        with mock.patch('builtins.input', return_value = MOCKCHOICE['choice_A']):
            assert work_log_db.search_selection() == MOCKCHOICE['choice_A']
            

class SearchFilterTests(unittest.TestCase):
    def test_search_return_extender(self):
        self.assertEqual(work_log_db.search_return_extender(entry_name=['joe'],
                                                             entry_task_name=['chill'],
                                                              entry_time=['15'],
                                                               entry_date=['2017/03/22'],
                                                                entry_note=['nay']),
                          ['joe', 'chill', '15', '2017/03/22', 'nay',])
     
    def test_search_return_filter(self):
        self.assertEqual(work_log_db.search_return_filter(entries=ENTRIES), [MOCKENTRY]) 
         
                                            
if __name__ == '__main__':
    
    unittest.main()