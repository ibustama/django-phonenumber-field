#-*- coding: utf-8 -*-
import string
import sys

from babel import Locale
from django.utils import translation
from django.forms import Select, TextInput
from django.forms.widgets import MultiWidget
from phonenumbers.data import _COUNTRY_CODE_TO_REGION_CODE

from phonenumber_field.phonenumber import PhoneNumber, to_python



class PhonePrefixSelect(Select):

    initial = None

    def __init__(self, initial=None):
        choices = []
        locale = Locale(translation.get_language())
        for prefix, values in _COUNTRY_CODE_TO_REGION_CODE.iteritems():
            prefix = '+%d' % prefix
            if initial and initial in values:
                self.initial = prefix
            for country_code in values:
                country_name = locale.territories.get(country_code)
                if country_name:
                    choices.append((prefix, u'%s %s' % (prefix, country_name)))
        return super(PhonePrefixSelect, self).__init__(choices=[('', '---')]+sorted(choices, key=lambda item: item[1][string.find(item[1], ' '):]))

    def render(self, name, value, *args, **kwargs):
        return super(PhonePrefixSelect, self).render(name, value or self.initial, *args, **kwargs)

class PhoneNumberPrefixWidget(MultiWidget):
    """
    A Widget that splits phone number input into:
    - a country select box for phone prefix
    - an input for local phone number
    """
    def __init__(self, attrs=None, initial=None):
        widgets = (PhonePrefixSelect(initial),TextInput(),)
        super(PhoneNumberPrefixWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            #print >>sys.stderr, value.country_code
            #print >>sys.stderr, value.national_number
            #return ['+%s'%(value.country_code), value.national_number]
#            i = string.find(value, ' ')
#            return [value[:i], value[i+1:]]
            return value.split('-')
        return [None, None]

    def value_from_datadict(self, data, files, name):
        values = super(PhoneNumberPrefixWidget, self).value_from_datadict(data, files, name)
        print >>sys.stderr, values
        #return PhoneNumber(country_code=int(values[0][1:], national_number=int(values[1])))
        phone_number_string = '%s-%s'%tuple(values)
        if phone_number_string == '-':
            return ''
        return phone_number_string