from fastapi import FastAPI, Depends
from prometheus_client import Counter, start_http_server
import time
import random
import threading

app = FastAPI()

# Prometheus metrics
cards_total = Counter('cards_total', 'Total draw actions from the fastapi app')
individual_card_total = Counter('individual_card_total', 'Number each card is drawn', ['card'])
hearts_total = Counter('hearts_total', 'Number of hearts being drawn')
clubs_total = Counter('clubs_total', 'Number of clubs being drawn')
diamonds_total = Counter('diamonds_total', 'Number of diamonds being drawn')
spades_total = Counter('spades_total', 'Number of spades being drawn')

# Card deck
suits = ['hearts', 'diamonds', 'clubs', 'spades']
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
deck = [{'suit': suit, 'value': value} for suit in suits for value in values]

def draw_card():
    """Draw a card from the deck."""
    card = random.choice(deck)
    cards_total.inc()
    individual_card_total.labels(card=f"{card['value']}_of_{card['suit']}").inc()
    if card['suit'] == 'hearts':
        hearts_total.inc()
    elif card['suit'] == 'clubs':
        clubs_total.inc()
    elif card['suit'] == 'diamonds':
        diamonds_total.inc()
    elif card['suit'] == 'spades':
        spades_total.inc()
    return card

@app.get("/")
def read_root():
    """Root endpoint. Returns a drawn card."""
    return draw_card()

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
    """Draw a card at an interval of 5 seconds."""
    while True:
        draw_card()
        time.sleep(5)

if __name__ == "__main__":
    start_http_server(8001)
    threading.Thread(target=draw_cards_interval).start()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
