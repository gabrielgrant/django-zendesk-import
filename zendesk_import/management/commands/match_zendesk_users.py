from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from zendesk_import.models import User as ZDUser

class Command(BaseCommand):
    help = 'Loads the supplied Zendesk data dump into Django'
    args = ''

    def handle(self, *args, **kwargs):
        pre_count = ZDUser.objects.filter(django_user=None).count()
        for zdu in ZDUser.objects.all():
            try:
                u = User.objects.get(email=zdu.email)
            except User.DoesNotExist:
                u = None
            except User.MultipleObjectsReturned:
                u = User.objects.filter(email=zdu.email)
                print 'multiple users returned for %s: %s' % (zdu.email, u)
                u = u[0]
            if u:
                zdu.django_user = u
                zdu.save()
        post_count = ZDUser.objects.filter(django_user=None).count()
        linked_count = pre_count - post_count
        total_count = ZDUser.objects.count()
        print 'Successfully linked %s of %s accounts' % (linked_count, total_count)

