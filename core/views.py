from django.shortcuts import render
from django.shortcuts import (
    render,
    redirect
)

from .forms import LoginForm, MaintenanceRequestForm, MileageForm, AssetForm, UserForm, BulkAssetAssignmentForm

from .services import api_post,api_put, api_delete,api_put_file,api_post_file

from django.shortcuts import (
    render,
    redirect,
)
from django.http import HttpResponse

from .forms import LoginForm
from .services import login_user

from django.core.paginator import Paginator



from .services import api_get

def home(request):

    return render(
        request,
        "home.html"
    )
def login_view(request):

    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(
            request.POST
        )

        if form.is_valid():

            # Honeypot check
            if form.cleaned_data["website"]:

                form.add_error(
                    None,
                    "Invalid login attempt."
                )

                return render(
                    request,
                    "auth/login.html",
                    {
                        "form": form
                    }
                )

            response = login_user(
                form.cleaned_data["username"],
                form.cleaned_data["password"]
            )

            if response.status_code == 200:

                data = response.json()

                access_token = data["access"]

                request.session["access_token"] = access_token

                request.session["refresh_token"] = data["refresh"]

                me_response = api_get(
                    "current-user/",
                    access_token
                )

                if me_response.status_code == 200:

                    me = me_response.json()

                    request.session["user_id"] = me["id"]

                    request.session["username"] = (
                        me["username"]
                    )

                    request.session["first_name"] = (
                        me.get("first_name", "")
                    )

                    request.session["last_name"] = (
                        me.get("last_name", "")
                    )

                    request.session["full_name"] = (
                        me.get(
                            "full_name",
                            me["username"]
                        )
                    )

                    request.session["user_role"] = (
                        me["role"]
                    )

                return redirect(
                    "dashboard"
                )

            try:

                data = response.json()

                error_message = data.get(
                    "detail",
                    "Login failed."
                )

            except Exception:

                error_message = (
                    "Login failed."
                )

            form.add_error(
                None,
                error_message
            )

    return render(
        request,
        "auth/login.html",
        {
            "form": form
        }
    )
def logout_view(request):

    request.session.flush()

    return redirect("login")

def dashboard(request):

    dashboard_response = api_get(
        "dashboard/",
        request.access_token
    )

    stats = dashboard_response.json()

    role = request.user_role

    if role == "MANAGER":

        alerts_response = api_get(
            "alerts/",
            request.access_token
        )

        return render(
            request,
            "dashboard/manager_dashboard.html",
            {
                "stats": stats,
                "alerts": alerts_response.json(),
            }
        )

    elif role == "AUDITOR":

        return render(
            request,
            "dashboard/auditor_dashboard.html",
            {
                "stats": stats
            }
        )

    return render(
        request,
        "dashboard/staff_dashboard.html",
        {
            "stats": stats
        }
    )
def asset_list(request):

    token = request.access_token

    query_string = []

    asset_type = request.GET.get(
        "asset_type"
    )

    status = request.GET.get(
        "status"
    )

    purchase_date_from = request.GET.get(
        "purchase_date_from"
    )

    purchase_date_to = request.GET.get(
        "purchase_date_to"
    )

    if asset_type:

        query_string.append(
            f"asset_type={asset_type}"
        )

    if status:

        query_string.append(
            f"status={status}"
        )

    if purchase_date_from:

        query_string.append(
            f"purchase_date_from={purchase_date_from}"
        )

    if purchase_date_to:

        query_string.append(
            f"purchase_date_to={purchase_date_to}"
        )

    endpoint = "assets/"

    if query_string:

        endpoint += (
            "?"
            + "&".join(query_string)
        )

    response = api_get(
        endpoint,
        token
    )

    assets = response.json()

    template = (
        "assets/assets_list.html"
    )

    if request.user_role == "STAFF":

        template = (
            "assets/staff_assets_list.html"
        )

    return render(
        request,
        template,
        {
            "assets":
                assets,

            "selected_asset_type":
                asset_type,

            "selected_status":
                status,

            "purchase_date_from":
                purchase_date_from,

            "purchase_date_to":
                purchase_date_to,
        }
    )

