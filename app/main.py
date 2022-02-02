from fastapi import FastAPI
from typing import Literal
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import copy

origins = ["*"]

class Card(BaseModel):
    name: str
    number1: str
    number2: str
    number3: str
    number4: str
    year: str
    month: str
    owner: str
    type: Literal["포코", "준", "공원", "브랜", "로이드", "도비", "콜린", "썬"]
    cvc: Optional[str]
    password1: Optional[str]
    password2: Optional[str]
    createAt: int

class CardInstance(BaseModel):
    id: str
    card: Card

class CardFactory:
    def __init__(self) -> None:
        self.cards: dict[str, Card] = {}


    def getAll(self):
        cards = copy.deepcopy(self.cards)

        for key in cards:
            card = cards[key]
            del card.password1
            del card.password2
            del card.cvc
            
        return cards

    def get(self, id: str):
        card = copy.deepcopy(self.cards.get(id))

        if card == None:
            return None

        del card.password1
        del card.password2
        del card.cvc

        return card

    def append(self, cardInsance: CardInstance):
        self.cards[cardInsance.id] = cardInsance.card

    def remove(self, id: str):
        del self.cards[id]

    def updateName(self, cardInsance: CardInstance):
        card = copy.deepcopy(self.cards.get(cardInsance.id))

        if card == None:
            return None
        
        card.name = cardInsance.card.name
        self.cards[cardInsance.id] = card
    

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cardFactory = CardFactory()

@app.get("/cards")
def read_cards():
    return cardFactory.getAll()

@app.get("/card/{card_id}")
def read_card(card_id: str):
    return cardFactory.get(card_id)

@app.post("/card")
def append_card(cardInstance: CardInstance):
    return cardFactory.append(cardInstance)

@app.put("/card")
def update_card(cardInstance: CardInstance):
    return cardFactory.updateName(cardInstance)

@app.delete("/card/{card_id}")
def delete_card(card_id: str):
    return cardFactory.remove(card_id)


