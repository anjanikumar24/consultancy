import re

from django import forms

from .models import LEVEL_CHOICES, Destination, Enquiry

PHONE_RE = re.compile(r"^\+?[\d\s\-()]{7,19}$")


class EnquiryForm(forms.ModelForm):
    consent = forms.BooleanField(
        required=True, error_messages={"required": "Please agree to be contacted so we can respond."})
    country_interest = forms.ChoiceField(required=False)
    website = forms.CharField(required=False, widget=forms.TextInput(attrs={"tabindex": "-1", "autocomplete": "off"}))  # honeypot

    class Meta:
        model = Enquiry
        fields = ["name", "email", "phone", "enquiry_type", "country_interest", "study_level", "message", "consent"]
        widgets = {"message": forms.Textarea(attrs={"rows": 4, "maxlength": 2000})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        names = list(Destination.objects.filter(is_active=True).values_list("name", flat=True))
        self.fields["country_interest"].choices = [("", "Not decided")] + [(n, n) for n in names] + [("Other", "Other")]
        self.fields["study_level"].choices = [("", "Select")] + LEVEL_CHOICES
        self.fields["enquiry_type"].widget = forms.HiddenInput()
        self.fields["name"].widget.attrs.update(autocomplete="name", maxlength=120)
        self.fields["email"].widget.attrs.update(autocomplete="email")
        self.fields["phone"].widget.attrs.update(autocomplete="tel", placeholder="+91 98765 43210", maxlength=20)
        for name, field in self.fields.items():
            w = field.widget
            if isinstance(w, forms.HiddenInput) or name == "website":
                continue
            css = "form-check-input" if isinstance(w, forms.CheckboxInput) else (
                "form-select" if isinstance(w, forms.Select) else "form-control")
            w.attrs["class"] = css

    def full_clean(self):
        super().full_clean()
        for name in self.errors:
            if name in self.fields:
                w = self.fields[name].widget
                w.attrs["class"] = (w.attrs.get("class", "") + " is-invalid").strip()

    def clean_name(self):
        value = " ".join(self.cleaned_data["name"].split())
        if len(value) < 2:
            raise forms.ValidationError("Please enter your full name.")
        return value

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()

    def clean_phone(self):
        value = self.cleaned_data["phone"].strip()
        if not PHONE_RE.match(value) or sum(c.isdigit() for c in value) < 7:
            raise forms.ValidationError("Enter a valid phone number, e.g. +91 98765 43210.")
        return value
