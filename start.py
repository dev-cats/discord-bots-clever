from datetime import datetime as time

#try:
#    with open('log.txt', 'x'):
#        pass
#except FileExistsError:
#    pass

def log(*a, sep=' ', end='\n'):
    '''Logs debug info.'''
    s = time.now().strftime('[%H:%M:%S]')
    print(s, *a, sep=sep, end=end)
    #with open('log.txt', 'w') as f:
    #    f.write(sep.join([s] + list(a)))
    #    f.write(end)

while True:
    with open('bot.py') as f:
        exec(f.read().encode('cp1251').decode('utf-8'))
    log('Restarting bot...')