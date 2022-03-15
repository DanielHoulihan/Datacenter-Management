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

class ChanegThresholdForm(forms.Form):
    low = forms.CharField(required=True)
    medium = forms.CharField(required=True)

    def clean(self):
        low = self.cleaned_data['low']
        medium = self.cleaned_data['medium']

        if float(low) > float(medium):
            raise forms.ValidationError("Upper must be greater than lower")

        if float(low) < 0 or float(low) > 100:
            raise forms.ValidationError("Low must be between 0 and 100")

        if float(medium) < 0 or float(medium) > 100:
            raise forms.ValidationError("Upper must be between 0 and 100")
        
        return float(low),float(medium)


