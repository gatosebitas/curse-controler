from django.utils.timezone import make_aware
from datetime import datetime

passed = make_aware(datetime(2000, 1, 1))


def sort_by_last_session(obj):
    if not obj.last_session:
        return passed
    return obj.last_session
