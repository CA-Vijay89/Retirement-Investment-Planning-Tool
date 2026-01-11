from django import forms

class RetirementForm(forms.Form):

    age = forms.IntegerField(
        label="Age",
        min_value=18,
        max_value=70
    )

    gender = forms.ChoiceField(
        choices=[
            ("Male", "Male"),
            ("Female", "Female")
        ]
    )

    education = forms.ChoiceField(
        choices=[
            ("Bachelors", "Bachelors"),
            ("Masters", "Masters")
        ]
    )

    field = forms.ChoiceField(
        label="Field of Work",
        choices=[
            ("Finance", "Finance"),
            ("IT", "IT"),
            ("Medical", "Medical"),
            ("Teaching", "Teaching"),
            ("Others", "Others")
        ]
    )

    monthly_expense = forms.IntegerField(
        label="Current Monthly Expenses (₹)",
        min_value=1000
    )

    retirement_age = forms.IntegerField(
        label="Expected Retirement Age",
        min_value=40,
        max_value=75
    )
