# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Device(models.Model):
    id = models.IntegerField(primary_key=True)
    station = models.ForeignKey('Station', models.DO_NOTHING, blank=True, null=True)
    scp = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'device'


class Station(models.Model):
    id = models.IntegerField(primary_key=True)
    ca = models.CharField(max_length=250)
    unit = models.CharField(max_length=250)
    name = models.CharField(max_length=250, blank=True, null=True)
    line = models.CharField(max_length=250, blank=True, null=True)
    division = models.CharField(max_length=250, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'station'


class Turnstile(models.Model):
    id = models.IntegerField(primary_key=True)
    device = models.ForeignKey(Device, models.DO_NOTHING, blank=True, null=True)
    timestamp = models.IntegerField()
    description = models.CharField(max_length=250, blank=True, null=True)
    entry = models.IntegerField()
    exit = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'turnstile'


class Previous(models.Model):
    id = models.BigIntegerField(primary_key=True)
    device_id = models.IntegerField(blank=True, null=True)
    timestamp = models.BigIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    entry = models.BigIntegerField(blank=True, null=True)
    exit = models.BigIntegerField(blank=True, null=True)
    file_date = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'previous'