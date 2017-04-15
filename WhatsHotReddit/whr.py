import praw

import six
import sys

from datetime import datetime

__version__ = 0.1

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


def main():
    print(r'''Welcome to

                /         __ ___   __             _
    |  ||_  _ |_  _  |__|/  \ |   |__)_ _| _|.|_   )
    |/\|| )(_||_ _)  |  |\__/ |   | \(-(_|(_|||_  .


    Get the hot topics on reddit, right on your terminal.

    '''.format(v=__version__))

    reddit = praw.Reddit('bot1')
    subreddit_name = ask("Enter subreddit name:",
                answer=str_compat)
    subreddit = reddit.subreddit(subreddit_name)
    count_to_fetch = ask('How many post would you want to see?', answer=int, default=5)
    if count_to_fetch > 10:
        print('Cannot fetch more than 10 posts.')
        sys.exit()
    identifiers = ask('Show Identifiers?', answer=bool, default=True)
    if identifiers:
        title = 'Title :: \n'
        body = 'Body :: \n'
        post_score = 'Score :: '
    else:
        title = ''
        body = ''
        post_score = ''
    for submission in subreddit.hot(limit=5):
        print('*'*20)
        print((u'{0}' + submission.title).format(title))
        print('-'*20)
        print((u'{0}' + submission.selftext).format(body))
        print('-'*20)
        print(('{0}' + str(submission.score)).format(post_score))

if __name__ == "__main__":
    main()

