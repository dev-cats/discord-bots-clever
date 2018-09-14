class TextNode:
    '''Creates an instance of TextNode from a multi-level dictionary.'''
    def __init__(self, d):
        for i in d:
            if type(d[i]) == dict:
                code = 'self.' + i.replace(' ', '_') + ' = ' + 'TextNode(' + str(d[i]) + ')'
            else:
                code = 'self.' + i.replace(' ', '_') + ' = ' + 'r"' + d[i] + '"'
            exec(code)

strings = TextNode({
    'desc': {
        'none': 'Ну, я не знаю, она что-то делает, но что... мне не сказали. Попробуй и узнаешь! :wink:'
    },
    'embed':{
        'author': 'Minecraft Бот',
        'thumbnail': 'https://d1u5p3l4wpay3k.cloudfront.net/minecraft_ru_gamepedia/b/bc/Wiki.png?version=26fd08a888d0d1a33fb2808ebc8678e9'
    },
    'func':{
        'help':{
            'overflow': 'Моя твоя не понимать, ты не говорить коротко!',
            'title': 'Помощь по боту',
            'specific':{
                'title': 'Помощь по ',
                'unknown': 'Я не знаю, что такое `%s %s`!'
            }
        },
        'kill':{
            'failure': 'Да кто ты такой?',
            'overflow': 'Ты чего, совсем обалдел? Не только пытаешься меня убить, но и грузишь всем этим своим бредом?',
            'success': 'Я вернусь! :thumbsup:'
        },
        'restart':{
            'failure': 'Да кто ты такой?',
            'overflow': 'Ты чего, совсем обалдел? Не только пытаешься меня перезапустить, но и грузишь всем этим своим бредом?',
            'success': 'Перезагрузка... :hourglass_flowing_sand:'
        },
        'none': 'Что?',
        'unknown': 'Я не понимаю, чего ты от меня хочешь!'        
    },
    'sdesc':{
        'none': 'Не знаю...'
    }
})