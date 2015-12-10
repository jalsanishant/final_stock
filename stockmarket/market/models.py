from django.db import models
from django.contrib.auth.models import User

class StockStatus(models.Model):
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

class Stock(models.Model):
    symbol = models.CharField(max_length=25)
    exchange = models.CharField(max_length=25)
    history = models.ManyToManyField(StockStatus)
    price = models.FloatField()
    def __unicode__(self): return self.symbol

class Order(models.Model):
    type   = models.CharField(max_length=25)
    amount = models.IntegerField()
    stock  = models.ForeignKey(Stock)
    date   = models.DateTimeField(auto_now_add=True)
    def __unicode__(self): return u'%s %s' % (self.type, self.stock.symbol)

class Position(models.Model):
    amount = models.IntegerField()
    stock  = models.ForeignKey(Stock)
    value  = models.FloatField()
    def __unicode__(self): return u'%s of %s' % (self.amount, self.stock.symbol)

class Portfolio(models.Model):
    user      = models.ForeignKey(User)
    history   = models.ManyToManyField(Order)
    positions = models.ManyToManyField(Position)
    value     = models.FloatField()
    balance   = models.FloatField()
    created   = models.DateTimeField(auto_now_add=True)

    def __unicode__(self): return self.user.username
