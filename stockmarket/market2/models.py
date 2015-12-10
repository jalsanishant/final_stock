from django.db import models
from django.contrib.auth.models import User

class StockStatus2(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()
    change = models.FloatField()
    volume = models.IntegerField()
    average_daily_volume = models.IntegerField()
    market_cap = models.CharField(max_length=100)
    book_value = models.FloatField()
    ebitda = models.CharField(max_length=100)
    dividend_per_share = models.FloatField()
    dividend_yield = models.FloatField()
    earnings_per_share = models.FloatField()
    i52_week_high = models.FloatField()
    i52_week_low = models.FloatField()
    i50_day_moving_average = models.FloatField()
    i200_day_moving_average = models.FloatField()
    price_to_earnings_ratio = models.FloatField()
    price_to_earnings_growth_ratio = models.FloatField()
    price_to_sales_ratio = models.FloatField()
    price_to_book_ratio = models.FloatField()

class Stock2(models.Model):
    symbol = models.CharField(max_length=25)
    exchange = models.CharField(max_length=25)
    history = models.ManyToManyField(StockStatus2)
    price = models.FloatField()
    def __unicode__(self): return self.symbol

class Order2(models.Model):
    type   = models.CharField(max_length=25)
    username = models.CharField(max_length=25)
    amount = models.IntegerField()
    stock  = models.ForeignKey(Stock2)
    date   = models.DateTimeField(auto_now_add=True)
    datestr = models.CharField(max_length=50)
    money = models.IntegerField()
    def __unicode__(self): return u'%s %s' % (self.type, self.stock.symbol)

class Position2(models.Model):
    amount = models.IntegerField()
    stock  = models.ForeignKey(Stock2)
    value  = models.FloatField()
    def __unicode__(self): return u'%s of %s' % (self.amount, self.stock.symbol)

class Portfolio2(models.Model):
    user      = models.ForeignKey(User)
    history   = models.ManyToManyField(Order2)
    positions = models.ManyToManyField(Position2)
    value     = models.FloatField()
    u         = models.CharField(max_length=25)
    balance   = models.FloatField()
    created   = models.DateTimeField(auto_now_add=True)
    def __unicode__(self): return self.user.username
