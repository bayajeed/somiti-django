# pages/admin.py
from django.contrib import admin
from .models import Member

# Member মডেলটিকে অ্যাডমিন সাইটে রেজিস্টার করা হয়েছে এবং এর প্রদর্শন কাস্টমাইজ করা হয়েছে।
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    """
    অ্যাডমিন প্যানেলে `Member` মডেলের প্রদর্শন এবং কার্যকারিতা নিয়ন্ত্রণের জন্য এই ক্লাসটি তৈরি।
    """
    
    # --- তালিকা প্রদর্শনের কনফিগারেশন ---
    # অ্যাডমিন লিস্ট ভিউতে কোন কোন ফিল্ড দেখানো হবে।
    list_display = [
        'name', 
        'role', 
        'area', 
        'phone', 
        'is_active', 
        'joined_date'
    ]
    
    # ডান পাশের সাইডবারে ফিল্টার অপশন যোগ করা হয়েছে।
    list_filter = ['role', 'area', 'is_active', 'joined_date']
    
    # সার্চ বক্সের মাধ্যমে কোন কোন ফিল্ডে সার্চ করা যাবে।
    search_fields = ['name', 'phone', 'email', 'area']
    
    # তালিকা থেকে সরাসরি `is_active` ফিল্ডটি এডিট করার সুবিধা।
    list_editable = ['is_active']
    
    # প্রতি পেজে কতজন সদস্য দেখানো হবে।
    list_per_page = 25
    
    # --- ফরম প্রদর্শনের কনফিগারেশন ---
    # সদস্য যোগ বা এডিট করার পেজে ফিল্ডগুলোকে গ্রুপে ভাগ করে দেখানো হয়েছে।
    fieldsets = (
        ('মৌলিক তথ্য', {
            'fields': ('name', 'role', 'area', 'image')
        }),
        ('যোগাযোগের তথ্য', {
            'fields': ('phone', 'email')
        }),
        ('অতিরিক্ত তথ্য', {
            'fields': ('bio', 'is_active')
        }),
        ('মেটাডেটা (সিস্টেম তথ্য)', {
            'fields': ('joined_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)  # এই সেকশনটি ডিফল্টভাবে লুকানো থাকবে।
        }),
    )
    
    # যে ফিল্ডগুলো শুধুমাত্র পড়া যাবে, এডিট করা যাবে না।
    readonly_fields = ['joined_date', 'created_at', 'updated_at']
    
    # ডিফল্টভাবে তালিকাটি পদবি ও নাম অনুযায়ী সাজানো থাকবে।
    ordering = ['role', 'name']
    
    # --- কাস্টম অ্যাডমিন অ্যাকশন ---
    # অ্যাডমিন তালিকা থেকে একাধিক সদস্যকে একসাথে সক্রিয় বা নিষ্ক্রিয় করার জন্য।
    actions = ['activate_members', 'deactivate_members']
    
    def activate_members(self, request, queryset):
        """নির্বাচিত সদস্যদের সক্রিয় (Activate) করে।"""
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} জন সদস্যকে সফলভাবে সক্রিয় করা হয়েছে।')
    activate_members.short_description = 'নির্বাচিত সদস্যদের সক্রিয় করুন'
    
    def deactivate_members(self, request, queryset):
        """নির্বাচিত সদস্যদের নিষ্ক্রিয় (Deactivate) করে।"""
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} জন সদস্যকে সফলভাবে নিষ্ক্রিয় করা হয়েছে।')
    deactivate_members.short_description = 'নির্বাচিত সদস্যদের নিষ্ক্রিয় করুন'