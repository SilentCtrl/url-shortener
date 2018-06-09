import MySQLdb

digit_offset = 48
upper_offset = 55
lower_offset = 61

def key_to_short(x):
    """Converts the integer key to a short url
    """
    url = ''
    while x > 0:
        url += int_to_char(x % 62)
        x = x // 62
    return url

def short_to_key(s):
    power = 0
    sum = 0
    for c in s[::-1]:
        sum += char_to_int(c) * (62 ** power)
        power += 1
    return sum

def int_to_char(x):
    """Takes an integer and converts it into
        a character in the range [0-9A-Za-z]
    """
    if x < 10:
        return chr(x + digit_offset)
    elif x < 36:
        return chr(x + upper_offset)
    elif x < 62:
        return chr(x + lower_offset)
    raise ValueError("%d is not in the modspace of 62" % x)

def char_to_int(c):
    """Takes a character in the range
        [0-9A-Za-z] and converts it into
        an integer
    """
    if '0' <= c <= '9':
        return ord(c) - digit_offset
    elif 'A' <= c <= 'Z':
        return ord(c) - upper_offset
    elif 'a' <= c <= 'z':
        return ord(c) - lower_offset
    raise ValueError("%s is an invalid character" % c)
 
def insert_to_database(url):
    """ Takes a URL to insert and returns
        it's shortened URL.
    """


def lookup_in_database(url):
    """ Takes a shortened URL and looks it
        up in the database. Returns it's
        actual URL if it is in the database.
    """


