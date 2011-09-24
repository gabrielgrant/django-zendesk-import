import os.path

from django.core.management.base import BaseCommand, CommandError
from zendesk_import import models as zd_models
from zendesk_import.importer import XMLImporter

class Command(BaseCommand):
    help = 'Imports the supplied Zendesk data dump into Django'
    args = '<path_to_zendesk_dump>'

    def handle(self, *args, **kwargs):
        if len(args) != 1:
            raise CommandError(
                'Exaclty one argument is needed: the path to the Zendesk data')
        base_path = args[0]
        model_names = 'Account, Organization, User, Forum, Entry, Post'.split(', ')
        for model_name in model_names:
            model = getattr(zd_models, model_name)
            plural_model_name = model._meta.verbose_name_plural.lower()
            xml_filename = os.path.join(base_path, '%s.xml' % plural_model_name)
            XMLImporter(xml_filename, model).do_import()
