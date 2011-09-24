import re

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from askbot import models as askbot_models
from zendesk_import import models as zd_models


class Command(BaseCommand):
    help = 'Imports the Zendesk info into Askbot'
    args = ''

    def handle(self, *args, **kwargs):
        # 
        default_userid_setting_name = 'ASKBOT_IMPORT_FROM_ZENDESK_DEFAULT_USER_ID'
        default_userid = getattr(settings, default_userid_setting_name, None)
        if default_userid is None:
            default_user = None
        else:
            default_user = askbot_models.User.objects.get(id=default_userid)
        # import entries as questions using forums as tags
        entries = zd_models.Entry.objects  \
            .filter(is_public=True)  \
            .exclude(submitter__django_user=None)

        print 'Importing %s Zendesk Entries as Askbot Questions' % len(entries)
        for entry in entries:
            q = entry.submitter.django_user.post_question(
                title=entry.title,
                body_text=entry.body,
                tags=re.sub(r'\s+', '_', entry.forum.name.lower()),
                timestamp=entry.updated_at,
            )
            # import posts as answers
            for post in entry.posts.all():
                u = post.user.django_user or default_user
                if u is not None:
                    u.post_answer(
                        question=q,
                        body_text=post.body,
                        timestamp=post.updated_at,
                    )
