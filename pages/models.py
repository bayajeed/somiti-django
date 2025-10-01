from django.db import models
from django.core.validators import RegexValidator

class Member(models.Model):
    """
    Member model for Somiti/Committee members
    """
    ROLE_CHOICES = [
        ('President', 'President'),
        ('Secretary', 'Secretary'),
        ('Treasurer', 'Treasurer'),
        ('Committee', 'Committee'),
        ('Member', 'Member'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200, verbose_name='সদস্যের নাম')
    role = models.CharField(
        max_length=50, 
        choices=ROLE_CHOICES, 
        default='Member',
        verbose_name='পদবি'
    )
    area = models.CharField(max_length=100, verbose_name='এলাকা')
    
    # Contact Information
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        verbose_name='ফোন নম্বর'
    )
    email = models.EmailField(verbose_name='ইমেইল')
    
    # Additional Information
    bio = models.TextField(blank=True, verbose_name='সংক্ষিপ্ত পরিচয়')
    image = models.ImageField(
        upload_to='members/', 
        blank=True, 
        null=True,
        verbose_name='ছবি'
    )
    
    # Metadata
    joined_date = models.DateField(auto_now_add=True, verbose_name='যোগদানের তারিখ')
    is_active = models.BooleanField(default=True, verbose_name='সক্রিয়')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['role', 'name']
        verbose_name = 'সদস্য'
        verbose_name_plural = 'সদস্যগণ'
    
    def __str__(self):
        return f"{self.name} - {self.role}"
    
    def get_avatar_url(self):
        """Return avatar URL or default image"""
        if self.image:
            return self.image.url
        return 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?q=80&w=200&h=200&auto=format&fit=crop&crop=faces'