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


def home_view(request):
    return render(request, 'home.html')

def about_view(request):
    return render(request, 'pages/about.html')

def sodosso_view(request):
    return render(request, 'pages/sodosso-list.html')

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



# ============= Template Views =============
def member_list_view(request):
    """
    Traditional Django template view for member list
    """
    members = Member.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        members = members.filter(
            Q(name__icontains=search_query) |
            Q(role__icontains=search_query) |
            Q(area__icontains=search_query) |
            Q(bio__icontains=search_query)
        )
    
    # Role filter
    role_filter = request.GET.get('role', '')
    if role_filter:
        members = members.filter(role=role_filter)
    
    # Pagination
    paginator = Paginator(members, 8)  # 8 members per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'members': page_obj,
        'search_query': search_query,
        'role_filter': role_filter,
        'role_choices': Member.ROLE_CHOICES,
    }
    return render(request, 'members/member_list.html', context)

def member_detail_view(request, pk):
    """
    Detail view for a single member
    """
    member = get_object_or_404(Member, pk=pk, is_active=True)
    context = {'member': member}
    return render(request, 'members/member_detail.html', context)


# ============= API Views =============
class MemberViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for Member CRUD operations
    
    Endpoints:
    - GET /api/members/ - List all members
    - POST /api/members/ - Create new member
    - GET /api/members/{id}/ - Retrieve member detail
    - PUT /api/members/{id}/ - Update member
    - PATCH /api/members/{id}/ - Partial update
    - DELETE /api/members/{id}/ - Delete member
    - GET /api/members/by_role/?role=President - Filter by role
    """
    queryset = Member.objects.filter(is_active=True)
    permission_classes = [AllowAny]  # Change as needed
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'role', 'area', 'bio']
    ordering_fields = ['name', 'role', 'joined_date']
    ordering = ['role', 'name']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return MemberListSerializer
        elif self.action == 'retrieve':
            return MemberDetailSerializer
        return MemberSerializer
    
    def get_queryset(self):
        """
        Override to add custom filtering
        """
        queryset = super().get_queryset()
        
        # Filter by role
        role = self.request.query_params.get('role', None)
        if role:
            queryset = queryset.filter(role=role)
        
        # Filter by area
        area = self.request.query_params.get('area', None)
        if area:
            queryset = queryset.filter(area__icontains=area)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def by_role(self, request):
        """
        Custom endpoint: /api/members/by_role/?role=President
        """
        role = request.query_params.get('role', None)
        if not role:
            return Response(
                {'error': 'Role parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        members = self.get_queryset().filter(role=role)
        serializer = self.get_serializer(members, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def roles(self, request):
        """
        Get all available roles
        Endpoint: /api/members/roles/
        """
        roles = [{'value': choice[0], 'label': choice[1]} 
                for choice in Member.ROLE_CHOICES]
        return Response(roles)
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """
        Toggle member active status
        Endpoint: POST /api/members/{id}/toggle_active/
        """
        member = self.get_object()
        member.is_active = not member.is_active
        member.save()
        serializer = self.get_serializer(member)
        return Response(serializer.data)