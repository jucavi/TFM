from datetime import datetime, timezone

def distance(dt):
    current_dt = datetime.now()
    return current_dt - dt

def local_time(timestamp):
    lt = timestamp.astimezone()
    return timestamp + lt.utcoffset()
