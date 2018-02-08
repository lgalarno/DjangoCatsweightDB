from django import forms

from CatsManagement.models import Cat

import datetime

class SelectCatsForm(forms.Form):
    selectc = forms.ModelMultipleChoiceField(
        label= 'Select cat(s)',
        queryset = Cat.objects.all(), # not optional, use .all() if unsure
        widget  = forms.CheckboxSelectMultiple(attrs={"checked":""}),
    )
    fromdate = forms.DateField(
        label='From',
        required=False,
        widget=forms.TextInput(attrs=
                                {
                                    'class':'datepick',
                                    'id':'datepicker1'
                                }
        )
    )
    todate = forms.DateField(
        label='To',
        required=False,
        widget=forms.TextInput(attrs=
                                {
                                    'class':'datepick',
                                    'id':'datepicker2'
                                }
        )
    )

    def clean_todate(self):
        todate = self.cleaned_data["todate"]
        currentdate = datetime.datetime.now().date()
        if todate:
            if todate > currentdate:
                raise forms.ValidationError("This cannot be a future date!")
        return todate

    def clean(self):
        cleaned_data = super(SelectCatsForm, self).clean()
        if not self.errors:
            fromdate = self.cleaned_data["fromdate"]
            todate = self.cleaned_data["todate"]
            if todate and fromdate:
                if todate < fromdate:
                    raise forms.ValidationError({'fromdate': ["End time cannot be earlier than start time!", ]})
        return cleaned_data