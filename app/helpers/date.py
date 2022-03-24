from datetime import datetime, timezone

def distance(dt):
    current_dt = datetime.now()
    return current_dt - dt

def local_time(timestamp):
    return timestamp.replace(tzinfo=timezone.utc).astimezone(tz=None)
