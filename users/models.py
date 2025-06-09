from django.db import models

class SecureCipherUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    bvn = models.CharField(max_length=11, unique=True)
    nin = models.CharField(max_length=11, unique=True)
    ecdsa_public_key = models.TextField()
    virtual_account_id = models.CharField(max_length=64, unique=True, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.virtual_account_id:
            # Strip leading 0 if present and assign as account number
            raw_phone = self.phone_number
            self.virtual_account_id = raw_phone.lstrip("0")
            self.virtual_account_id = f"VX-{self.virtual_account_id}"
        # Ensure the virtual_account_id is unique
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.virtual_account_id})"
