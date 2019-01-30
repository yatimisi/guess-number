from django.http import HttpResponse
from django.shortcuts import render, redirect
import random, string


def index(request):

    if 'target' not in request.session:
        create(request)
        message = '請輸入四個數字：'
    else:
        message = check(request)

        if(message == None):
            del message
            message = guess(request)

    return render(request, 'index.html', { 'message': message,
                                            'target': "".join(str(x) for x in request.session.get('target')),
                                            })


def create(request):
    target = random.sample(string.digits, 4)

    request.session['target'] = target
    request.session['count'] = 0


def check(request):
    number = request.POST.get('number')

    if len(number) != 4:
        return '長度須為4!'

    if not number.isdigit():
        return '請輸入數字!'


def guess(request):

    guess = list(request.POST.get('number'))
    target = request.session.get('target')
    request.session['count'] = request.session.get('count') + 1

    a, b = 0, 0
    for i, j in zip(target, guess):
        if i == j:
            a += 1
        elif j in target:
            b += 1

    if a == 4:
        return '恭喜你猜對了! 答案是：{} 您總共猜了{}次'.format("".join(str(x) for x in target), request.session.get('count'))
    else:
        return '{}A{}B'.format(a,b)
