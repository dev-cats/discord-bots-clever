from datetime import datetime as time

def log(value, *args, sep=' ', end='\n'):
    s = time.now().strftime('[%H:%M:%S]')
    print(s, value, *args, sep=sep, end=end, file=open('log.txt', 'w'))
    print(s, value, *args, sep=sep, end=end)
    
while True:
    with open('bot.py') as f:
        exec(f.read().encode('cp1251').decode('utf-8'))
    log('Restarting bot...')
