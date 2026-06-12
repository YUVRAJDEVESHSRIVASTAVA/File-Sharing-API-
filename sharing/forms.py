from django import forms


class ShareForm(forms.Form):
    file = forms.FileField()
    sender_email = forms.EmailField()
    recipient_email = forms.EmailField()


class DeclineForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
