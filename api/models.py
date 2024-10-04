from django.db import models

class Card(models.Model):
    name = models.CharField(max_length=255)
    cost = models.IntegerField()
    inkable = models.BooleanField(default=False)
    color = models.CharField(max_length=50, null=True, blank=True)  # Changed ink to color
    lore = models.IntegerField(null=True, blank=True)
    strength = models.IntegerField(null=True, blank=True)
    willpower = models.IntegerField(null=True, blank=True)
    rarity = models.CharField(max_length=50, null=True, blank=True)
    card_type = models.CharField(max_length=50, null=True, blank=True)
    artist = models.CharField(max_length=255, null=True, blank=True)
    set_name = models.CharField(max_length=100, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.card_type} (Cost: {self.cost})"

class Deck(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def card_count(self):
        return sum(deck_card.quantity for deck_card in self.deckcard_set.all())

class DeckCard(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('deck', 'card')  # Ensures each card can only appear once per deck

    def __str__(self):
        return f"{self.card.name} x{self.quantity} in {self.deck.name}"
