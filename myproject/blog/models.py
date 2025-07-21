from django.db import models
from django.contrib.postgres.fields import DateRangeField


class Station(models.Model):
    staid = models.TextField(unique=True, primary_key=True)
    staname = models.TextField(blank=True, null=True)
    longstaname = models.TextField(blank=True, null=True)
    network = models.TextField(blank=True, null=True)
    agency = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    receiver = models.TextField(blank=True, null=True)
    recvers = models.TextField(blank=True, null=True)
    recnum = models.TextField(blank=True, null=True)
    antenna = models.TextField(blank=True, null=True)
    antnum = models.TextField(blank=True, null=True)
    deltan = models.FloatField(blank=True, null=True)
    deltae = models.FloatField(blank=True, null=True)
    deltah = models.FloatField(blank=True, null=True)
    startdate = models.TextField(blank=True, null=True)
    enddate = models.TextField(blank=True, null=True)
    sta_daterange = DateRangeField(blank=True, null=True)

    class Meta:
        db_table = 'stations'  # Указываем имя существующей таблицы
        managed = False  # Чтобы Django не пытался управлять таблицей

    def __str__(self):
        return f"{self.staid} - {self.staname}"



class File(models.Model):
    id = models.AutoField(primary_key=True)
    staid = models.ForeignKey(
        Station,
        to_field='staid',
        db_column='staid',
        on_delete=models.CASCADE,
        related_name='files'
    )
    filename = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    period = models.TextField(blank=True, null=True)
    filetype = models.TextField(blank=True, null=True)
    int_observation = models.IntegerField(blank=True, null=True)
    fullness = models.FloatField(blank=True, null=True)
    path = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'stations_files'
        managed = False

    def __str__(self):
        return f"{self.filename} for {self.staid}"
