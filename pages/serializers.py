# pages/serializers.py
from rest_framework import serializers
from .models import Member

class MemberSerializer(serializers.ModelSerializer):
    """
    Serializer for Member model - used for API responses
    """
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Member
        fields = [
            'id', 'name', 'role', 'area', 'phone', 
            'email', 'bio', 'avatar_url', 'joined_date', 
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'joined_date']
    
    def get_avatar_url(self, obj):
        """Get avatar URL with request context"""
        request = self.context.get('request')
        avatar = obj.get_avatar_url()
        if avatar and request and not avatar.startswith('http'):
            return request.build_absolute_uri(avatar)
        return avatar

class MemberListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for member list views
    """
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Member
        fields = ['id', 'name', 'role', 'area', 'avatar_url']
    
    def get_avatar_url(self, obj):
        request = self.context.get('request')
        avatar = obj.get_avatar_url()
        if avatar and request and not avatar.startswith('http'):
            return request.build_absolute_uri(avatar)
        return avatar

class MemberDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for single member view
    """
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Member
        fields = '__all__'
    
    def get_avatar_url(self, obj):
        request = self.context.get('request')
        avatar = obj.get_avatar_url()
        if avatar and request and not avatar.startswith('http'):
            return request.build_absolute_uri(avatar)
        return avatar