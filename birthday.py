from datetime import datetime
from google.cloud import datastore


def clean(s):
    """Return a string w/ angle brackets, endlines, & tab characters removed."""

    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    s = s.replace('\n', ' ')
    s = s.replace('\t', ' ')
    s = s.strip()
    if len(s) > 100:
        s = s[:100]

    return s


def get_client():
    """Get the Client object for the datastore."""
    
    return datastore.Client()


def fetch_birthdays():
    """Fetch and return the birthday data from the datastore."""

    client = get_client()
    query = client.query(kind='birthday')
    
    return query.fetch()


class Birthday():
    """An object representing a single birthday."""

    def __init__(self, name, date, entity_id=None):
        """Initialize a birthday object with a given name and date."""

        self.name = name
        self.date = date
        self.entity_id = entity_id
        self.countdown = self.get_countdown()


    def get_formatted_date(self):
        """Return this birthdays's date as a 'Month DD YYYY' string."""

        return self.date.strftime('%b %d, %Y')


    def get_countdown(self):
        """Return the number of days between the the given date and today."""

        # Calculate begining of today, the birthday this year, and the birthday next year to use in calculation
        today = datetime.combine(datetime.today(), datetime.min.time())
        this_year = datetime(today.year, self.date.month, self.date.day)
        next_year = datetime(today.year+1, self.date.month, self.date.day)
    
        # Get the difference in days as an integer
        countdown = ((this_year if this_year > today else next_year) - today).days
        return countdown % 365

    def __str__(self):
        """Return a simple formatted string with the birthday contents."""

        return 'Name: %s Birthday:(%s) Countdown: [%s]' % (self.name, self.get_formatted_date(), str(self.get_countdown()))
    

    def __lt__(self, other):
        return self.countdown < other.countdown


    def __gt__(self, other):
        return self.countdown > other.countdown
    

    def __eq__(self, other):
        return self.countdown == other.countdown
    

    def __ne__(self, other):
        return self.countdown != other.countdown
    

    def __le__(self, other):
        return self.countdown <= other.countdown
    

    def __ge__(self, other):
        return self.countdown >= other.countdown


class BirthdayManager():
    """A class for managing Birthdays."""

    def __init__(self):
        """Initialize the BirhtdayManager with a new list of birthdays."""

        self.birthdays = []


    def add_birthday(self, entity, birthday):
        """Add a birthday to our birthdays list."""

        client = get_client()
        client.put(entity)

        self.birthdays.append(birthday)        
        self.birthdays.sort()


    def create_birthday(self, name, date):
        """Create a new birthday with a given date."""
        
        client = get_client()
        key = client.key('birthday')
        entity = datastore.Entity(key)
        entity.update(
            {
                'name': clean(name),
                'date': date,
            }
        )

        new_birthday = Birthday(clean(name), date, entity.id)

        self.add_birthday(entity, new_birthday)


    def get_birthdays_output(self):
        """Return the current birthday contents as a plain text string."""

        self.update_birthdays()

        return '\n'.join(str(birthday) for birthday in self.birthdays)


    def get_birthdays(self):
        """Return the current birthday contents as HTML."""

        self.update_birthdays()

        return self.birthdays


    def clear_birthdays(self):
        """Clear all birthdays in the database and on the page."""
        
        client = get_client()
        fetch = fetch_birthdays()

        for entity in fetch:
            key = client.key('birthday', entity.id)
            client.delete(key)
    
        self.birthdays.clear()


    def delete_birthday(self, id):
        """Delete a single birthday from the datastore update the list."""

        client = get_client()
        key = client.key('birthday', int(id))
        client.delete(key)

        self.update_birthdays()


    def update_birthdays(self):
        """Update the list of birthdays new Birthday objects based on the datastore."""

        fetch = fetch_birthdays()

        self.birthdays = [
            Birthday(entity['name'], datetime.fromtimestamp(entity['date'].timestamp()), entity.id)
            for entity in fetch
        ]
        self.birthdays.sort()
 