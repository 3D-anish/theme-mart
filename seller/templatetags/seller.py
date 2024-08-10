from django import template

register = template.Library()

def you_earned(sell_objs):  # Only one argument.
    total_earnings = sum(sell.final_sell for sell in sell_objs)
    return total_earnings

def paid(sell_objs):  # Only one argument.
    total_earnings = sum(sell.final_sell for sell in sell_objs.filter(paid = True))
    return total_earnings

register.filter('you_earned', you_earned)
register.filter('paid', paid)
