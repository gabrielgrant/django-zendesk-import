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
            self.default_user = None
        else:
            self.default_user = askbot_models.User.objects.get(id=default_userid)
        # import entries as questions using forums as tags
        entries_public = zd_models.Entry.objects.filter(is_public=True)
        if self.default_user is None:
            entries = entries_public.exclude(submitter__django_user=None)
        else:
            entries = entries_public

        print 'Importing %s of %s public Zendesk Entries as Askbot Questions' % (
            len(entries), len(entries_public)
        )
        for entry in entries:
            self.import_entry_as_question(entry)
    def import_entry_as_question(self, entry):
        u = entry.submitter.django_user or self.default_user
        q = u.post_question(
            title=entry.title,
            body_text=entry.body,
            tags=re.sub(r'\s+', '_', entry.forum.name.lower()),
            timestamp=entry.updated_at,
        )
        # import posts as answers
        answer_count = 0
        for post in entry.posts.all():
            self.import_post_as_answer(post, q)
            answer_count += 1
        print 'Imported %s Posts as Answers to "%s"' % (answer_count, q)
    def import_post_as_answer(self, post, question):
        u = post.user.django_user or self.default_user
        if u is not None:
            u.post_answer(
                question=question,
                body_text=post.body,
                timestamp=post.updated_at,
            )
