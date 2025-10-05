# pages/models.py
from datetime import datetime
from django.db import models
from django.core.validators import RegexValidator

from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
import os

# সদস্যের ইমেজ আপলোড পাথ কাস্টমাইজ করার জন্য ফাংশন
def member_image_upload_path(instance, filename):
    # শুধু ফাইলের নাম রেখে দিচ্ছি, যাতে আগের path যোগ না হয়
    filename = os.path.basename(filename)
    # এখন শুধু এইরকম path হবে: members/<role>/<filename>
    return f"members/{instance.role}/{filename}"

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

    # === Additional Information ===
    bio = models.TextField(blank=True, verbose_name='Short Description') # সংক্ষিপ্ত বর্ণনা (অপশনাল)
    image = models.ImageField(
        upload_to=member_image_upload_path,
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
        ordering = ['id' ,'role', 'name']
        verbose_name = 'Member'
        verbose_name_plural = 'Members'

    def __str__(self):
        """
        অবজেক্টকে স্ট্রিং হিসেবে প্রকাশ করার জন্য। 
        অ্যাডমিন প্যানেল এবং অন্যান্য জায়গায় সদস্যের নাম ও পদবি দেখানো হবে।
        """
        return f"{self.id} - {self.name} - {self.role}"
    
    def get_avatar_url(self):
        """
        সদস্যের প্রোফাইল ছবি থাকলে তার URL প্রদান করে, অন্যথায় একটি ডিফল্ট ছবি প্রদান করে।
        """
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        # একটি ডিফল্ট অ্যাভাটার ইমেজ প্রদান করা হয়েছে
        return 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?q=80&w=200&h=200&auto=format&fit=crop&crop=faces'
    
    # count of all active members


    # ইমেজ কনভার্সন এবং সাইজ কমানোর জন্য save মেথড ওভাররাইড করা হয়েছে
    def save(self, *args, **kwargs):
        # প্রথমে instance টি normal ভাবে save করুন
        super().save(*args, **kwargs)

        # এখন image থাকলে কনভার্ট করুন
        if self.image:
            img_path = self.image.path
            img = Image.open(img_path)

            # WEBP ফরম্যাটে কনভার্ট করা
            webp_io = BytesIO()
            img.save(webp_io, format='WEBP', quality=85)

            # filename rename: username + timestamp
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            username = self.name.replace(" ", "_")
            new_filename = f"{username}_{timestamp}.webp"

            # final path: members/<role>/<filename>
            upload_path = f"members/{self.role}/{new_filename}"

            # image save
            self.image.save(upload_path, ContentFile(webp_io.getvalue()), save=False)

            # আগের ফাইল ডিলিট (optional)
            try:
                if os.path.exists(img_path):
                    os.remove(img_path)
            except Exception:
                pass

            super().save(*args, **kwargs)

