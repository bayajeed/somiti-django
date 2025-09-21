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
