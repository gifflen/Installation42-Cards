from django.db import models
from django.db.models import Sum

#Attack, Defense etc
class ActionType(models.Model):
    name = models.CharField(max_length=10,unique=True)
    def __unicode__(self):return str(self.name)

#AOE, SELF, TARGETED, MELEE, L+R or L/R GLOBAL
class ActionTarget(models.Model):
    name = models.CharField(max_length=10,unique=True)
    description = models.TextField(max_length=100)
    def __unicode__(self):return str(self.name)

class Action(models.Model):
    name = models.CharField(max_length=50,unique=True)
    type = models.ForeignKey('ActionType')
    target = models.ForeignKey('ActionTarget')
    armor = models.PositiveIntegerField(default=0)
    health = models.PositiveIntegerField(default=0)
    damage = models.PositiveIntegerField(default=0)
    value = models.PositiveIntegerField(default=0)
    def __unicode__(self):return str(self.name)

class Deck(models.Model):
    name = models.CharField(max_length=50)
    def __unicode__(self):return str(self.name)

class Faction(models.Model):
    name = models.CharField(max_length=50,unique=True)
    description = models.TextField(max_length=200)
    color = models.TextField(max_length=6)
    def __unicode__(self):return str(self.name)

class Ability(models.Model):
    name = models.CharField(max_length=50,unique=True)
    description = models.TextField(max_length=100)
    actions = models.ManyToManyField('Action')
    value_adjustment = models.IntegerField(default=0)
    def __unicode__(self):return str(self.name)

    @property
    def total_damage(self):
        return self.actions.aggregate(Sum('damage'))['damage_sum']

    @property
    def total_healing(self):
        return self.actions.aggregate(Sum('healing'))['healing_sum']

    @property
    def total_armor(self):
        return self.actions.aggregate(Sum('armor'))['armor_sum']

    @property
    def total_value(self):
        return self.actions.aggregate(Sum('value'))['value_sum']

class Card(models.Model):
    name = models.CharField(max_length=50,unique=True)
    economy = models.PositiveIntegerField(default=0)
    cost = models.PositiveIntegerField(default=0)
    ability1 = models.ForeignKey('Ability', related_name='ability1_name')
    ability2 = models.ForeignKey('Ability', related_name='ability2_name')
    faction = models.ForeignKey('Faction')
    deck = models.ForeignKey('Deck')
    def __unicode__(self):return str(self.name)

