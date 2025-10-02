# pages/serializers.py
from rest_framework import serializers
from .models import Member

class MemberSerializer(serializers.ModelSerializer):
    """
    `Member` মডেলের জন্য একটি সম্পূর্ণ সিরিয়ালাইজার। 
    API-এর মাধ্যমে সদস্য তৈরি (Create) এবং আপডেট (Update) করার জন্য এটি ব্যবহৃত হয়।
    এতে সদস্যের প্রায় সমস্ত তথ্য অন্তর্ভুক্ত থাকে।
    """
    # `get_avatar_url` মডেলের মেথড থেকে পাওয়া URL এখানে যুক্ত করা হয়েছে।
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Member
        # API-তে কোন কোন ফিল্ড দেখানো হবে তা এখানে নির্দিষ্ট করা হয়েছে।
        fields = [
            'id', 'name', 'role', 'area', 'phone', 
            'email', 'bio', 'avatar_url', 'joined_date', 
            'is_active', 'created_at', 'updated_at'
        ]
        # এই ফিল্ডগুলো শুধুমাত্র পড়া যাবে, এডিট করা যাবে না।
        read_only_fields = ['id', 'created_at', 'updated_at', 'joined_date']
    
    def get_avatar_url(self, obj):
        """
        সদস্যের ছবির সম্পূর্ণ URL তৈরি করে। 
        যদি ছবিটি আপলোড করা থাকে, তবে তার সম্পূর্ণ পাথ (e.g., http://.../media/...) প্রদান করে।
        """
        request = self.context.get('request')
        avatar = obj.get_avatar_url()
        # যদি avatar URL থাকে এবং request object থাকে এবং avatar 'http' দিয়ে শুরু না হয়,
        # তাহলে build_absolute_uri দিয়ে সম্পূর্ণ URL বানানো হয়।
        if avatar and request and not avatar.startswith('http'):
            return request.build_absolute_uri(avatar)
        # না হলে avatar  ফেরত দেওয়া হয়।
        return avatar

class MemberListSerializer(serializers.ModelSerializer):
    """
    সদস্যদের তালিকা দেখানোর জন্য একটি সংক্ষিপ্ত সিরিয়ালাইজার।
    API-এর `list` ভিউতে এটি ব্যবহার করা হয়, যাতে শুধুমাত্র প্রয়োজনীয় তথ্য (যেমন নাম, পদবি) লোড হয়।
    এর ফলে API রেসপন্স দ্রুত হয়।
    """
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Member
        # শুধুমাত্র তালিকা দেখানোর জন্য প্রয়োজনীয় ফিল্ডগুলো এখানে রাখা হয়েছে।
        fields = ['id', 'name', 'role', 'area', 'avatar_url']
    
    def get_avatar_url(self, obj):
        """
        ছবির সম্পূর্ণ URL তৈরি করে।
        """
        request = self.context.get('request')
        avatar = obj.get_avatar_url()
        if avatar and request and not avatar.startswith('http'):
            return request.build_absolute_uri(avatar)
        return avatar

class MemberDetailSerializer(serializers.ModelSerializer):
    """
    একজন নির্দিষ্ট সদস্যের বিস্তারিত তথ্য দেখানোর জন্য এই সিরিয়ালাইজারটি ব্যবহৃত হয়।
    API-এর `retrieve` (detail) ভিউতে এটি ব্যবহার করা হয়।
    `__all__` ব্যবহারের মাধ্যমে মডেলের সমস্ত ফিল্ড অন্তর্ভুক্ত করা হয়েছে।
    """
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Member
        fields = '__all__' # মডেলের সব ফিল্ড অন্তর্ভুক্ত করা হয়েছে।
    
    def get_avatar_url(self, obj):
        """
        ছবির সম্পূর্ণ URL তৈরি করে।
        """
        request = self.context.get('request')
        avatar = obj.get_avatar_url()
        if avatar and request and not avatar.startswith('http'):
            return request.build_absolute_uri(avatar)
        return avatar
