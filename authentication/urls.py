from django.urls import path

from django.contrib.auth import views
from authentication.views.login import OrganisationLoginView

from authentication.views.register import ActivateView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("activate/<uidb64>/<token>/", ActivateView.as_view(), name="activate"),
    path('user/login/', OrganisationLoginView.as_view(), name='login'),

    path('user/logout/', views.LogoutView.as_view(), name='logout'),
    path('user/password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('user/password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('user/password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('user/password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('user/reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('user/reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete')
]