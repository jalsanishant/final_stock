from django.shortcuts import render_to_response, get_object_or_404
from models import StockStatus, Stock, Order, Position, Portfolio
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse, Http404
from updater import update

def render_error(request, error):
    if request.user.is_authenticated():
        portfolio = get_object_or_404(Portfolio, user=request.user)
        hist = list(reversed(list(portfolio.history.all())))[:5]
        return render_to_response('portfolio.html', 
            {'portfolio': portfolio, 'hist': hist, 'error': error})
    else:
        return render_to_response('index.html', {'error': error})

def index(request):
    if request.user.is_authenticated():
        portfolio = get_object_or_404(Portfolio, user=request.user)
        hist = list(reversed(list(portfolio.history.all())))[:5]
        return render_to_response('portfolio.html', 
            {'portfolio': portfolio, 'hist': hist})
    else:
        return render_to_response('index.html')

def register(request):
    uname = request.POST["username"]
    passw = request.POST["password"]

    if request.POST["username"] == "" or request.POST["password"] == "":
        return render_to_response('index.html',
            {'error': 'You did not fill out the form completely'})
    
    if User.objects.filter(username = request.POST["username"]).count() != 0:
        return render_to_response('index.html',
            {'error':  'There is already a user with this username'})
    
    User.objects.create_user(uname, '', passw)
    u = auth.authenticate(username=uname, password=passw)
    auth.login(request, u)
    
    p = Portfolio(user = u, balance = 10000, value = 0)
    
    p.save()
    
    return HttpResponseRedirect('/')

def login(request):
    # Will have username/password in request.POST
    uname = request.POST["username"]
    passw = request.POST["password"]
    # Authenticate User
    user = auth.authenticate(username = uname, password = passw)
    # If good, redirect to /
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/')
    else:
        return render_to_response('index.html',
            {'error': 'There was an error with your login'})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def help(request):
    return render_to_response('help.html')

def search(request, query):
    if query is None:
        query = request.POST['q']
    query = query.upper()
    return HttpResponseRedirect('/stock/%s/' % query)

def show_stock(request, symbol):
    stks = Stock.objects.filter(symbol=symbol)
    if stks.count() == 0:
        stk = Stock(symbol=symbol, price=0.0)
        stk.save()
    elif stks.count() == 1:
        stk = stks[0]
    else:
        return HttpResponse("%s" % stks.count())
    try:
        ss = stk.history.order_by('date')[0]
    except:
        update(stk)
        ss = stk.history.order_by('date')[0]
    return render_to_response('stock.html', {'stock': stk, 'status': ss})

def handle_buy(request):
    
    if request.user.is_authenticated(): 
        p = Portfolio.objects.get(user=request.user)
    else:
        return render_error(request, 'You don\'t seem to be logged in')
      
    symbol = request.POST["symbol"] 
    stk = Stock.objects.get(symbol=symbol)
    
    try:
        share = int(request.POST['number_of_shares'])
    except:
        return render_error(request, 'Try entering a real number')
    
    if p.balance < share * stk.price:
        return render_error(request, "Insufficient funds deadbeat")
    
    o = Order(type='buy', amount=share, stock=stk)
    o.save()
    
    p.history.add(o)
    p.save()
    
    pos = p.positions.filter(stock=stk)
    
    if pos.count() == 1:
        pos = pos[0]
        pos.amount = pos.amount + share
        pos.value = pos.amount * stk.price
        pos.save()
    
    else:
        pos = Position(amount=share, stock=stk, value=share * stk.price)
        pos.save()
        p.positions.add(pos)
        p.save()
    
    p.value += share * stk.price
    p.balance -= share * stk.price
    p.save()
    
    return HttpResponseRedirect('/')

def handle_sell(request):
    
    if request.user.is_authenticated(): #check if user is authenticate
        p = Portfolio.objects.get(user=request.user)
    else:
        return render_error(request, 'You don\'t seem to be logged in')
    # Then find the stock symbol in request.POST    
    symbol = request.POST["symbol"] 
    stk = Stock.objects.get(symbol=symbol)
    # And the number of shares in request.POST
    try:
        share = int(request.POST['number_of_shares'])
    except:
        return render_error(request, 'Try entering a real number')
    
    pos = p.positions.filter(stock=stk)
    if pos.count() == 0:
        return render_error(request, 'You don\'t own any of that stock')
    else:
        pos = pos[0]
        if pos.amount < share:
            return render_error(request, 'You don\'t own enough of that stock')
        pos.amount = pos.amount - share
        pos.save()
        pos.value = pos.amount * stk.price
        pos.save()
    p.value -= share * stk.price
    p.balance += share * stk.price
    p.save()
    
    o = Order(type='sell', amount=share, stock=stk)
    o.save()
    p.history.add(o)
    p.save()
    
    return HttpResponseRedirect('/')

def show_leaders(request):
    plist = list(reversed(list(Portfolio.objects.order_by('value'))))
    return render_to_response('leaderboard.html', {'portfolios': plist})


