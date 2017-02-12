from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import Http404
import datetime
import time


class Person(User):
    picture = models.CharField(max_length=255, null=True, blank=True)
    fb_id = models.CharField(max_length=255, null=True, blank=True)

    @staticmethod
    def update_who_is_using(users, session):
        _p = session.person
        for u in users:
            if u.pk == _p.pk:
                u.using_account = True
                return u

    @classmethod
    def get_by_email(cls, email, raise404=None):
        try:
            return cls.objects.get(email=email)
        except cls.DoesNotExist:
            if raise404:
                raise Http404
            return None

    @classmethod
    def set_picture(cls, user):
        person = cls.get_by_email(user.email)
        user.picture = None if not person else person.picture

    @property
    def last_session(self):
        try:
            return SessionAccount.objects.filter(person=self).latest('id').start_at
        except SessionAccount.DoesNotExist:
            return None


class SessionAccount(models.Model):
    UTC_DIFFERENCE = 18000  # seconds

    start_at = models.DateTimeField(auto_now_add=True)
    session_time = models.IntegerField()  # in minutes
    person = models.ForeignKey(Person)
    is_active = models.BooleanField(default=True)

    @property
    def is_available(self):
        if not self.is_active:
            return False
        return self.expire_at > timezone.now()

    @property
    def expire_at(self):
        return self.start_at + datetime.timedelta(minutes=self.session_time)

    @property
    def remaining(self):
        return time.mktime(self.expire_at.timetuple()) - time.mktime(datetime.datetime.now().timetuple()) - self.UTC_DIFFERENCE

    @property
    def expire_at_seconds(self):
        return time.mktime(self.expire_at.timetuple())
