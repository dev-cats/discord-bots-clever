import discord
import asyncio

from start import log
from const import *
from strings import strings

client = discord.Client()                              												# get client
functions = {}                                          											# define the functions dict

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
				await functions[content[0]].func(message, content[1:])  # call the function
			else:
				await client.send_message(message.channel, strings.func.unknown)
		else:
			await client.send_message(message.channel, strings.func.none)

class Command:
	def __init__(self, name, func, syntax=None, sdesc=strings.sdesc.none, desc=strings.desc.none):
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
		embed = discord.Embed(title=strings.func.help.title, color=0x008800)
		embed.set_author(name=strings.embed.author)
		embed.set_thumbnail(url=strings.embed.thumbnail)
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
			function = functions[arg]
			embed = discord.Embed(title=strings.func.help.specific.title + arg, color=0x008800)
			embed.set_author(name=strings.embed.author)
			embed.set_thumbnail(url=strings.embed.thumbnail)
			embed.add_field(name='`' + function.syntax + '`', value=function.desc, inline=True)
			await client.send_message(message.channel, embed=embed)
		else:
			log('Unknown command.')
			await client.send_message(message.channel, strings.func.help.specific.unknown % (prefixes[0], arg))
	else:
		log('Too many arguments!')
		await client.send_message(message.channel, strings.func.help.overflow)

async def restart(message, args):
	if len(args):
		await client.send_message(message.channel, strings.func.restart.overflow)
	else:
		if 'Dev' in [str(role) for role in message.author.roles]:
			await client.send_message(message.channel, strings.func.restart.success)
			client.close()
		else:
			await client.send_message(message.channel, strings.func.restart.failure)

async def kill(message, args):
	if len(args):
		await client.send_message(message.channel, strings.func.kill.overflow)
	else:
		if 'Host' in [str(role) for role in message.author.roles]:
			await client.send_message(message.channel, strings.func.kill.success)
			exit()
		else:
			await client.send_message(message.channel, strings.func.kill.failure)
# Functions end

# Commands go here
prefixes = ['!bot']
Command("help", help, syntax='help [команда]', sdesc='Этот список или помощь по команде.', desc='Показывает список всех команд или подробное описание указаной команды (как то, что вы сейчас читаете).')
Command("restart", restart, syntax='restart', sdesc='Перезапуск бота.', desc='Перезапускает бота. Доступно только `@Dev`.')
Command("kill", kill, syntax='kill', sdesc='Остановка бота.', desc='Останавливает бота. Доступно только `@Host`.')
# Commands end

client.run(token)