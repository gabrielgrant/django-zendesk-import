from django.db import models

class Account(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

class Organization(models.Model):
    id = models.IntegerField(primary_key=True)

class User(models.Model):
    django_user = models.ForeignKey('auth.User', related_name='zendesk_users', null=True)
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    is_active = models.BooleanField()
    last_login = models.DateTimeField(null=True)
    locale_id = models.IntegerField(null=True)
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(
        Organization,
        related_name='users',
        null=True,
    )
    phone = models.CharField(max_length=20)
    restriction = models.SmallIntegerField(choices=[
        (0, 'All tickets'),
        (1, 'Tickets in member groups'),
        (2, 'Tickets in member organization'),
        (3, 'Assigned tickets'),
        (4, 'Tickets requested by user'),
    ])
    role = models.SmallIntegerField(choices=[
        (0, 'End user'),
        (2, 'Administrator'),
        (4, 'Agent')
    ])
    # time_zone =  <- non-standard format. #TODO
    updated_at = models.DateTimeField()
    uses_12_hour_clock = models.BooleanField()
    email = models.EmailField(max_length=255)
    is_verified = models.BooleanField()
    photo_url = models.URLField(verify_exists=False)

class Forum(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.TextField(blank=True)
    name = models.CharField(max_length=255)
    is_public = models.BooleanField()

class Entry(models.Model):
    id = models.IntegerField(primary_key=True)
    body = models.TextField()
    created_at = models.DateTimeField()
    forum = models.ForeignKey(Forum, related_name='entries')
    is_locked = models.BooleanField()
    is_pinned = models.BooleanField()
    is_public = models.BooleanField()
    submitter = models.ForeignKey(User, related_name='entries')
    title = models.CharField(max_length=255)
    updated_at = models.DateTimeField()
    votes_count = models.IntegerField(null=True)

    class Meta:
        verbose_name_plural = 'entries'

class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    account = models.ForeignKey(Account, related_name='posts')
    body = models.TextField()
    created_at = models.DateTimeField()
    entry = models.ForeignKey(Entry, related_name='posts')
    forum = models.ForeignKey(Forum, related_name='posts')
    is_informative = models.BooleanField()
    updated_at = models.DateTimeField()
    user = models.ForeignKey(User, related_name='posts')

