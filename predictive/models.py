from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class SensorDataLog(models.Model):
    id = models.AutoField(primary_key=True)
    element_id = models.CharField(max_length=255, null=False)
    max = models.DecimalField(max_digits=8, decimal_places=4)
    min = models.DecimalField(max_digits=8, decimal_places=4)
    avg = models.DecimalField(max_digits=8, decimal_places=4)
    no_of_records = models.IntegerField()
    timestamp = models.DateTimeField()
    org_id = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.max}-{self.min} - {self.avg} - {self.timestamp}"


class SettingsOrg(models.Model):
    company_code = models.CharField(max_length=255, null=False)
    plant_code = models.CharField(max_length=255, null=False)
    line_code = models.CharField(max_length=255, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    org_id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.timestamp} - {self.plant_code} - {self.line_code} - {self.org_id}"


class SettingsElement(models.Model):
    element_id = models.CharField(max_length=255, null=False)
    element_name = models.CharField(max_length=255, null=False)
    tag = models.CharField(max_length=255, null=False)
    server_ip = models.CharField(max_length=255, null=False)
    machine_code = models.CharField(max_length=255, null=False)
    element_type = models.CharField(max_length=255, null=False)
    remarks = models.TextField()
    org_id = models.CharField(max_length=255, null=False)
    active = models.BooleanField(default=True)
    prediction = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.element_id}-{self.element_name} - {self.element_type} - {self.active}"


class ErrorLog(models.Model):
    id = models.AutoField(primary_key=True)
    service = models.CharField(max_length=255, null=False)
    error_category = models.CharField(max_length=255, null=False)
    error_text = models.TextField()
    severity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)],
                                   help_text="severity must be between 1 to 10 ( integer ) ")
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.service}-{self.error_category} - {self.severity} - {self.timestamp}"
