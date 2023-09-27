from django.contrib import admin
from django.urls import path,include
from Loans import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register_user/', views.register_user, name='register_user'),
    path('api/apply_loan/', views.apply_loan, name='apply_loan'),
    path('api/make_payment/', views.make_payment, name='make_payment'),
    path('api/get_statement/', views.get_statement, name='get_statement'),
    path('all-loans/',views.all_loans,name='all_loans')
]
