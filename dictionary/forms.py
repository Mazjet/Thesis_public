from django import forms

from .models import UserSuggestion


class UserSuggestionForm(forms.ModelForm):
    class Meta:
        model = UserSuggestion
        fields = ["candidate_term", "candidate_definition", "contact_email"]
        widgets = {
            "candidate_definition": forms.Textarea(attrs={"rows": 6}),
        }
