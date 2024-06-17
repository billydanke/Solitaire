import DeckManager
import EventManager

moveStack = [] # (Card, source, destination)

def AddMove(card, source, destination):
    moveStack.append((card,source,destination))

def UndoMove():

    if(not moveStack):
        print("Attempted to undo an empty move stack!")
        return

    # Get the top move off of the stack and remove it from the stack (pop).
    card,source,destination = moveStack.pop()

    DeckManager.grabbedCardList.append(card)

    # Get children cards and append them as well
    childCards = card.owner.getChildCards(card)

    # If the owner is DrawPile, set the cheaty flip on the card below
    if(card.owner.type == "DrawPile"):
        prevCard = None
        if(len(card.owner.cards) > 1):
            prevCard = card.owner.cards[-2]
        if(prevCard != None and not (prevCard in card.owner.pileCards)):
            # At this point, we know that the prevCard is the card below the topmost
            prevCard.flippedOver = True
            #print(f"set card {prevCard.labelText} to cheaty flipped")

    card.owner.cards.remove(card)

    for index,childCard in enumerate(childCards):
        card.moveWithCard = True

        # Get parent cards
        if(index == 0):
            childCard.parentCard = card
        else:
            childCard.parentCard = childCards[index-1]

        # Set this card's parent's child to this. (lol confusing)
        childCard.parentCard.childCard = childCard

        DeckManager.grabbedCardList.append(childCard)
        childCard.owner.cards.remove(childCard)
        childCard.dragSourceX = childCard.x
        childCard.dragSourceY = childCard.y

    # Reset the card's owner to its source.
    for card in DeckManager.grabbedCardList:
            EventManager.cardList.remove(card)
            EventManager.cardList.append(card)

    card.handleDestination(source,False)