def asset_detail(
    request,
    asset_id
):

    response = api_get(
        f"assets/{asset_id}/",
        request.access_token
    )

    asset = response.json()

    return render(
        request,
        "assets/asset_detail.html",
        {
            "asset": asset
        }
    )
# views.py

def create_request(request):

    assets_response = api_get(
        "assets/",
        request.access_token
    )

    assets = assets_response.json()

    asset_choices = [

        (
            asset["id"],
            f'{asset["asset_code"]} - {asset["name"]}'
        )

        for asset in assets

        if asset["status"] == "ACTIVE"
    ]

    selected_asset = request.GET.get(
        "asset"
    )

    if request.method == "POST":

        form = MaintenanceRequestForm(
            request.POST
        )

        form.fields[
            "asset"
        ].choices = asset_choices

        if form.is_valid():

            response = api_post(
            "requests/",
            request.access_token,
            {
                "asset": form.cleaned_data["asset"],
                "issue_description": form.cleaned_data["issue_description"]
            }
        )

        if response.status_code in [200, 201]:

            return redirect(
                "my-requests"
            )

        elif response.status_code == 429:

            form.add_error(
                None,
                (
                    "Too many maintenance requests "
                    "submitted. Please wait."
                )
            )

        else:

            try:

                error_data = response.json()

                form.add_error(
                    None,
                    error_data.get(
                        "detail",
                        "Request failed."
                    )
                )

            except Exception:

                form.add_error(
                    None,
                    "Request failed."
                )
    else:

        form = MaintenanceRequestForm()

        form.fields[
            "asset"
        ].choices = asset_choices

        if selected_asset:

            form.initial[
                "asset"
            ] = selected_asset

    return render(
        request,
        "requests/create_request.html",
        {
            "form":
                form,

            "assets":
                assets,
        }
    )
def my_requests(request):

    response = api_get(
        "requests/",
        request.access_token
    )

    requests_data = (
        response.json()
    )

    return render(
        request,
        "requests/my_requests.html",
        {
            "requests":
            requests_data
        }
    )

def approve_request(
    request,
    request_id
):

    api_post(
        f"requests/{request_id}/approve/",
        request.access_token,
        {}
    )

    return redirect(
        "my-requests"
    )

def reject_request(
    request,
    request_id
):

    api_post(
        f"requests/{request_id}/reject/",
        request.access_token,
        {}
    )

    return redirect(
        "my-requests"
    )

def submit_mileage(request):

    assets_response = api_get(
        "assets/?asset_type=VEHICLE",
        request.access_token
    )

    vehicles = assets_response.json()

    asset_choices = [

        (
            vehicle["id"],
            vehicle["name"]
        )

        for vehicle in vehicles
    ]

    selected_asset = request.GET.get(
        "asset"
    )

    form = MileageForm(
        asset_choices=asset_choices
    )

    if selected_asset:

        form.initial[
            "asset"
        ] = selected_asset

    if request.method == "POST":

        form = MileageForm(
            request.POST,
            asset_choices=asset_choices
        )

        if form.is_valid():

            response = api_post(
            "mileage/",
            request.access_token,
            {
                "asset":
                    form.cleaned_data["asset"],

                "mileage":
                    form.cleaned_data["mileage"]
            }
        )

        if response.status_code in [200, 201]:

            return redirect(
                "mileage-history"
            )

        elif response.status_code == 429:

            form.add_error(
                None,
                (
                    "Too many mileage submissions. "
                    "Please wait."
                )
            )

        else:

            try:

                error_data = response.json()

                form.add_error(
                    None,
                    error_data.get(
                        "detail",
                        "Submission failed."
                    )
                )

            except Exception:

                form.add_error(
                    None,
                    "Submission failed."
                )

    return render(
        request,
        "mileage/submit.html",
        {
            "form":
                form
        }
    )

def mileage_history(request):

    response = api_get(
        "mileage/",
        request.access_token
    )

    logs = response.json()

    return render(
        request,
        "mileage/history.html",
        {
            "logs": logs
        }
    )

