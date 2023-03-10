from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

# bad_list = [
#     ('Rediska', 'R******'),
#     ('rediska', 'r******'),
#     ('fuck', 'f***')
# ]

#нежелательные слова, при расширении списка вынесем в отдельный файл
bad_list = ['fuck',
             'rediska',
             ]


@register.filter()
@stringfilter #чтобы не вызывать ошибки, приведем в строку
def censor(value, bad_words = bad_list):
    words = value.split()#разделим строку
    new_line=''

    for word in words:
        #проверяем, не входит ли слово в нежелательный список
        if word.lower() in bad_words in bad_words:
            new_line += word[0] #если да, первый символ оставляем
            for i in word[1:]:
                new_line += '*'#остальные заменяем на *
            new_line += ' '
        #здесь все тоже, но учитываем знаки пунктуации в переданной строке
        elif (word[:-1].lower()) in bad_words:
            new_line += word[0]
            for i in word[1:-1]:
                new_line += '*'
            new_line += (word[-1] + ' ')
        #склеиваем в строку обычне слова без запретов
        else:
            new_line += (word + ' ')

    return new_line.rstrip()

    #Вариант с хранением нежелательных слов в кортеже
    #гораздо короче код, но пока не нашел как разделять по регистрам,
    #кроме как в список кортежей вносить 2 пары значений для одного слова.
    # for vals in bad_words:
    #     old, new = vals
    #     value = value.replace(old, new)
    # return value