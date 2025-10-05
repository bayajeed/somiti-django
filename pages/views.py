# pages/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Member
from .serializers import (
    MemberSerializer, 
    MemberListSerializer, 
    MemberDetailSerializer
)

# ==============================================
# ========== সাধারণ টেমপ্লেট ভিউ (Template Views) ===========
# ==============================================

# --- প্রধান পেজগুলোর জন্য ভিউ --- 

def home_view(request):
    """ হোমপেজ রেন্ডার করে। """
    return render(request, 'home.html')

def about_view(request):
    """ About পেজ রেন্ডার করে। """
    return render(request, 'pages/about.html')

def services_view(request):
    """ Services পেজ রেন্ডার করে। """
    return render(request, 'pages/services.html')

def portfolio_view(request):
    """ Portfolio পেজ রেন্ডার করে। """
    return render(request, 'pages/portfolio.html')

def ownership_view(request):
    """ Ownership পেজ রেন্ডার করে। """
    return render(request, 'pages/ownership.html')

def blog_view(request):
    """ Blog পেজ রেন্ডার করে। """
    return render(request, 'pages/blog/blog-products.html')

def contact_view(request):
    """ Contact পেজ রেন্ডার করে। """
    return render(request, 'pages/contact.html')


# --- সদস্যদের তালিকা এবং বিস্তারিত তথ্যের জন্য ভিউ --- 

def sodosso_view(request):
    """
    সদস্যদের তালিকা দেখানোর জন্য এই ভিউ ব্যবহার করা হয়।
    এতে সার্চ, ফিল্টারিং এবং পেজিনেশন কার্যকারিতা অন্তর্ভুক্ত রয়েছে।
    """
    # শুধুমাত্র সক্রিয় সদস্যদের দেখানো হবে।
    members = Member.objects.filter(is_active=True)
    
    # সার্চ কার্যকারিতা: নাম, পদবি, এলাকা বা বায়ো দিয়ে সার্চ করা যাবে।
    search_query = request.GET.get('search', '')
    if search_query:
        members = members.filter(
            Q(name__icontains=search_query) |
            Q(role__icontains=search_query) |
            Q(area__icontains=search_query) |
            Q(bio__icontains=search_query)
        )
    
    # পদবি অনুযায়ী ফিল্টারিং।
    role_filter = request.GET.get('role', '')
    if role_filter:
        members = members.filter(role=role_filter)

    # members = members.order_by('id')  # আইডি অনুযায়ী সাজানো হবে।
    # members = members.order_by('role', 'id', 'name')  # আইডি, পদবি এবং নাম অনুযায়ী সাজানো হবে।

    # পেজিনেশন: প্রতি পেজে ৮ জন সদস্য দেখানো হবে।
    paginator = Paginator(members, 8)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'members': page_obj, # পেজিনেটেড সদস্য তালিকা
        'search_query': search_query, # সার্চের জন্য ব্যবহৃত শব্দ
        'role_filter': role_filter, # ফিল্টারিংয়ের জন্য ব্যবহৃত পদবি
        'role_choices': Member.ROLE_CHOICES, # ফিল্টার ড্রপডাউনের জন্য পদবি তালিকা
    }
    return render(request, 'pages/sodosso-list.html', context)

def member_detail_view(request, pk):
    """
    একজন নির্দিষ্ট সদস্যের বিস্তারিত তথ্য দেখানোর জন্য এই ভিউ।
    """
    member = get_object_or_404(Member, pk=pk, is_active=True)
    context = {'member': member}
    return render(request, 'pages/sodosso-list.html', context) # Note: আপনি এখানেও sodosso-list.html ব্যবহার করেছেন।


# ====================================================
# ========== API ভিউসেট (DRF API ViewSet) ============
# ====================================================

