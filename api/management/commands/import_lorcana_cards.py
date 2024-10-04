import requests
from django.core.management.base import BaseCommand
from api.models import Card

class Command(BaseCommand):
    help = 'Import all Lorcana cards from the API into the local database'

    BASE_URL = 'https://api.lorcana-api.com/cards/fetch'

    def handle(self, *args, **kwargs):
        page = 1
        page_size = 100  # Adjust the page size according to API limits
        has_more = True
        
        while has_more:
            url = f'{self.BASE_URL}?pagesize={page_size}&page={page}'
            response = requests.get(url)

            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(f"Failed to fetch page {page}: {response.status_code}"))
                break

            cards_data = response.json()

            if len(cards_data) == 0:
                self.stdout.write(self.style.SUCCESS(f"All cards fetched!"))
                break

            # Process the cards for the current page
            self.import_cards(cards_data)

            # Check if there are more pages to fetch
            if len(cards_data) < page_size:
                has_more = False

            page += 1

    def import_cards(self, cards_data):
        """Process and save the cards into the database."""
        for card_data in cards_data:
            # Use update_or_create to either update the existing card or create a new one
            card, created = Card.objects.update_or_create(
                name=card_data['Name'],
                defaults={
                    'cost': card_data['Cost'],
                    'inkable': card_data['Inkable'],
                    'color': card_data.get('Color'),  # Ensure the ink field is updated
                    'lore': card_data.get('Lore'),
                    'strength': card_data.get('Strength'),
                    'willpower': card_data.get('Willpower'),
                    'rarity': card_data['Rarity'],
                    'card_type': card_data['Type'],
                    'artist': card_data['Artist'],
                    'set_name': card_data['Set_Name'],
                    'image_url': card_data['Image'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added {card.name} to the database."))
            else:
                self.stdout.write(self.style.SUCCESS(f"Updated {card.name} in the database."))
