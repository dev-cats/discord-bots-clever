from datetime import datetime as time

def log(*args, **kwargs):
    s = time.now().strftime('[%H:%M:%S] ')
    print(s, *args, **kwargs)

while True:
    with open('bot.py') as f:
        exec(f.read().encode('cp1251').decode('utf-8'))
    log('Restarting bot...')
