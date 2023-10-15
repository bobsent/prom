# At the beginning of your code, create an empty set to track removed cards
removed_cards = set()


def draw_card():
    deck = new_deck()
    draw_cards_count = reset_counter()
    card = random.choice(deck)
    cards_total.inc()

    card_key = f"{card['value']}_of_{card['suit']}"
    
    # Check if the card has been drawn 101 times
    if card_key in drawn_cards and drawn_cards[card_key] >= 101:
        # Remove the card from the deck
        deck.remove(card)
        removed_cards.add(card_key)  # Add the removed card to the set
        del drawn_cards[card_key]

    # Increment the counter for individual cards
    if card_key in drawn_cards:
        drawn_cards[card_key] += 1
    else:
        drawn_cards[card_key] = 1

    # Increment the Counter for a specific color
    if card['suit'] == 'hearts':
        hearts_total.inc()
    elif card['suit'] == 'clubs':
        clubs_total.inc()
    elif card['suit'] == 'diamonds':
        diamonds_total.inc()
    elif card['suit'] == 'spades':
        spades_total.inc()

    if draw_cards_count == 13:
        deck = new_deck()
        draw_cards_count = 0

    return card


@app.get("/removed_cards")
def list_removed_cards():
    return {"removed_cards": list(removed_cards)}


# New endpoint to return a removed card to the deck and reset its counter
@app.put("/return_card/{card_key}")
def return_card(card_key: str):
    if card_key in drawn_cards:
        drawn_cards[card_key] = 0
        return {"message": f"Card {card_key} has been returned to the deck with the counter reset to 0."}
    else:
        raise HTTPException(status_code=404, detail=f"Card {card_key} not found in the removed cards list.")


