from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('services/', views.services_view, name='services'),
    path('portfolio/', views.portfolio_view, name='portfolio'),
    path('ownership/', views.ownership_view, name='ownership'),
    path('blog/', views.blog_view, name='blog-products'),
    path('contact/', views.contact_view, name='contact'),
]
