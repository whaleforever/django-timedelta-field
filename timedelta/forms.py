from django import forms
from django.utils.translation import ugettext_lazy as _

import datetime
from collections import defaultdict

from widgets import TimedeltaWidget
from models import parse

class TimedeltaFormField(forms.Field):
    default_error_messages = {
        'invalid':_('Enter a valid time span: e.g. "3 days, 4 hours, 2 minutes"')
    }
    
    def __init__(self, *args, **kwargs):
        defaults = {'widget':TimedeltaWidget}
        defaults.update(kwargs)
        super(TimedeltaFormField, self).__init__(*args, **defaults)
        
    def clean(self, value):
        # import pdb; pdb.set_trace()
        super(TimedeltaFormField, self).clean(value)
        if value == '' and not self.required:
            return u''
        
        data = defaultdict(float)
        try:
            return parse(value)
            for part in value.split(','):
                value, which = part.strip().split(' ')
                if not which.endswith('s'):
                    which += "s"
                if which == "wks":
                    which = "weeks"
                if which == "mins":
                    which = "minutes"
                if which == "secs":
                    which = "seconds"
                data[which] = float(value)
        except TypeError:
            raise forms.ValidationError(self.error_messages['invalid'])
            
        return datetime.timedelta(**data)