from collections import UserDict
import re
from datetime import datetime as dtdt
from abc import ABC, abstractmethod

class AbstractBot(ABC):
    @abstractmethod
    def message(self, message):
        pass

class MessageBot(AbstractBot):
    def message(self, message):
        print(message)

class Field:                                                                                                    
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):                                                                                     
    def __init__(self, value):
        self.value = value


class Phone(Field):                                                                                     

    def __init__(self, value):
       self.value = value

    @property
    def value(self):
        return self._value

    @value.setter                                                                                             
    def value(self, new_value):
        if re.fullmatch(r'\d{10}', new_value):
            self._value = new_value
        else:
            raise ValueError(f"Phone number {new_value} should consist of 10 digits")


class Birthday(Field):
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter                                                                                             
    def value(self, new_value):
        if re.fullmatch(r'(\d{2}\.){2}\d{4}', new_value):
            self._value = dtdt.strptime(new_value, "%d.%m.%Y").date()
        else:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:                                                                                          
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):                                                                                         
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

    def add_birthday(self, birthday:str):                                                                           
        if not self.birthday:
            self.birthday = Birthday(birthday)
        else: raise ValueError(f"Contact {self.name} has already added birthday {self.birthday}")
        
    def find_phone(self, phone: str): 
        for existing_phone in self.phones:
            if phone == existing_phone.value:
                return existing_phone
        return None
        
    def add_phone(self, phone:str):                                                                           
        if not self.find_phone(phone):
            self.phones.append(Phone(phone))
        else: raise ValueError(f"Contact {self.name} already has phone number {phone}")
            
    def remove_phone(self, phone:str):  
        phone_for_remove = self.find_phone(phone)                                                                              
        if phone_for_remove:
            self.phones.remove(phone_for_remove)
        else: raise ValueError(f"Contact {self.name} has no phone number: {phone}")

    def edit_phone(self, old:str, new:str):
        phone_for_edit = self.find_phone(old)     
        if phone_for_edit:
            phone_for_edit.value = new
        else: raise ValueError(f"Contact {self.name} has no phone number: {old}")


class AddressBook(UserDict):

    def add_record(self, record:Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        for key in self.data.keys():
            if key == name:
                return self.data[key]

    def delete(self, name: str):
        for key in self.data.keys():
            if key == name:
                del self.data[key]
                break
    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())