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
    # path('history/', views.history_view, name='history'),
    # path('mission-vision/', views.mission_vision_view, name='mission_vision '),
    # path('activities/', views.activities_view, name='activities'),
    # path('member-list/', views.member_list_view, name='member_list'),
    # path('membership-rules/', views.membership_rules_view, name='membership_rules'),
    # path('news-events/', views.news_events_view, name='news_events'),
    # path('latest-news/', views.latest_news_view, name='latest_news'),
    # path('upcoming-events/', views.upcoming_events_view, name='upcoming_events'),
    # path('notice-board/', views.notice_board_view, name='notice_board'),
    # path('gallery/', views.gallery_view, name='gallery'),

]
