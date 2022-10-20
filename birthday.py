import datetime


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


class Birthday():
    """An object representing a single birthday."""

    def __init__(self, name, date):
        """Initialize a birthday for named user."""

        self.name = name
        self.date = date


    def get_formatted_date(self):
        """Return this messages's time as a 'YYYYMMDD' string."""

        return self.date.strftime('%Y%m%d')

    def get_countdown(self):
        return self.date - datetime.datetime.today()

    def to_html(self):
        """Convert this message to an HTML div."""
        
        # outputDiv = '<div class="Message">%s (%s): %s</div>'
        outputRow = '<tr>%s</tr>'
        outputTableElement = '<td class="%s">%s</td>'

        nameElement = outputTableElement % ('birthday-name', self.name)
        dateElement = outputTableElement % ('birthday-date', self.date)
        countdownElement = outputTableElement % ('birthday-countdown', self.get_countdown())

        return outputRow % (nameElement, dateElement, countdownElement)


    def __str__(self):
        """Return a simple formatted string with the message contents."""

        return 'Name: %s Birthday:(%s) Countdown: [%s]' % (self.name, self.get_formatted_date(), str(self.get_countdown()))
    

    def __lt__(self, other):
        return self.date < other.date


    def __gt__(self, other):
        return self.date > other.date
    

    def __eq__(self, other):
        return self.date == other.date
    

    def __ne__(self, other):
        return self.date != other.date
    

    def __le__(self, other):
        return self.date <= other.date
    

    def __ge__(self, other):
        return self.date >= other.date


class BirthdayManager():
    """A class for managing Birthdays."""

    def __init__(self):
        """Initialize the BirhtdayManager with a new list of birthdays."""

        self.birthdays = []


    def add_birthday(self, birthday):
        """Add a birthday to our birthdays list."""

        self.birthdays.append(birthday)        
        self.birthdays.sort()


    def create_birthday(self, name, date):
        """Create a new birthday with the current date."""

        self.add_birthday(Birthday(clean(name), date))


    def get_birthdays_output(self):
        """Return the current birthday contents as a plain text string."""

        result = ''
        for birthday in self.birthdays:
            result += str(birthday)
            result += '\n'
        return result


    def get_birthdays_html(self):
        """Return the current birthday contents as HTML."""

        result = ''
        for birthday in self.birthdays:
            result += birthday.to_html()
            result += '\n'
        return result


    def delete_birthday(self, time):
        # Implement Later -- TODO
        pass 


