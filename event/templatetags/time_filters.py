from django import template
import datetime

register = template.Library()

@register.filter
def format_timedelta(td):
    if not isinstance(td, datetime.timedelta):
        return str(td)
    
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days}d {hours}h {minutes}m {seconds}s"