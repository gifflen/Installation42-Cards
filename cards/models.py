from django.db import models
from django.db.models import Sum

class ActionType(models.Model):
    """
        ActionType Model.

        Various kinds of action types.
        Used by :model:`cards.Action`.

        name    --  Name of the action type. Ex. Attack
    """
    name = models.CharField(max_length=10,unique=True)
    def __unicode__(self):return str(self.name)
    class Meta:
        ordering = ['name']

#AOE, SELF, TARGETED, MELEE, L+R or L/R GLOBAL
class ActionTarget(models.Model):
    """
        ActionTarget Model.

        Contains the various ways abilities can target players.
        Used by :model:`cards.Action`.

        name        --  Name for the targeting mechanic.
        description --  A full description for how the targeting works.
    """
    name = models.CharField(max_length=10,unique=True)
    description = models.TextField(max_length=100)
    def __unicode__(self):return str(self.name)
    class Meta:
        ordering = ['name']

class Action(models.Model):
    """
        Action Model.

        Contains the various actions that are use to create an ability.
        Used by :model:`cards.Ability`.

        name    --  Name for the generic action.
        type    --  The type of action the ability is classified as. References :model:`cards.ActionType`
        target  --  The targeting mechanic this ability uses. References :model:`cards.ActionTarget`
        armor   --  The amount of armor this action contributes to the player.
        health  --  The amount of health this action contributes to the player.
        damage  --  The amount of damage this action inflicts on its target.
        value   --  The balancing value this card is worth.
    """
    name = models.CharField(max_length=50,unique=True)
    type = models.ForeignKey('ActionType')
    target = models.ForeignKey('ActionTarget')
    armor = models.PositiveIntegerField(default=0)
    health = models.PositiveIntegerField(default=0)
    damage = models.PositiveIntegerField(default=0)
    value = models.PositiveIntegerField(default=0)
    def __unicode__(self):return str(self.name)
    class Meta:
        ordering = ['name']

class Deck(models.Model):
    """
        Deck Model.

        Contains the various possible decks that a card can be present in.
        Used by :model:`cards.Card`.

        name    --  Name for the deck.
    """
    name = models.CharField(max_length=50)
    def __unicode__(self):return str(self.name)
    class Meta:
        ordering = ['name']

class Faction(models.Model):
    """
        Faction Model.

        Contains the various factions of the game.
        Used by :model:`cards.Card`.

        name        --  Name of the faction.
        description --  The description of the faction.
        color       --  The color associated with the faction.
    """
    name = models.CharField(max_length=50,unique=True)
    description = models.TextField(max_length=200)
    color = models.CharField(max_length=10)
    def __unicode__(self):return str(self.name)
    class Meta:
        ordering = ['name']

class Ability(models.Model):
    """
        Ability Model.

        Contains all relevant information for what an ability present on a card comprises of.
        Used by :model:`cards.Card`.

        name        --  Name of the ability.
        description --  A short description of the ability.
        actions     --  A reference to the different actions that
                            combine to create the ability. References :model:`cards.Action`
        value_adj   --  The modifier for making an ability have more or less value.
    """
    name = models.CharField(max_length=50,unique=True)
    description = models.TextField(max_length=100)
    actions = models.ManyToManyField('Action')
    value_adj = models.IntegerField(default=0)
    def __unicode__(self):return str(self.name)
    class Meta:
        ordering = ['name']
        verbose_name_plural ="Abilities"

    @property
    def total_damage(self):
        """  Sums total damage based on actions present in an ability
            Default: 0
        """
        return self.actions.aggregate(Sum('damage'))['damage__sum']

    @property
    def total_health(self):
        """  Sums total health based on actions present in an ability
            Default: 0
        """
        return self.actions.aggregate(Sum('health'))['health__sum']

    @property
    def total_armor(self):
        """  Sums total armor based on actions present in an ability
            Default: 0
        """
        return self.actions.aggregate(Sum('armor'))['armor__sum']

    @property
    def total_value(self):
        """  Sums total card value based on actions present in an ability and the value_adj
            Default: 0
        """
        return self.actions.aggregate(Sum('value'))['value__sum']+self.value_adj

class Card(models.Model):
    """
        Card Model.

        Contains all of the information about a card.

        name    --  Name of the card
        economy --  Economy generated by the card
        cost    --  Cost to purchase the card
        ability1--  The first of two playable abilities on a card. Uses :model:`cards.Ability`
        ability2--  The second of two playable abilities on a card. Uses :model:`cards.Ability`
        faction --  The faction this card is associated with. Uses :model:`cards.Faction`
        deck    --  The deck this card belongs to. Uses :model:`cards.Deck`
    """
    name = models.CharField(max_length=50,unique=True)
    economy = models.PositiveIntegerField(default=0)
    cost = models.PositiveIntegerField(default=0)
    ability1 = models.ForeignKey('Ability', related_name='ability1_name')
    ability2 = models.ForeignKey('Ability', related_name='ability2_name')
    faction = models.ForeignKey('Faction')
    deck = models.ForeignKey('Deck')
    def __unicode__(self):return str(self.name)
    class Meta:
        ordering = ['name']
    @property
    def total_value(self):
        """  Sums total card value based on abilities on the card
            Default: 0
        """
        return self.ability1.total_value + self.ability2.total_value

