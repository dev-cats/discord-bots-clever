from const import *
import discord
import asyncio
from start import log

client = discord.Client()                              												# get client
functions = {}                                          											# define the functions dict
strings = {
    'desc.none':'No description for this command provided.',
    'embed.author':'Bot',
    'embed.thumbnail':'https://discordapp.com/assets/2c21aeda16de354ba5334551a883b481.png',
    'func.help.overflow':'Too many arguments!',
    'func.help.title':'Bot Help',
    'func.help.specific.title':'Help for %s',
    'func.help.specific.unknown':'`%s %s` is not a function!',
    'func.kill.failure':'You don\'t have permissions to do this.',
    'func.kill.overflow':'Too many arguments!',
    'func.kill.success':'The bot was stopped.',
    'func.none':'Please, specify a function.',
    'func.unknown':'This is not a function',
    'sdesc.none':'No description.'
}

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
			if content[0] in functions.keys():
				await functions[content[0]].func(message, content[2:] if len(content) > 2 else [])  # call the function
			else:
				await client.send_message(message.channel, strings['func.unknown'])
		else:
			await client.send_message(message.channel, strings['func.none'])

class Command:
	def __init__(self, name, func, syntax=None, sdesc=strings['sdesc.none'], desc=strings['desc.none']):
		if name in functions.keys():																# check for repeating 
			raise KeyError()
		self.name = name
		self.func = func
		if syntax is None:
			syntax = name
		self.syntax = prefixes[0] + ' ' + name
		self.sdesc = sdesc
		self.desc = desc
		functions[name] = self

# Functions go here
async def help(message, args):
	if len(args) == 0:
		log('Listing commands.')
		embed = discord.Embed(title=strings['func.help.title'], color=0x008800)
		embed.set_author(name=strings['embed.author'])
		embed.set_thumbnail(url=strings['embed.thumbnail'])
		for key in functions:
			embed.add_field(name='`' + functions[key].syntax + '`', value=functions[key].sdesc, inline=True)
		await client.send_message(message.channel, embed=embed)
	elif len(args) == 1 or len(args) == 2 and args[0] in prefixes:
		if len(args) == 2:
			arg = args[1]
		else:
			arg = args[0]
		log('Getting help for', arg + '.')
		if arg in functions.keys():
			function = function[arg]
			embed = discord.Embed(title=strings['func.help.specific.title'] + arg, color=0x008800)
			embed.set_author(name=strings['embed.author'])
			embed.set_thumbnail(url=strings['embed.thumbnail'])
			embed.add_field(name='`' + function.syntax + '`', value=function.desc, inline=True)
			await client.send_message(message.channel, embed=embed)
		else:
			log('Unknown command.')
			await client.send_message(message.channel, strings['func.help.specific.unknown'] % (prefixes[0], arg))
	else:
		log('Too many arguments!')
		await client.send_message(message.channel, strings['func.help.overflow'])

async def kill(message, args):
	if len(args) > 0:
		await client.send_message(message.channel, strings['func.kill.overflow'])
	else:
		if 'Lord' in [str(role) for role in message.author.roles]:
			await client.send_message(message.channel, strings['func.kill.success'])
			client.close()
		else:
			await client.send_message(message.channel, strings['func.kill.failure'])
# Functions end

# Strings go here
strings = {
    'desc': {
        'none': 'Ну, я не знаю, она что-то делает, но что... мне не сказали. Попробуй и узнаешь! :wink:'
    },
    'embed':{
        'author': 'Minecraft Бот',
        'thumbnail': 'https://d1u5p3l4wpay3k.cloudfront.net/minecraft_ru_gamepedia/b/bc/Wiki.png?version=26fd08a888d0d1a33fb2808ebc8678e9'
    },
    'func':{
        'help':{
            'overflow': 'Я твоя не понимать, ты говорить коротко!',
            'title': 'Помощь по боту',
            'specific.title': 'Помощь по %s',
            'specific.unknown': 'Я не знаю, что такое `%s %s`!'
        },
        'kill':{
            'failure': 'Да кто ты такой?',
            'overflow': 'Ты чего, совсем обалдел? Не только пытаешься меня убить, но и грузишь всем этим своим бредом?',
            'success': 'Я вернусь! :thumbsup:'
        },
        'none': 'Что?',
        'unknown': 'Я не понимаю, чего ты от меня хочешь!'        
    },
    'sdesc':{
        'none': 'Не знаю...'
    }
}
# Strings end

# Commands go here
prefixes = ['!bot']
Command("help", help, syntax='help [команда]', sdesc='Этот список или помощь по команде.', desc='Показывает список всех команд или подробное описание указаной команды (как то, что вы сейчас читаете).')
Command("kill", kill, syntax='kill', sdesc='Остановить бота.', desc='Останавливает бота. Доступно только @Owner.')
# Commands end

client.run(token)