from django.db import models


class Record(models.Model):
    record_date = models.CharField(max_length = 100)
    record_response = models.CharField(max_length = 100)