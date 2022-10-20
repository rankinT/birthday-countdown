# THIS PAGE DEFINES A BASIC BIRTHDAY OBJECT TO BE USED IN CLOUD DATASTORE
month = None
day = None
year = None

def __init__(self, month, day, year):
    self.month = month
    self.day = day
    self.year = year

# TO STRING
def __str__(self):
    return self.month + "/" +  self.day + "/" + self.year

# RETURNS MONTH, DAY, YEAR
def get_data(self):
    return self.month, self.day, self.year

# ACCESSORS
def get_month(self):
    return self.month

def get_day(self):
    return self.day

def get_year(self):
    return self.year


def main():
    pass

if __name__ == '__main__':
    main()