class MemberViewSet(viewsets.ModelViewSet):
    """
    সদস্যদের জন্য একটি সম্পূর্ণ CRUD (Create, Read, Update, Delete) API।
    DRF (Django Rest Framework) ব্যবহার করে এটি তৈরি করা হয়েছে।

    সাধারণ এন্ডপয়েন্টগুলো:
    - GET /api/members/ -> সকল সদস্যের তালিকা ( সংক্ষিপ্ত )
    - POST /api/members/ -> নতুন সদস্য তৈরি
    - GET /api/members/{id}/ -> নির্দিষ্ট সদস্যের বিস্তারিত তথ্য
    - PUT /api/members/{id}/ -> সদস্যের তথ্য আপডেট
    - DELETE /api/members/{id}/ -> সদস্যকে ডিলেট
    """
    queryset = Member.objects.filter(is_active=True)
    permission_classes = [AllowAny]  # API অ্যাক্সেসের জন্য অনুমতি ( আপাতত সবার জন্য খোলা )
    filter_backends = [filters.SearchFilter, filters.OrderingFilter] # সার্চ এবং অর্ডারিং সুবিধা যোগ করা হয়েছে
    search_fields = ['name', 'role', 'area', 'bio'] # কোন কোন ফিল্ডে সার্চ করা যাবে
    ordering_fields = ['name', 'role', 'joined_date'] # কোন কোন ফিল্ড অনুযায়ী সাজানো যাবে
    ordering = ['role', 'name'] # ডিফল্ট অর্ডারিং
    
    def get_serializer_class(self):
        """
        অ্যাকশন অনুযায়ী সঠিক সিরিয়ালাইজার ক্লাস রিটার্ন করে।
        - `list` অ্যাকশনের জন্য: `MemberListSerializer` (সংক্ষিপ্ত তথ্য)
        - `retrieve` অ্যাকশনের জন্য: `MemberDetailSerializer` (বিস্তারিত তথ্য)
        - অন্য সব অ্যাকশনের জন্য: `MemberSerializer` (সম্পূর্ণ তথ্য)
        """
        if self.action == 'list':
            return MemberListSerializer
        elif self.action == 'retrieve':
            return MemberDetailSerializer
        return MemberSerializer
    
    def get_queryset(self):
        """
        API অনুরোধ অনুযায়ী কোয়েরিসেট ফিল্টার করার জন্য এই মেথডটি ওভাররাইড করা হয়েছে।
        URL প্যারামিটার (e.g., `?role=President`) অনুযায়ী ফিল্টার করা যাবে।
        """
        queryset = super().get_queryset()
        
        # পদবি (`role`) অনুযায়ী ফিল্টার
        role = self.request.query_params.get('role', None)
        if role:
            queryset = queryset.filter(role=role)
        
        # এলাকা (`area`) অনুযায়ী ফিল্টার
        area = self.request.query_params.get('area', None)
        if area:
            queryset = queryset.filter(area__icontains=area)
        
        return queryset
    
    # --- কাস্টম API এন্ডপয়েন্ট --- 

    @action(detail=False, methods=['get'], url_path='by-role')
    def by_role(self, request):
        """
        পদবি অনুযায়ী সদস্যদের তালিকা পাওয়ার জন্য একটি কাস্টম এন্ডপয়েন্ট।
        এন্ডপয়েন্ট: GET /api/members/by-role/?role=President
        """
        role = request.query_params.get('role', None)
        if not role:
            return Response(
                {'error': 'Role parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        members = self.get_queryset().filter(role=role)
        # `get_serializer` ব্যবহার করে সঠিক সিরিয়ালাইজার পাওয়া যায়।
        serializer = self.get_serializer(members, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get']) 
    def roles(self, request):
        """
        সিস্টেমে উপলব্ধ সকল পদবি তালিকা পাওয়ার জন্য একটি এন্ডপয়েন্ট।
        এন্ডপয়েন্ট: GET /api/members/roles/
        """
        roles = [{'value': choice[0], 'label': choice[1]} for choice in Member.ROLE_CHOICES]
        return Response(roles)
    
    @action(detail=True, methods=['post'], url_path='toggle-active')
    def toggle_active(self, request, pk=None):
        """
        একজন সদস্যের `is_active` স্ট্যাটাস পরিবর্তন (toggle) করার জন্য।
        এন্ডপয়েন্ট: POST /api/members/{id}/toggle-active/
        """
        member = self.get_object()
        member.is_active = not member.is_active
        member.save()
        serializer = self.get_serializer(member)
        return Response(serializer.data)
