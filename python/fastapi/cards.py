from fastapi import FastAPI, Response
import prometheus_client
from prometheus_client import Counter

import time
import random
import threading
import uvicorn


app = FastAPI()

# Prometheus metrics
cards_total = Counter('cards_total', 'Total draw actions from the fastapi app')
individual_card_total = Counter('individual_card_total', 'Number each card is drawn', ['card'])
hearts_total = Counter('hearts_total', 'Number of hearts being drawn')
clubs_total = Counter('clubs_total', 'Number of clubs being drawn')
diamonds_total = Counter('diamonds_total', 'Number of diamonds being drawn')
spades_total = Counter('spades_total', 'Number of spades being drawn')

# Card deck
def new_deck():
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
    deck = [{'suit': suit, 'value': value} for suit in suits for value in values]
    return deck

def reset_counter():
    return 0

def draw_card():
    """Draw a card from the deck."""
    deck = new_deck()
    draw_cards_count = reset_counter()
    card = random.choice(deck)
    cards_total.inc()

    # increment the counter for individual cards
    individual_card_total.labels(card=f"{card['value']}_of_{card['suit']}").inc()

    # reset the Counter of individual to 0 when a card is drawn 101 times
    if individual_card_total.labels(card=f"{card['value']}_of_{card['suit']}")._value == 101:
        individual_card_total.labels(card=f"{card['value']}_of_{card['suit']}")._value = 0

    deck.remove(card)
    draw_cards_count += 1
    
    # increment the Counter for a specific color
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

@app.get("/card")
def read_root():
    """card endpoint. Returns a drawn card."""
    return draw_card()

@app.get("/metrics")
def get_metrics():
    return Response(
        media_type="text/plain",
        content=prometheus_client.generate_latest(),
    )

@app.post("/reset")
def reset_counters():
    """Reset all the counters to zero."""
    cards_total._value.set(0)
    individual_card_total._metrics.clear()
    hearts_total._value.set(0)
    clubs_total._value.set(0)
    diamonds_total._value.set(0)
    spades_total._value.set(0)
    return {"message": "All counters have been reset!"}

def draw_cards_interval():
    """Draw a card at an interval of 1 second."""
    while True:
        draw_card()
        time.sleep(0.1)

if __name__ == "__main__":
    threading.Thread(target=draw_cards_interval).start()
    uvicorn.run(app, host="192.168.140.102", port=5000)