def workorder_list(request):

    response = api_get(
        "workorders/",
        request.access_token
    )

    workorders = response.json()

    return render(
        request,
        "workorders/list.html",
        {
            "workorders":
            workorders
        }
    )

def workorder_detail(
    request,
    workorder_id
):

    response = api_get(
        f"workorders/{workorder_id}/",
        request.access_token
    )

    workorder = response.json()

    return render(
        request,
        "workorders/detail.html",
        {
            "workorder":
            workorder
        }
    )

def complete_workorder(
    request,
    workorder_id
):

    api_post(
        f"workorders/{workorder_id}/complete/",
        request.access_token,
        {}
    )

    return redirect(
        "workorder-list"
    )

def create_asset(request):

    form = AssetForm()

    if request.method == "POST":

        form = AssetForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            data = form.cleaned_data.copy()

            photo = request.FILES.get(
                "photo"
            )

            data.pop(
                "photo",
                None
            )

            for key, value in data.items():

                if value is None:

                    data[key] = ""

                else:

                    data[key] = str(value)

            files = {}

            if photo:

                files["photo"] = (
                    photo.name,
                    photo,
                    photo.content_type
                )

            response = api_post_file(
                "assets/",
                request.access_token,
                data,
                files
            )

            print(
                "STATUS:",
                response.status_code
            )

            print(
                "BODY:",
                response.text
            )

            if response.status_code in [200, 201]:

                return redirect(
                    "asset-list"
                )

            return HttpResponse(
                f"""
                Asset Creation Failed

                <br><br>

                Status:
                {response.status_code}

                <br><br>

                {response.text}
                """
            )

    return render(
        request,
        "assets/create_asset.html",
        {
            "form": form
        }
    )
def edit_asset(
    request,
    asset_id
):

    response = api_get(
        f"assets/{asset_id}/",
        request.access_token
    )

    if response.status_code != 200:

        return HttpResponse(
            f"""
            Failed to load asset.

            <br><br>

            Status:
            {response.status_code}

            <br><br>

            {response.text}
            """
        )

    asset = response.json()

    if request.method == "POST":

        form = AssetForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            data = (
                form.cleaned_data.copy()
            )

            photo = request.FILES.get(
                "photo"
            )

            # Remove photo from regular fields
            data.pop(
                "photo",
                None
            )

            # Convert values for multipart form upload
            for key, value in data.items():

                if value is None:

                    data[key] = ""

                else:

                    data[key] = str(
                        value
                    )

            files = {}

            if photo:

                files["photo"] = (
                    photo.name,
                    photo,
                    photo.content_type
                )

            update_response = (
                api_put_file(
                    f"assets/{asset_id}/",
                    request.access_token,
                    data,
                    files
                )
            )

            print(
                "STATUS:",
                update_response.status_code
            )

            print(
                "BODY:",
                update_response.text
            )

            if (
                update_response.status_code
                in [200, 202]
            ):

                return redirect(
                    "asset-detail",
                    asset_id=asset_id
                )

            return HttpResponse(
                f"""
                Update Failed

                <br><br>

                Status:
                {update_response.status_code}

                <br><br>

                {update_response.text}
                """
            )

    else:

        form = AssetForm(
            initial=asset
        )

    return render(
        request,
        "assets/edit_asset.html",
        {
            "form": form,
            "asset": asset
        }
    )
def delete_asset(
    request,
    asset_id
):

    if request.user_role != "MANAGER":
        return redirect("dashboard")

    api_delete(
        f"assets/{asset_id}/",
        request.access_token
    )

    return redirect(
        "asset-list"
    )

def create_user(request):

    if request.user_role != "MANAGER":
        return redirect("dashboard")

    form = UserForm()

    if request.method == "POST":

        form = UserForm(request.POST)

        if form.is_valid():

            api_post(
                "users/",
                request.access_token,
                form.cleaned_data
            )

            return redirect(
                "dashboard"
            )

    return render(
        request,
        "users/create.html",
        {
            "form": form
        }
    )

