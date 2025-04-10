from datetime import datetime, timedelta


# 🕒 Generate time slots (returns list of time strings)
def generate_time_slots(start_time, end_time, slot_duration=30):
    """
    Example:
    generate_time_slots("10:00", "13:00", 30)
    -> ["10:00", "10:30", "11:00", "11:30", "12:00", "12:30"]
    """
    fmt = "%H:%M"
    slots = []
    current = datetime.strptime(start_time, fmt)
    end = datetime.strptime(end_time, fmt)

    while current + timedelta(minutes=slot_duration) <= end:
        slots.append(current.strftime(fmt))
        current += timedelta(minutes=slot_duration)
    return slots


# 📅 Get today's date in yyyy-mm-dd format
def today_date():
    return datetime.now().strftime("%Y-%m-%d")


# 🧾 Format datetime string
def format_datetime(dt_str, fmt_in="%Y-%m-%dT%H:%M:%S", fmt_out="%d-%m-%Y %I:%M %p"):
    try:
        dt = datetime.strptime(dt_str, fmt_in)
        return dt.strftime(fmt_out)
    except Exception:
        return dt_str


# ✅ Check if a time is within range
def is_time_within_range(start, end, check):
    """
    Returns True if check is between start and end.
    All params in "HH:MM" format.
    """
    t_start = datetime.strptime(start, "%H:%M")
    t_end = datetime.strptime(end, "%H:%M")
    t_check = datetime.strptime(check, "%H:%M")
    return t_start <= t_check <= t_end


# 🔍 Parse Mongo ObjectId (string-safe)
def parse_objectid(oid):
    try:
        from bson import ObjectId
        return ObjectId(oid)
    except Exception:
        return None
