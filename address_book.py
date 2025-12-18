from collections import UserDict
from datetime import datetime, date, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if len(value) < 3:
            raise ValueError("Name is too short, need more than 2 symbols")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(date)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday: str):
        if self.birthday is not None:
            raise ValueError("Birthday already exists")
        self.birthday = Birthday(birthday)
        return self.birthday

    def add_phone(self, phone: str):
        if phone not in self.phones:
            self.phones.append(Phone(phone))
            return phone

    def remove_phone(self, phone: str):
        p = self.find_phone(phone)
        if p is None:
            return None

        self.phones.remove(p)
        return p

    def edit_phone(self, phone: str, new_phone: str):
        p = self.find_phone(phone)
        if p is None:
            raise ValueError(f"Old phone '{phone}' not found.")

        new_phone_obj = Phone(new_phone)
        p.value = new_phone_obj.value
        return p

    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        result = f"Contact name: {self.name.value}, Phones: {'; '.join(p.value for p in self.phones)}"

        if self.birthday:
            result += f", Birthday: {self.birthday.value}"

        return result


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record
        return record

    def find(self, name: Name):
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            return self.data.pop(name, None)

    def get_upcoming_birthdays(self, days=7):
     
        upcoming_birthdays = []
        today = date.today()

        for record in self.values():
            if record.birthday is None:
                continue 
             
            birthday_date = record.birthday.value

            birthday_this_year =  birthday_date.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_date.replace(year=today.year + 1)


            if 0 <= (birthday_this_year - today).days <= days:
           
               congratulation_date_str = self._adjust_for_weekend(birthday_this_year)

               upcoming_birthdays.append(
                {"name": record.name.value,   "birthday": congratulation_date_str.strftime("%Y.%m.%d")}
            )
        return upcoming_birthdays
    
    @staticmethod
    def _adjust_for_weekend(birthday_date):
        if birthday_date.weekday() == 5:
            return birthday_date + timedelta(days=2)
        if birthday_date.weekday() == 6:
            return birthday_date + timedelta(days=1)
        return birthday_date

    def __str__(self):
        result = ["AddressBook:"]
        for record in self.data.values():
            result.append(str(record))
        return "\n".join(result)




