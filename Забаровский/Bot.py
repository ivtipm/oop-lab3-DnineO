import re
import random
import datetime
from time import localtime, strftime

class Bot(object):
    user_name = None
    def __init__(self):
        super().__init__()

    def set_user_name(self, name):
        self.user_name = name
    
    def answer_message(self, message):

        answer, mess_type = self.check_culc(message)
        
        if mess_type != 'calc':
            mess_type = self.check_message_type(message)
            if mess_type == 'date':
                answer = self.get_date()
            if mess_type == 'time':
                answer = self.get_time()
            if mess_type!='date' and mess_type!='time':
                answer = self.create_answers(mess_type)
        return answer
    


    def create_answers(self, mess_type):
        greetlist= ['Привет', 'Здравствуй','Доброго времени суток']
        byelist = ['Пока', 'До свидания', 'До встречи']
        answers_type= {'greeting':[greet+', '+self.user_name+" !" for greet in greetlist],
        'bye': [bye+', '+self.user_name + " !" for bye in byelist],
        'howareyou': ['Хорошо', 'Нормально', 'Замечательно', 'Прекрасно'],
        'commands':['Я умею делать арифметические операции: например "Посчитай 2+2", "Сложи 4 и 7","Сколько будет 9.536 поделить на -3". Могу вывести дату и время, побеседовать и рассказать анекдот'],
        'dont_understand': ['Даже не знаю, что ответить'],
        'thankyou':['Всегда пожалуйста :)', 'Не за что', 'Всегда рад помочь :)'],
        'anekdot': ['Только неграмотный человек на вопрос "Как найти площадь Ленина?" отвечает "длину Ленина умножить на ширину Ленина..."А грамотный знает, что надо взять интеграл по поверхности!',
                    ' Разговор на экзамене по математическому анализу. Преподаватель:"А что вы будете делать, если я попрошу вас посчитать сумму этого ряда?" Студент:" Я повешусь!" Преподаватель:" Правильно, он не сходится." ']}
        answer = random.choice(answers_type[mess_type])
        return answer

    def get_date(self):
        date = strftime("%Y-%m-%d %H:%M:%S", localtime()).split(' ')[0].split("-")
        answer = 'Сегодня ' + date[2]+'.'+date[1]+'.'+date[0]
        return answer 
    def get_time(self):
        time = strftime("%Y-%m-%d %H:%M:%S", localtime()).split()[1]
        answer = 'Сейчас ' + time
        return answer


    def check_message_type(self, message):
        phrases_type = {'greeting':['Привет', 'Здравствуй','Добрый день','Добрый вечер','Доброе утро'],
        'bye': ['Пока', 'До свидания', 'До встречи'], 'howareyou': ['Как ты','Как дела', 'Как поживаешь'],
        'commands': ['Что ты умеешь', 'Что ты можешь', 'Расскажи о себе'], 'date': ['дата', 'число'],
        'time': ['время', 'времени'], 'anekdot':["анекдот"], 'thankyou':['Спасибо','благодарю'] }
        mess_type = "dont_understand"
        for phr_type in phrases_type:
            for word in phrases_type[phr_type]:
                if message.find(word) !=-1 or message.find(word.lower()) != -1:
                    mess_type = phr_type

        return mess_type

    
    def check_culc(self, message):
        calc_type = None
        mess_type = None
        finded = 0
        answer = None
        operandlist= {'плюс': '+','минус':'-'}
        operactions= {'Умножь': "*", "Подели": "/", "Сложи": "+", "Вычти": "-"}
        math_string = self.create_math_expression(message)
        if math_string:
            try:
                answer = str(eval(math_string))
            except ZeroDivisionError:
                answer=' На ноль делить нельзя!'
            finded = 1
        else:
            for action in operactions:
                if message.find(action) != -1 or message.find(action.lower()) != -1:
                    finded = 1
                    answer = self.math_expr_with_words(message,action, operactions)
            if finded == 0:
                for operand in operandlist:
                    if message.find(operand) != -1:
                        message = message.replace(operand,operandlist[operand])
                        math_string = self.create_math_expression(message)
                        try:
                            answer = str(eval(math_string))
                            finded =1
                        except TypeError:
                            answer = 'Операнды должны быть числа, а не слова!'
                            finded = 1
        if finded == 1:
            calc_type = True
            mess_type = 'calc'
        else:
            calc_type = False


        return answer, mess_type

    

    def create_math_expression(self, message):
        match=re.search(r'(-?\d+(?:\.\d+)?)\s*([-+*\/])\s*(-?\d+(?:\.\d+)?)',message)
        math_string = match[0] if match else None
        return math_string
    


    def math_expr_with_words(self,message,action,operactions):
        numlist = re.findall(r'(-?\d+(?:\.\d+)?)', message)
        if numlist:
            if (operactions[action] == '/' and (numlist[1] == "0" or numlist[1] == "0.0")):
                answer = ' На ноль делить нельзя!'
            else:
                math_string = numlist[0]+operactions[action]+numlist[1]
                try:
                    answer = str(eval(math_string))
                except ZeroDivisionError:
                    answer=' На ноль делить нельзя!'
        else:
            answer = 'Операнды должны быть числа, а не слова!' 
        return answer
