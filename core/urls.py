from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),

     path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    path(
    "dashboard/",
    views.dashboard,
    name="dashboard"
),

path(
    "assets/",
    views.asset_list,
    name="asset-list"
),

path(
    "assets/<int:asset_id>/",
    views.asset_detail,
    name="asset-detail"
),

path(
    "requests/",
    views.my_requests,
    name="my-requests"
),

path(
    "requests/create/",
    views.create_request,
    name="create-request"
),

path(
    "workorders/",
    views.workorder_list,
    name="workorder-list"
),

path(
    "workorders/<int:workorder_id>/",
    views.workorder_detail,
    name="workorder-detail"
),

path(
    "workorders/<int:workorder_id>/complete/",
    views.complete_workorder,
    name="complete-workorder"
),

path(
    "mileage/",
    views.mileage_history,
    name="mileage-history"
),

path(
    "mileage/submit/",
    views.submit_mileage,
    name="submit-mileage"
),

path(
    "assets/create/",
    views.create_asset,
    name="create-asset"
),

path(
    "assets/<int:asset_id>/edit/",
    views.edit_asset,
    name="edit-asset"
),

path(
    "assets/<int:asset_id>/delete/",
    views.delete_asset,
    name="delete-asset"
),

# User Management

path(
    "users/",
    views.user_list,
    name="user-list"
),

path(
    "users/create/",
    views.create_user,
    name="create-user"
),

path(
    "users/<int:user_id>/edit/",
    views.edit_user,
    name="edit-user"
),

path(
    "users/<int:user_id>/delete/",
    views.delete_user,
    name="delete-user"
),

path(
    "manager/requests/",
    views.manager_requests,
    name="manager-requests"
),

path(
    "manager/requests/<int:request_id>/approve/",
    views.approve_request,
    name="approve-request"
),

path(
    "manager/requests/<int:request_id>/reject/",
    views.reject_request,
    name="reject-request"
),

path(
    "reports/assets/",
    views.asset_report,
    name="asset-report"
),

path(
    "reports/maintenance/",
    views.maintenance_report,
    name="maintenance-report"
),

path(
    "reports/workorders/",
    views.workorder_report,
    name="workorder-report"
),

path(
    "reports/mileage/",
    views.mileage_report,
    name="mileage-report"
),

path(
    "assets/<int:asset_id>/assign/",
    views.assign_asset_view,
    name="assign-asset"
),

path(
    "audit-logs/",
    views.audit_log_list_view,
    name="audit-log-list"
),
path(
    "workorders/",
    views.workorder_list_view,
    name="workorder-list"
),
path(
    "assets/bulk-assign/",
    views.bulk_assign_assets_view,
    name="bulk-assign-assets"
),


]