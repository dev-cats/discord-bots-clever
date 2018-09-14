import discord
import asyncio

from start import log
from const import *
from strings import strings

client = discord.Client()                              												# get client

def start(t):
    client.run(t)

async def send(*args, **kwargs):
    await client.send_message(*args, **kwargs)

@client.event
async def on_ready():                                   											# some logging
    log('All set and ready!')
    log('Bot logged in as', client.user.name, 'with id', client.user.id)
    log('-----')

@client.event
async def on_message(message):
    log(message.server, '/', message.channel, '/', message.author, 'wrote', message.content)
    if any([message.content.startswith(i) for i in prefixes]):
        text = message.content.lower()                      											# parse message
        content = text.split()[1:]
        await asyncio.sleep(0.2)                            										# make it feel natural
        await client.send_typing(message.channel)
        await asyncio.sleep(1)            											# more logging
        if len(content):
            if content[0] in Command.functions.keys():
                await Command.functions[content[0]].func(message, content[1:])  # call the function
            else:
                await send(message.channel, strings.func.unknown)
        else:
            await send(message.channel, strings.func.none)

class Command:
    '''Defines a bot command.'''
    functions = {}                                          											# define the functions dict
    def __init__(self, name, func, syntax, sdesc, desc):
        if name in self.functions.keys():																# check for repeating 
            raise KeyError()
        self.name = name
        self.func = func
        self.syntax = prefixes[0] + ' ' + syntax
        self.sdesc = sdesc
        self.desc = desc
        self.functions[name] = self

def command(func, name=None, syntax=None, sdesc=strings.sdesc.none, desc=strings.desc.none):
    if name is None:
        name = func.__name__
    if syntax is None:
        syntax = name    
    def wrapper(*a, **kwa):
        func(*a, **kwa)
    Command(name, wrapper, syntax, sdesc, desc)
    return func

# Functions go here
@command(syntax='help [команда]', sdesc='Этот список или помощь по команде.', desc='Показывает список всех команд или подробное описание указаной команды (как то, что вы сейчас читаете).')
async def help(message, args):
    '''Prints help on all the commands.'''
    if len(args) == 0:
        log('Listing commands.')
        embed = discord.Embed(title=strings.func.help.title, color=0x008800)
        embed.set_author(name=strings.embed.author)
        embed.set_thumbnail(url=strings.embed.thumbnail)
        for key in Command.functions:
            embed.add_field(name='`' + Command.functions[key].syntax + '`', value=Command.functions[key].sdesc, inline=True)
        await send(message.channel, embed=embed)
    elif len(args) == 1 or len(args) == 2 and args[0] in prefixes:
        if len(args) == 2:
            arg = args[1]
        else:
            arg = args[0]
        log('Getting help for', arg + '.')
        if arg in Command.functions.keys():
            function = Command.functions[arg]
            embed = discord.Embed(title=strings.func.help.specific.title + arg, color=0x008800)
            embed.set_author(name=strings.embed.author)
            embed.set_thumbnail(url=strings.embed.thumbnail)
            embed.add_field(name='`' + function.syntax + '`', value=function.desc, inline=True)
            await send(message.channel, embed=embed)
        else:
            log('Unknown command.')
            await send(message.channel, strings.func.help.specific.unknown % (prefixes[0], arg))
    else:
        log('Too many arguments!')
        await send(message.channel, strings.func.help.overflow)

@command(syntax='restart', sdesc='Перезапуск бота.', desc='Перезапускает бота. Доступно только `@Dev`.')
async def restart(message, args):
    '''Restarts the bot.'''
    if len(args):
        await send(message.channel, strings.func.restart.overflow)
    else:
        if 'Dev' in [str(role) for role in message.author.roles]:
            await send(message.channel, strings.func.restart.success)
            client.close()
        else:
            await send(message.channel, strings.func.restart.failure)

@command(sdesc='Остановка бота.', desc='Останавливает бота. Доступно только `@Host`.')
async def kill(message, args):
    '''Stops the bot.'''
    if len(args):
        await send(message.channel, strings.func.kill.overflow)
    else:
        if 'Host' in [str(role) for role in message.author.roles]:
            await send(message.channel, strings.func.kill.success)
            exit()
        else:
            await send(message.channel, strings.func.kill.failure)
# Functions end

# Commands go here
prefixes = ['!bot']
#start(token)