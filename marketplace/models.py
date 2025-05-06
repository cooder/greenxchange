from django.db import models
from django.utils import timezone


# Create your models here.


class Energy_Type(models.Model):
    name  =  models.CharField(max_length=200, unique=True)
    created_on   =  models.DateTimeField(auto_now_add=True, editable=False)
    updated_on   =  models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Energy(models.Model):
    energy_type =  models.ForeignKey(Energy_Type, on_delete=models.CASCADE, related_name='energies')
    seller_id   =  models.PositiveIntegerField()
    quantity    =  models.PositiveIntegerField(default=0)
    price       =  models.DecimalField(max_digits=10, decimal_places=2)
    unit        =  models.CharField(max_length=15, blank=True, null=True)
    status      = models.CharField(max_length=15, choices=[
                     ('available', 'Available'),
                     ('expired', 'Expired'),
                     ('sold', 'Sold')
                     ], default='available')
    expiry_date =  models.DateTimeField()
    created_on  =  models.DateTimeField(auto_now_add=True, editable=False)
    updated_on  =  models.DateTimeField(auto_now=True)
    
    def is_expired(self):
        return timezone.now() > self.expiry_date

    def save(self, *args, **kwargs):
        if self.is_expired():
            self.status = 'expired'
        else:
            if self.quantity>0:
                self.status='available'
            if self.quantity==0:
                self.status='sold'
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.energy_type.name} - Seller {self.seller_id}"

class EnergyOffer(models.Model):
    energy_id = models.ForeignKey(Energy, on_delete=models.CASCADE, related_name='offers')
    buyer_id = models.PositiveIntegerField()
    offered_quantity = models.PositiveIntegerField()
    offered_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ], default='pending')
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Offer by Buyer {self.buyer_id} on Energy {self.energy.id}"