def asset_report(request):

    response = api_get(
        "assets/",
        request.access_token
    )

    assets = response.json()

    return render(
        request,
        "reports/assets.html",
        {
            "assets": assets
        }
    )

def maintenance_report(
    request
):

    response = api_get(
        "requests/",
        request.access_token
    )

    requests_data = (
        response.json()
    )

    return render(
        request,
        "reports/maintenance.html",
        {
            "requests":
            requests_data
        }
    )

def workorder_report(
    request
):

    response = api_get(
        "workorders/",
        request.access_token
    )

    workorders = (
        response.json()
    )

    return render(
        request,
        "reports/workorders.html",
        {
            "workorders":
            workorders
        }
    )

def user_list(request):

    response = api_get(
        "users/",
        request.access_token
    )

    users = response.json()

    return render(
        request,
        "users/user_list.html",
        {
            "users": users
        }
    )

def create_user(request):

    form = UserForm()

    if request.method == "POST":

        form = UserForm(request.POST)

        if form.is_valid():

            api_post(
                "users/",
                request.access_token,
                form.cleaned_data
            )

            return redirect(
                "user-list"
            )

    return render(
        request,
        "users/create_user.html",
        {
            "form": form
        }
    )

def edit_user(
    request,
    user_id
):

    response = api_get(
        f"users/{user_id}/",
        request.access_token
    )

    user_data = response.json()

    form = UserForm(
        initial=user_data
    )

    if request.method == "POST":

        form = UserForm(request.POST)

        if form.is_valid():

            api_put(
                f"users/{user_id}/",
                request.access_token,
                form.cleaned_data
            )

            return redirect(
                "user-list"
            )

    return render(
        request,
        "users/edit_user.html",
        {
            "form": form
        }
    )

def delete_user(
    request,
    user_id
):

    if request.method == "POST":

        api_delete(
            f"users/{user_id}/",
            request.access_token
        )

        return redirect(
            "user-list"
        )

    return render(
        request,
        "users/delete_user.html"
    )

def manager_requests(request):

    response = api_get(
        "requests/",
        request.access_token
    )

    requests_data = response.json()

    return render(
        request,
        "requests/manager_requests.html",
        {
            "requests":
            requests_data
        }
    )
def approve_request(
    request,
    request_id
):

    api_post(
        f"requests/{request_id}/approve/",
        request.access_token,
        {}
    )

    return redirect(
        "manager-requests"
    )

def reject_request(
    request,
    request_id
):

    api_post(
        f"requests/{request_id}/reject/",
        request.access_token,
        {}
    )

    return redirect(
        "manager-requests"
    )

def asset_report(request):

    if request.user_role == "STAFF":

        return redirect("dashboard")

    response = api_get(
        "reports/assets/",
        request.access_token
    )

    return render(
        request,
        "reports/asset_report.html",
        {
            "report":
            response.json()
        }
    )

def maintenance_report(request):

    if request.user_role == "STAFF":

        return redirect("dashboard")

    response = api_get(
        "reports/maintenance/",
        request.access_token
    )

    return render(
        request,
        "reports/maintenance_report.html",
        {
            "report":
            response.json()
        }
    )

def workorder_report(request):

    if request.user_role == "STAFF":

        return redirect("dashboard")

    response = api_get(
        "reports/workorders/",
        request.access_token
    )

    return render(
        request,
        "reports/workorder_report.html",
        {
            "report":
            response.json()
        }
    )

def mileage_report(request):

    if request.user_role == "STAFF":

        return redirect("dashboard")

    response = api_get(
        "reports/mileage/",
        request.access_token
    )

    return render(
        request,
        "reports/mileage_report.html",
        {
            "report":
            response.json()
        }
    )

from django.shortcuts import (
    render,
    redirect
)

from django.contrib import messages

from .services import (
    api_get,
    api_patch
)

from .forms import (
    AssetAssignmentForm
)


