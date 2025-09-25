from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')

def about_view(request):
    return render(request, 'pages/about.html')

def services_view(request):
    return render(request, 'pages/services.html')

def portfolio_view(request):
    return render(request, 'pages/portfolio.html')

def ownership_view(request):
    return render(request, 'pages/ownership.html')

def blog_view(request):
    return render(request, 'pages/blog/blog-products.html')

def contact_view(request):
    return render(request, 'pages/contact.html')

def history_view(request):
    return render(request, 'pages/history.html')
def mission_vision_view(request):
    return render(request, 'pages/mission_vision.html')
def activities_view(request):
    return render(request, 'pages/activities.html')
def member_list_view(request):
    return render(request, 'pages/member_list.html')
def membership_rules_view(request):
    return render(request, 'pages/membership_rules.html')
def news_events_view(request):
    return render(request, 'pages/news_events.html')
def latest_news_view(request):
    return render(request, 'pages/latest_news.html')
def upcoming_events_view(request):
    return render(request, 'pages/upcoming_events.html')
def notice_board_view(request):
    return render(request, 'pages/notice_board.html')
def gallery_view(request):
    return render(request, 'pages/gallery.html')
# Add more view functions as needed
