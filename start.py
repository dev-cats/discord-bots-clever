from datetime import datetime as time

with open('log.txt', 'x') as f:
    pass

def log(value, *args, sep=' ', end='\n'):
    s = time.now().strftime('[%H:%M:%S]')
    print(s, value, *args, sep=sep, end=end)
    print(s, value, *args, sep=sep, end=end, file=open('log.txt', 'w'))
    
while True:
    with open('bot.py') as f:
        exec(f.read().encode('cp1251').decode('utf-8'))
    log('Restarting bot...')
