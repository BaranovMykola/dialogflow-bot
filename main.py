# declaration-ocr-66601081fd69.json
import os
import Bot
import random
import string
import pyswip as ps

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./food-en-48f9e47f143e.json"

def check_dict(dict):
    if 'given-name' in dict.keys() and 'foods' in dict.keys():
        write_to_prolog(dict)


def write_to_prolog(dict):
    str = 'order({0},{1}).'.format(dict['given-name'].lower(), dict['foods'].lower())

    with open('prolog.pl', 'r') as pl:
        lines = [x.strip() for x in pl.readlines()]

    with open('prolog.pl', 'a+') as pl:
        # lines = [x.strip() for x in pl.readlines()]
        if str not in lines:
            pl.write('\n'+str)


print('Say \'Hi\'')
b = Bot.Bot('food-en', 'en')

while True:
    str = input('>>> ')


    res, i = b.say(str)
    c = b.contexts
    check_dict(c)
    print(res)
    if i == 'By':
        break

try:
    prolog = ps.Prolog()
    prolog.consult("./prolog.pl")
    for i in prolog.query("order(X,Y)"):
        print('{}\torder\t{}'.format(i['X'].upper(), i['Y'].upper()))
except:
    pass