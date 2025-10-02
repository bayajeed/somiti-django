# pages/models.py
from django.db import models
from django.core.validators import RegexValidator

class Member(models.Model):
    """
    সমিতি বা কমিটির সদস্যদের তথ্য সংরক্ষণ করার জন্য এই মডেলটি তৈরি করা হয়েছে।
    এতে সদস্যদের ব্যক্তিগত তথ্য, পদবি, যোগাযোগের বিবরণ এবং অন্যান্য প্রয়োজনীয় তথ্য অন্তর্ভুক্ত রয়েছে।
    """
    
    # সদস্যদের পদবি নির্ধারণের জন্য চয়েস ফিল্ড।
    ROLE_CHOICES = [
        ('President', 'President'),
        ('Secretary', 'Secretary'),
        ('Treasurer', 'Treasurer'),
        ('Committee', 'Committee'),
        ('Member', 'Member'),
    ]
    
    # === মৌলিক তথ্য ===
    name = models.CharField(max_length=200, verbose_name='Name') # সদস্যের পূর্ণ নাম
    role = models.CharField(
        max_length=50, 
        choices=ROLE_CHOICES, 
        default='Member',
        verbose_name='Role' # সদস্যের পদবি
    )
    area = models.CharField(max_length=100, verbose_name='Area') # সদস্যের এলাকা বা ওয়ার্ড
    
    # === যোগাযোগের তথ্য ===
    # ফোন নম্বরের ফরম্যাট যাচাই করার জন্য RegexValidator ব্যবহার করা হয়েছে।
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+8801900000000'. Up to 15 digits allowed."
    )
    phone = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        verbose_name='Phone' # ফোন নম্বর (ইন্টারন্যাশনাল ফরম্যাটে
    )
    email = models.EmailField(verbose_name='E-mail', blank=True, null=True) # ইমেইল অপশনাল করা হয়েছে
    
    # === অতিরিক্ত তথ্য ===
    bio = models.TextField(blank=True, verbose_name='সংক্ষিপ্ত পরিচয়')
    image = models.ImageField(
        upload_to='members/', 
        blank=True, 
        null=True,
        verbose_name='Image' # প্রোফাইল ছবি (অপশনাল)
    )
    
    # === মেটাডেটা ===
    joined_date = models.DateField(auto_now_add=True, verbose_name='Joining Date')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At') # তৈরির সময়
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At') # আপডেটের সময়
    
    class Meta:
        """
        মডেলের মেটা-অপশনস।
        - ordering: সদস্যদের তালিকা ডিফল্টভাবে 'role' এবং 'name' অনুযায়ী সাজানো থাকবে।
        - verbose_name: অ্যাডমিন প্যানেলে মডেলের সিঙ্গুলার নাম 'সদস্য' হিসেবে দেখাবে।
        - verbose_name_plural: অ্যাডমিন প্যানেলে মডেলের প্লুরাল নাম 'সদস্যগণ' হিসেবে দেখাবে।
        """
        ordering = ['role', 'name']
        verbose_name = 'সদস্য'
        verbose_name_plural = 'সদস্যগণ'
    
    def __str__(self):
        """
        অবজেক্টকে স্ট্রিং হিসেবে প্রকাশ করার জন্য। 
        অ্যাডমিন প্যানেল এবং অন্যান্য জায়গায় সদস্যের নাম ও পদবি দেখানো হবে।
        """
        return f"{self.name} - {self.role}"
    
    def get_avatar_url(self):
        """
        সদস্যের প্রোফাইল ছবি থাকলে তার URL প্রদান করে, অন্যথায় একটি ডিফল্ট ছবি প্রদান করে।
        """
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        # একটি ডিফল্ট অ্যাভাটার ইমেজ প্রদান করা হয়েছে
        return 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?q=80&w=200&h=200&auto=format&fit=crop&crop=faces'
