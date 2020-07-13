from django.db import models


class CoronaInfoC(models.Model):
    updated = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    cases = models.TextField(blank=True, null=True)
    todayCases = models.TextField(blank=True, null=True, default=0)
    deaths = models.TextField(blank=True, null=True)
    todayDeaths = models.TextField(blank=True, null=True, default=0)
    recovered = models.TextField(blank=True, null=True)
    todayRecovered = models.TextField(blank=True, null=True, default=0)
    active = models.TextField(blank=True, null=True)
    critical = models.TextField(blank=True, null=True)
    casesPerOneMillion = models.TextField(blank=True, null=True)
    deathsPerOneMillion = models.TextField(blank=True, null=True)
    tests = models.TextField(blank=True, null=True)
    testsPerOneMillion = models.TextField(blank=True, null=True)
    population = models.TextField(blank=True, null=True)
    continent = models.TextField(blank=True, null=True)
    oneCasePerPeople = models.TextField(blank=True, null=True)
    oneDeathPerPeople = models.TextField(blank=True, null=True)
    oneTestPerPeople = models.TextField(blank=True, null=True)
    activePerOneMillion = models.TextField(blank=True, null=True)
    recoveredPerOneMillion = models.TextField(blank=True, null=True)
    criticalPerOneMillion = models.TextField(blank=True, null=True)
    flag = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.country

    class Meta:
        ordering = ['country']


class CoronaInfoD(models.Model):
    name = models.TextField(blank=True, null=True)
    bnName = models.TextField(blank=True, null=True)
    cases = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class CoronaInfoA(models.Model):
    name = models.TextField(blank=True, null=True)
    bnName = models.TextField(blank=True, null=True)
    cases = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
