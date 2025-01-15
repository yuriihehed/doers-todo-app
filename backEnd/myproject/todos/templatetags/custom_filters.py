from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def format_duration(duration):
    if not duration:
        return "00h00m00s"
    
    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    return f"{hours:02d}h{minutes:02d}m{seconds:02d}s"