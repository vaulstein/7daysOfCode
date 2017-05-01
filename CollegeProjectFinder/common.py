import datetime
import sys

import pytz

try:
    import tzlocal

    _DEFAULT_TIMEZONE = tzlocal.get_localzone().zone
except:
    _DEFAULT_TIMEZONE = 'Asia/Calcutta'

import six

__version__ = "1.0.dev0"

TWITTER_API_URL = 'https://api.twitter.com/1.1'

# url for list of valid timezones
_TZ_URL = 'http://en.wikipedia.org/wiki/List_of_tz_database_time_zones'

CONF = {
    'consumer_key': '',
    'consumer_secret': '',
    'api_key': '',
    'api_secret': '',
    'data_to_fetch': 1,
    'query': '',
    'geocode': '',
    'lang': '',
    'result_type': 'popular',
    'count': 100,
    'until': None,
    'since_id': None,
    'type_of_follow': '1'
}

RESULT_MAP = {
    '1': 'popular',
    '2': 'recent',
    '3': 'mixed'
}


def decoding_strings(f):
    def wrapper(*args, **kwargs):
        out = f(*args, **kwargs)
        if isinstance(out, six.string_types) and not six.PY3:
            # todo: make encoding configurable?
            if six.PY3:
                return out
            else:
                return out.decode(sys.stdin.encoding)
        return out

    return wrapper


def _input_compat(prompt):
    if six.PY3:
        r = input(prompt)
    else:
        r = raw_input(prompt)
    return r


if six.PY3:
    str_compat = str
else:
    str_compat = unicode

dateObject = 'YYYY-MM-DD'


@decoding_strings
def ask(question, answer=str_compat, default=None, l=None, options=None):
    if answer == str_compat:
        r = ''
        while True:
            if default:
                r = _input_compat('> {0} [{1}] '.format(question, default))
            else:
                r = _input_compat('> {0} '.format(question, default))

            r = r.strip()

            if len(r) <= 0:
                if default:
                    r = default
                    break
                else:
                    print('You must enter something')
            else:
                if l and len(r) != l:
                    print('You must enter a {0} letters long string'.format(l))
                else:
                    break

        return r

    elif answer == bool:
        r = None
        while True:
            if default is True:
                r = _input_compat('> {0} (Y/n) '.format(question))
            elif default is False:
                r = _input_compat('> {0} (y/N) '.format(question))
            else:
                r = _input_compat('> {0} (y/n) '.format(question))

            r = r.strip().lower()

            if r in ('y', 'yes'):
                r = True
                break
            elif r in ('n', 'no'):
                r = False
                break
            elif not r:
                r = default
                break
            else:
                print("You must answer 'yes' or 'no'")
        return r
    elif answer == int:
        r = None
        while True:
            if default:
                r = _input_compat('> {0} [{1}] '.format(question, default))
            else:
                r = _input_compat('> {0} '.format(question))

            r = r.strip()

            if not r:
                r = default
                break

            try:
                r = int(r)
                break
            except:
                print('You must enter an integer')
        return r
    elif answer == list:
        # For checking multiple options
        r = None
        while True:
            if default:
                r = _input_compat('> {0} [{1}] '.format(question, default))
            else:
                r = _input_compat('> {0} '.format(question))

            r = r.strip()

            if not r:
                r = default
                break

            try:
                if int(r) in range(1, len(options) + 1):
                    break
                else:
                    print('Please select valid option: ' + ' or '.join('{}'.format(s) for _, s in enumerate(options)))
            except:
                print('Please select valid option: ' + ' or '.join('{}'.format(s) for _, s in enumerate(options)))
        return r
    if answer == dateObject:
        r = ''
        while True:
            if default:
                r = _input_compat('> {0} [{1}] '.format(question, default))
            else:
                r = _input_compat('> {0} '.format(question, default))

            r = r.strip()

            if not r:
                r = default
                break

            try:
                datetime.datetime.strptime(r, '%Y-%m-%d')
                break
            except ValueError:
                print("Incorrect data format, should be YYYY-MM-DD")

        return r

    else:
        raise NotImplemented(
            'Argument `answer` must be str_compat, bool, or integer')


def ask_timezone(question, default, tzurl):
    """Prompt for time zone and validate input"""
    lower_tz = [tz.lower() for tz in pytz.all_timezones]
    while True:
        r = ask(question, str_compat, default)
        r = r.strip().replace(' ', '_').lower()
        if r in lower_tz:
            r = pytz.all_timezones[lower_tz.index(r)]
            break
        else:
            print('Please enter a valid time zone:\n'
                  ' (check [{0}])'.format(tzurl))
    return r


def start():
    print(r'''Welcome to College Project Finder v{v}.

       _ \    _ \    _ \       |  ____|   ___| __ __|      ____| _ _|   \  |  __ \   ____|   _ \
      |   |  |   |  |   |      |  __|    |        |        |       |     \ |  |   |  __|    |   |
      ___/   __ <   |   |  \   |  |      |        |        __|     |   |\  |  |   |  |      __ <
     _|     _| \_\ \___/  \___/  _____| \____|   _|       _|     ___| _| \_| ____/  _____| _| \_\



    This script will help you find the coolest trending Open source projects that you can use as a project in college.

    Please answer the following questions so this script can generate your
    required output.

        '''.format(v=__version__))
    
