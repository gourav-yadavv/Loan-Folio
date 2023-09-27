from django.urls import path
from . import views

urlpatterns = [
    path('api/register-user/', views.register_user, name='register_user'),
    path('api/apply-loan/', views.apply_loan, name='apply_loan'),
    path('api/make-payment/', views.make_payment, name='make_payment'),
    path('api/get-statement/', views.get_statement, name='get_statement'),
    path('all-loans/', views.all_loans, name='all_loans'),
]
