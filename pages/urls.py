# pages/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# অ্যাপের নাম সেট করা হয়েছে, যাতে টেমপ্লেটে URL সহজে কল করা যায়।
# যেমন: {% url 'pages:home' %} 
app_name = 'pages'

# =======================================
# ========== API URL রাউটার ============
# =======================================

# DRF-এর DefaultRouter ব্যবহার করে API ভিউসেটের জন্য URL স্বয়ংক্রিয়ভাবে তৈরি করা হয়।
# এটি list, create, retrieve, update, destroy ইত্যাদি এন্ডপয়েন্ট তৈরি করবে।
router = DefaultRouter()
router.register(r'members', views.MemberViewSet, basename='member-api')

# =======================================
# ========== URL প্যাটার্নস ============
# =======================================

urlpatterns = [
    # --- সাধারণ পেজের জন্য URL --- 
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('services/', views.services_view, name='services'),
    path('portfolio/', views.portfolio_view, name='portfolio'),
    path('ownership/', views.ownership_view, name='ownership'),
    path('blog/', views.blog_view, name='blog-products'),
    path('contact/', views.contact_view, name='contact'),

    # --- সদস্য সম্পর্কিত টেমপ্লেট ভিউয়ের জন্য URL ---
    # সদস্যদের তালিকা দেখানোর জন্য। যেমন: /sodosso/
    path('sodosso/', views.sodosso_view, name='sodosso'), 
    
    # নির্দিষ্ট সদস্যের বিস্তারিত তথ্য দেখানোর জন্য। যেমন: /sodosso/5/
    path('sodosso/<int:pk>/', views.member_detail_view, name='sodosso-detail'),

    # --- API ভিউয়ের জন্য URL ---
    # /api/ এর অধীনে সকল API এন্ডপয়েন্ট অন্তর্ভুক্ত করা হয়েছে।
    # যেমন: /api/members/, /api/members/1/, ইত্যাদি।
    path('api/', include(router.urls)),
]

# নিচের কমেন্ট করা URL গুলো ভবিষ্যতে প্রয়োজন হলে ব্যবহার করতে পারেন।
# urlpatterns += [
#     path('history/', views.history_view, name='history'),
#     path('mission-vision/', views.mission_vision_view, name='mission_vision'),
#     path('activities/', views.activities_view, name='activities'),
#     path('membership-rules/', views.membership_rules_view, name='membership_rules'),
#     path('news-events/', views.news_events_view, name='news_events'),
#     path('notice-board/', views.notice_board_view, name='notice_board'),
#     path('gallery/', views.gallery_view, name='gallery'),
# ]