def assign_asset_view(
    request,
    asset_id
):

    token = request.session.get(
        "access_token"
    )

    asset_response = api_get(
        f"assets/{asset_id}/",
        token
    )

    if asset_response.status_code != 200:

        messages.error(
            request,
            "Asset not found."
        )

        return redirect(
            "asset-list"
        )

    asset = asset_response.json()

    users_response = api_get(
        "users/",
        token
    )

    users = []

    if users_response.status_code == 200:

        users = [
            (
                user["id"],
                f'{user["username"]} ({user["role"]})'
            )
            for user in users_response.json()
            if user["role"] == "STAFF"
        ]

    if request.method == "POST":

        form = AssetAssignmentForm(
            request.POST,
            users=users
        )

        if form.is_valid():

            response = api_patch(
                f"assets/{asset_id}/assign/",
                token,
                {
                    "user_id":
                    form.cleaned_data[
                        "assigned_to"
                    ]
                }
            )

            if response.status_code == 200:

                messages.success(
                    request,
                    "Asset assigned successfully."
                )

                return redirect(
                    "asset-list"
                )

            messages.error(
                request,
                "Assignment failed."
            )

    else:

        form = AssetAssignmentForm(
            users=users
        )

    return render(
        request,
        "assets/assign_asset.html",
        {
            "asset": asset,
            "form": form,
        }
    )

def audit_log_list_view(request):

    token = request.session.get(
        "access_token"
    )

    response = api_get(
        "audit-logs/",
        token
    )

    if response.status_code != 200:

        messages.error(
            request,
            "Unable to load audit logs."
        )


    logs = response.json()

    action = request.GET.get(
        "action",
        ""
    )

    model_name = request.GET.get(
        "model_name",
        ""
    )

    search = request.GET.get(
        "q",
        ""
    )

    if action:

        logs = [
            log
            for log in logs
            if log["action"] == action
        ]

    if model_name:

        logs = [
            log
            for log in logs
            if log["model_name"] == model_name
        ]

    if search:

        logs = [
            log
            for log in logs
            if (
                search.lower()
                in str(log).lower()
            )
        ]

    paginator = Paginator(
        logs,
        15
    )

    page_number = request.GET.get(
        "page"
    )

    logs = paginator.get_page(
        page_number
    )

    return render(
        request,
        "audit_logs/audit_log_list.html",
        {
            "logs": logs,
            "selected_action": action,
            "selected_model": model_name,
        }
    )


from django.contrib.auth.decorators import login_required



@login_required
def workorder_list_view(request):

    token = request.session.get(
        "access_token"
    )

    response = api_get(
        "workorders/",
        token
    )

    workorders = []

    if response.status_code == 200:

        workorders = response.json()

    return render(
        request,
        "workorders/list.html",
        {
            "workorders": workorders
        }
    )

def bulk_assign_assets_view(
    request
):

    token = request.session.get(
        "access_token"
    )

    users_response = api_get(
        "users/",
        token
    )

    assets_response = api_get(
        "assets/",
        token
    )

    users = []

    assets = []

    if users_response.status_code == 200:

        users = [
            (
                user["id"],
                user["username"]
            )
            for user in users_response.json()
            if user["role"] == "STAFF"
        ]

    if assets_response.status_code == 200:

        assets = [
            (
                asset["id"],
                f'{asset["asset_code"]} - {asset["name"]}'
            )
            for asset in assets_response.json()
        ]

    if request.method == "POST":

        form = BulkAssetAssignmentForm(
            request.POST,
            users=users,
            assets=assets
        )

        if form.is_valid():

            response = api_post(
                "assets/bulk_assign/",
                token,
                {
                    "ids": [
                        int(x)
                        for x in form.cleaned_data[
                            "asset_ids"
                        ]
                    ],
                    "user_id":
                    int(
                        form.cleaned_data[
                            "assigned_to"
                        ]
                    )
                }
            )

            if response.status_code == 200:

                messages.success(
                    request,
                    (
                        f'{response.json()["assigned"]} '
                        'assets assigned.'
                    )
                )

                return redirect(
                    "asset-list"
                )

    else:

        form = BulkAssetAssignmentForm(
            users=users,
            assets=assets
        )

    return render(
        request,
        "assets/bulk_assign.html",
        {
            "form": form
        }
    )

def test_backend(request):
    return HttpResponse(settings.BACKEND_API_URL)