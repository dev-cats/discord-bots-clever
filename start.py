from datetime import datetime as time

try:
    with open('log.txt', 'x'):
        pass
except FileExistsError:
    pass

def log(*args, **kwargs):
    '''Logs debug info.'''
    s = time.now().strftime('[%H:%M:%S]')
    print(s, *args, **kwargs)
    print(s, *args, **kwargs, file=open('log.txt', 'w'))

while True:
    with open('bot.py') as f:
        exec(f.read().encode('cp1251').decode('utf-8'))
    log('Restarting bot...')