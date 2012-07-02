from django.db import models

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
    def __unicode__(self):return str(self.name)

class Deck(models.Model):
    name = models.CharField(max_length=50)
    def __unicode__(self):return str(self.name)

class Faction(models.Model):
    name = models.CharField(max_length=50,unique=True)
    description = models.TextField(max_length=200)
    def __unicode__(self):return str(self.name)

class Ability(models.Model):
    name = models.CharField(max_length=50,unique=True)
    description = models.TextField(max_length=100)
    action = models.ManyToManyField('Action')
    def __unicode__(self):return str(self.name)
    #TODO: Total stats from all selected abilities
    def total_damage(self): return 0
    def total_healing(self): return 0
    def total_armor(self): return 0

class Card(models.Model):
    name = models.CharField(max_length=50,unique=True)
    economy = models.PositiveIntegerField(default=0)
    cost = models.PositiveIntegerField(default=0)
    ability1 = models.ForeignKey('Abilities')
    ability2 = models.ForeignKey('Abilities')
    faction = models.ForeignKey('Faction')
    deck = models.ForeignKey('Deck')
    def __unicode__(self):return str(self.name)

