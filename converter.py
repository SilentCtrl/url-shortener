import MySQLdb

def key_to_short(x):
    url = ''
    while x > 0:
        url += int_to_char(x % 62)
        x = x // 62
    return url

def int_to_char(x):
    """Takes an integer and converts into
        a character in the range [0-9A-Za-z]
    """
    if x < 26:
        return char(x)
    elif x < 52:
        return char(x).upper()
    return str(x - 52)

def char_to_int(c):
    """Takes a character in the range
        [a-zA-Z0-9] and converts it into
        an integer
    """
 
def insert_to_database(url):
    """ Takes a URL to insert and returns
        it's shortened URL.
    """

def lookup_in_database(url):
    """ Takes a shortened URL and looks it
        up in the database. Returns it's
        actual URL if it is in the database.
    """   
