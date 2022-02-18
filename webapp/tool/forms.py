from django import forms

class SelectCurrentForm(forms.Form):
    current_datacenter = forms.CharField(required=False)

    def clean_current_datacenter(self):
        data = self.cleaned_data['current_datacenter']
        return data



class DeleteConfigurationForm(forms.Form):
    to_delete = forms.CharField(required=True)

    def clean_current_datacenter(self):
        data = self.cleaned_data['to_delete']
        return data




