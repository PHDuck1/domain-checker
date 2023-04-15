from checker import DomainChecker

URL = 'https://btc.us/'
INPUT_FILENAME = 'text.txt'

if __name__ == '__main__':
    dc = DomainChecker(url=URL)
    dc.run(INPUT_FILENAME, free_text='Available for')
