from datetime import datetime as time
print_stdout = print
def print(*args, **kwargs):
    s = time.now().strftime('[%H:%M:%S] ') + kwargs['sep'].join(args)
    print_stdout(s, kwargs['end'])
while True:
    with open('bot.py') as f:
        exec(f.read())
    print('Restarting bot...')
