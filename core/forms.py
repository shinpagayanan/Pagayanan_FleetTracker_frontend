from django import forms


class LoginForm(forms.Form):

    username = forms.CharField(
        max_length=150
    )

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    website = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

class AssetAssignmentForm(
    forms.Form
):

    assigned_to = forms.ChoiceField(
        label="Assign To"
    )

    def __init__(
        self,
        *args,
        users=None,
        **kwargs
    ):
        super().__init__(
            *args,
            **kwargs
        )

        self.fields[
            "assigned_to"
        ].choices = users or []

class MaintenanceRequestForm(forms.Form):

    asset = forms.TypedChoiceField(
        coerce=int
    )

    issue_description = forms.CharField(
        widget=forms.Textarea
    )

class MileageForm(forms.Form):

    asset = forms.TypedChoiceField(
            coerce=int
        )


    mileage = forms.IntegerField()

    def __init__(
        self,
        *args,
        asset_choices=None,
        **kwargs
    ):

        super().__init__(*args, **kwargs)

        self.fields[
            "asset"
        ].choices = asset_choices or []

# forms.py

class AssetForm(forms.Form):

    asset_code = forms.CharField()

    name = forms.CharField()

    asset_type = forms.ChoiceField(
        choices=[
            ("VEHICLE", "Vehicle"),
            ("IT", "IT Equipment"),
        ]
    )

    photo = forms.ImageField(
        required=False
    )

    purchase_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"}
        )
    )

    procurement_cost = forms.DecimalField()

    status = forms.ChoiceField(
    choices=[
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
    ]
)

    plate_number = forms.CharField(
        required=False
    )

    current_mileage = forms.IntegerField(
        required=False
    )

    maintenance_interval = forms.IntegerField(
        required=False
    )

class UserForm(forms.Form):

    first_name = forms.CharField(
        required=False
    )

    last_name = forms.CharField(
        required=False
    )

    username = forms.CharField()

    email = forms.EmailField()

    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False
    )

    role = forms.ChoiceField(
        choices=[
            ("STAFF", "Staff"),
            ("AUDITOR", "Auditor"),
            ("MANAGER", "Manager"),
        ]
    )

class BulkAssetAssignmentForm(forms.Form):

    assigned_to = forms.ChoiceField()

    asset_ids = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    def __init__(
        self,
        *args,
        users=None,
        assets=None,
        **kwargs
    ):
        super().__init__(
            *args,
            **kwargs
        )

        self.fields[
            "assigned_to"
        ].choices = users or []

        self.fields[
            "asset_ids"
        ].choices = assets or []