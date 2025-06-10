from django.db import models
from users.models import SecureCipherUser



# Create your models here.

class Transaction(models.Model):
    # What it does: Core transaction data
    user = models.ForeignKey(SecureCipherUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    recipient_account = models.CharField(max_length=50)
    
    # What it does: Cryptographic signatures
    sig_p = models.TextField()  # Paul's signature
    sig_s = models.TextField()  # Server's signature
    
    # What it does: Public keys used
    q_p = models.TextField()    # Paul's public key
    q_s = models.TextField()    # Server's public key
    
    # What it does: Bank API interaction
    bank_response = models.TextField(blank=True)
    encrypted_payload = models.TextField(blank=True)
    
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
