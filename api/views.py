from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Deck, Card, DeckCard
from django.contrib import messages
from django.http import JsonResponse

from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Card

def card_list(request):
    # Number of cards per page
    cards_per_page = 18

    # Sorting and filtering parameters from the request
    sort_by = request.GET.get('sort_by', 'name')
    rarity_filter = request.GET.get('rarity', 'all')
    inkable_filter = request.GET.get('inkable', 'all')
    card_type_filter = request.GET.get('card_type', 'all')
    color_filter = request.GET.get('color', 'all')  # New color filter

    # Get all cards
    cards = Card.objects.all()

    # Apply filtering by rarity
    if rarity_filter != 'all':
        cards = cards.filter(rarity=rarity_filter)

    # Apply filtering by inkable
    if inkable_filter != 'all':
        cards = cards.filter(inkable=(inkable_filter == 'true'))

    # Apply filtering by card type
    if card_type_filter != 'all':
        cards = cards.filter(card_type=card_type_filter)

    # Apply filtering by color
    if color_filter != 'all':
        cards = cards.filter(color=color_filter)

    # Apply sorting
    if sort_by == 'name':
        cards = cards.order_by('name')
    elif sort_by == 'cost':
        cards = cards.order_by('-cost')
    elif sort_by == 'lore':
        cards = cards.order_by('-lore')
    elif sort_by == 'strength':
        cards = cards.order_by('-strength')
    elif sort_by == 'willpower':
        cards = cards.order_by('-willpower')

    # Apply pagination
    paginator = Paginator(cards, cards_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Handle AJAX request and return JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cards_html = render(request, 'api/partials/card_list.html', {'page_obj': page_obj}).content.decode('utf-8')
        pagination_html = render(request, 'api/partials/pagination.html', {'page_obj': page_obj}).content.decode('utf-8')
        return JsonResponse({'cards_html': cards_html, 'pagination_html': pagination_html})

    # Regular page load
    return render(request, 'api/card_list.html', {'page_obj': page_obj})

def create_deck(request):
    if request.method == "POST":
        deck_name = request.POST.get("deck_name")
        deck = Deck.objects.create(name=deck_name)
        return redirect('add_to_deck', deck_id=deck.id)
    return render(request, 'api/create_deck.html')

def add_to_deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    cards = Card.objects.all()

    if request.method == "POST":
        card_id = request.POST.get("card_id")
        quantity_to_add = int(request.POST.get("quantity", 1))  # Get quantity from the form
        card = get_object_or_404(Card, id=card_id)

        # Check if the card is already in the deck
        deck_card, created = DeckCard.objects.get_or_create(deck=deck, card=card)

        # Ensure that adding the card won't exceed the 4-card limit
        if deck_card.quantity + quantity_to_add > 4:
            messages.error(request, f"You can't have more than 4 copies of {card.name} in your deck.")
        else:
            deck_card.quantity += quantity_to_add  # Add to the existing quantity
            deck_card.save()
            messages.success(request, f"Added {quantity_to_add} copies of {card.name} to your deck.")

        return redirect('view_deck', deck_id=deck.id)

    return render(request, 'api/add_to_deck.html', {'deck': deck, 'cards': cards})
def view_deck(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    deck_cards = DeckCard.objects.filter(deck=deck)
    return render(request, 'api/view_deck.html', {'deck': deck, 'deck_cards': deck_cards})

def remove_from_deck(request, deck_id, card_id):
    deck = get_object_or_404(Deck, id=deck_id)
    card = get_object_or_404(Card, id=card_id)
    deck_card = get_object_or_404(DeckCard, deck=deck, card=card)
    
    if deck_card.quantity > 1:
        deck_card.quantity -= 1  # Reduce quantity by 1
        deck_card.save()
    else:
        deck_card.delete()  # Remove the card from the deck if quantity is 1

    return redirect('view_deck', deck_id=deck.id)