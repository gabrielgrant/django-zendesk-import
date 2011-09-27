import sys
import os.path
from xml.etree.ElementTree import parse
import iso8601
from glob import glob
from zendesk_import import models as zd_models

class XMLImporter(object):
    def __init__(self, xml_file, model, field_name_conversions=None):
        self.xml_file = xml_file
        if field_name_conversions is None:
            model_name = model.__name__.lower()
            field_name_conversions = TAG_NAME_CONVERSIONS.get(model_name, {})
        self.field_name_conversions = field_name_conversions
        self.model = model

    def do_import(self):
        xml_doc = parse(self.xml_file)
        models = []
        for c in xml_doc.getroot().getchildren():
            m = self.model()
            for xml_field in c.getchildren():
                model_field_name = self.convert_tag_name(xml_field.tag)
                if hasattr(m, model_field_name):
                    val = self.convert_tag_value(xml_field) 
                    setattr(m, model_field_name, val)
            try:
                m.save()
            except:
                # print extra debug info
                print m, [(f, getattr(m, f.name)) for f in m._meta.fields]
                raise
            models.append(m)
        return models

    def convert_tag_name(self, name):
        converted_name = self.field_name_conversions.get(name, name)
        return converted_name.replace('-', '_')

    def convert_tag_value(self, tag):
        tag_value = tag.text
        tag_type = tag.get('type')
        if tag.get('nil') == 'true':
            if tag_type is not None:
                return None
            else:
                return ''
        val = TAG_VALUE_CONVERSIONS.get(tag_type, lambda x: x)(tag_value)
        if val is None:
            print 'a None got through!', tag, tag_value, tag_type
        return val

TAG_NAME_CONVERSIONS = {
    'user': {
        'restriction-id': 'restriction',
        'roles': 'role',
    }
}

TAG_VALUE_CONVERSIONS = {
    'datetime': lambda x: iso8601.parse_date(x),
    'boolean': lambda x: x != 'false',
    'integer': lambda x: int(x),
    None: lambda x: '' if x is None else x,
}

def main(base_path):
    model_names = 'Account, Organization, User, Forum, Entry, Post'.split(', ')
    for model_name in model_names:
        #if testmode:
        if False:
            model = Mock()
        else:
            model = getattr(zd_models, model_name)
        xml_filename = os.path.join(base_path, '%ss.xml' % model_name.lower())
        print XMLImporter(xml_filename, model).do_import()


if __name__ == '__main__':
    if 1 >= len(sys.argv) >= 4:
        print 'Usage: import.py [--test] <basepath>'
        sys.exit(-1)
    if sys.argv[1] == '--test':
        from mock import Mock
        testmode = True
        base_path = sys.argv[2]
    else:
        testmode = False
        base_path = sys.argv[1]
    

