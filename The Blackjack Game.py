# =======================     BlackJack    ============================

import cards, games

class BJ_Card(cards.Card):
    """ A blackjack Card"""
    ACE_VALUE = 1

    # the below method decides what each card is worth as in 1 is worth 1 and j, q, k is worth 10
    @property
    def value(self):
        if self.is_face_up: # if the card is facing up perform the action below
            v = BJ_Card.RANKS.index(self.rank) + 1 # this access the RANKS attribute in cards class in cardsmodule and then finds the index for the rank of the card. so if its a 6 the index would be 5 and then you take the index plus 1 makes the card value.
            if v > 10: # if the index +1 aka the rank/value of the card that came out is greater than 10 e.g jack
                v = 10 # jack queen and king all set to a value of 10
            else:
                v = BJ_Card.RANKS.index(self.rank) + 1 # if not facing up nothing happens.
            return v # return the result
    
class BJ_Deck(cards.Deck): # creates a deck object for the game.
    """ A Blackjack deck"""
    def populate(self): # takes the attributes of suits and rank from the cardmodule and creates a card object for every card.
        for suit in BJ_Card.SUITS: # for every suit and every rank perform the creation of an object below.
            for rank in BJ_Card.RANKS:
                self.cards.append(BJ_Card(rank, suit)) # it then adds in to the inherited self.cards list in the deck class in cardmodule 
    
    def check_deck(self,names): # checks to see if
        print("\nchecking if enough cards in deck to play another round....")
        noplayers = len(names)
        cardsrequired = noplayers * 5
        decksize = len(self.cards)
        if decksize < cardsrequired:
            print("There are not enough cards left in the deck to play another round. repopulating the deck.")
            self.populate()
            self.shuffle()
        else:
            print("There are enough cards to play the round. restarting new round....")


class BJ_Hand(cards.Hand): # here we are adding the name parameter to name the player.
    """A BlackJack Hand"""  # this method grabs the attributes from its superclass instead of creating the
    def __init__(self, name): # attributes again.
        super(BJ_Hand, self).__init__() # its access the constructor attributes which is just the list of cards
        self.name = name
        self.balance = 100 # here is the new variable

    def __str__(self):
        rep = self.name + ":\t" + super(BJ_Hand, self).__str__()
        if self.total:  # if there is a value in the total attribute then perform below.
            rep += "(" + str(self.total) +")" # sets rep to total value
        return rep # out puts that total value.
    @property
    def total(self): # if any card in the hand has a value of None which means its facing down.
        
        for card in self.cards:
            if not card.value:
                return None
        
        t = 0 # adds up all the card values and treats ace as 1 due to 0 index +1 earlier in the value method
        for card in self.cards:
            t+= card.value
        
        contains_ace = False
        for card in self.cards: # for every card in the self.cards apply the value method and if the value = 1
            if card.value ==  BJ_Card.ACE_VALUE:
                contains_ace = True  # if ace is found then set the variable contains ace to true 
                                    # to be used in the next loop.
        
        if contains_ace and t<= 11: # ace is worth 11 or 1 but if the total is = 11 including the ace
            t+=10    # if its less than 11 then you can add and go up to 21 as the 1 is already added in the total
                    # but its more than 11 then you bust as you go over 21.
        return t
    
    def is_busted(self):
        return self.total > 21
         # shorted version instead of using if statements to return true or false.
        # so if self.total is greater than 21 return true if it doesnt then return false.
        # self refers to itself as the object.

class BJ_Player(BJ_Hand):
    """ A Blackjack Player"""

    def is_hitting(self):
        if self.total == 21:
            print(self.name,"has the maximum score, Automatically holding at 21.")
            return False
        response = games.ask_yes_no("\n"+ self.name + " do you want to hit? (Y/N):  ") # uses games module and its ask yes no function.
        if response == "n": 
            print(self.name,"is holding")
            return False
        return response == "y" # if response == "y" return True
    @property
    def place_bet(self):
        print("")
        print(self.name,"has a current balance of £",self.balance)
        bet = games.ask_number("How much would you like to bet:  £", 1, self.balance+1)
        print(self.name,"has chosen to bet £",bet)
        self.balance -= bet
        self.bet = bet
        print("you have £",self.balance,"remaining")

    def bust(self):
        print(self.name, "busts")
        self.lose()

    def lose(self):
        print(self.name, "loses")

    @property
    def is_bankrupt(self):
        return self.balance == 0

    def win(self, dealertotal):
        winnings = (self.bet*2)
        self.balance += winnings
        if dealertotal > 21: 
            print("The dealer has busted",self.name,"wins : £",winnings)
            print(self.name,"has a new balance of £",self.balance)
            
        else: 
            print(self.name,"Wins : £",winnings)
            print(self.name,"has a new balance of £",self.balance)
        
    def push(self):
        print(self.name, "pushes")
        self.balance += self.bet
        print("Your bet of",self.bet,"has been returned to your balance")

class BJ_Dealer(BJ_Hand):
    def is_hitting(self):
        return self.total < 17  # returns True if less than 17 making dealer hit again
    def bust(self):
        print(self.name, "has busted") # prints statement
    def flip_first_card(self):
        first_card = self.cards[0] # sets the first card in the hand to first_card
        first_card.flip() # performs the flip method in the card Class on the first_card.

class BJ_Game(object):
    """ A blackjack Game"""
    def __init__(self, names): # takes the list of names
        self.players = [] # makes a list where we can store players playing
        for name in names: # for every name in the list of names create a BJ PLAYER OBJECT
            player = BJ_Player(name) # the code that creates the object using names in a list
            self.players.append(player) # append the object to the self.players list.
        
        self.dealer = BJ_Dealer("Dealer") # # creates a BJ_dealer object and assigns it as a attribute of BJ_GAME
        self.deck = BJ_Deck() # assigns a BJ_deck as an attribute of BJ game
        self.deck.populate() # creates and deck using the decks populate method
        self.deck.shuffle() # shuffles the deck in a random order using the decks shuffle method.

    @property
    def still_playing(self):
        sp = []  # a list of players till playing to be created from the loops below
        for player in self.players: #for every player that is playing 
            if not player.is_busted(): # run the is busted method on the object. and if it return false
                sp.append(player) # it appends that player to the sp list.
        return sp  # returns the list of players still playing

    def enough_funds(self):
        #playable =[] # this variable is used in a longer but better solution which places the players left messages in order
        for player in reversed(self.players):
            if player.is_bankrupt:
                print(player.name,"has insufficent funds to play again.",player.name,"has left the table.")
                self.players.remove(player)#take this out if second soultion is needed.
            #else: This is a second soultion if needed.
                #print(player.name,"has sufficient funds to continue.")
                #playable.append(player)
        #self.players = playable
    def __additional_cards(self, player): # this method deals the player extra cards
        while not player.is_busted() and player.is_hitting(): # while hitting and not busted keep looping
            self.deck.deal([player]) # deals the player a card from the deck and uses the deal method in deck.
            print(player) # prints player
            if player.is_busted(): # if the players super class 'hand' object method 'is_busted' returns true 
                player.bust() # then it activates the BJ_player method bust.

    def play(self,names): #the constructor created a deck and players now its time to play with it
        for player in self.players:
            player.place_bet

        print("") # starts by dealing 2 cards to everyone. access the deal class in the cards module and takes in the list of players and changes the dealer object into a list.
        self.deck.deal(self.players + [self.dealer], per_hand = 2) # and takes into how many rounds in wants to deal. which is 2.   
        self.dealer.flip_first_card() # this hides the dealers first card by accessing

        for player in self.players: # for every object(BJ_player) in the player list
            print(player) # access its BJ_players>BJ_hand __str__method which prints name , cards and score.
        print(self.dealer) # accesses the same as the players did in the _str__ method 
        
        for player in self.players: # for every object(BJ_player) in the player list
            self.__additional_cards(player) # apply additional cards method give a player card objects if the criteria of not busted and is continuing to hit
        
        self.dealer.flip_first_card()
        if not self.still_playing: # if the sp in still playing is empty meaning no one is still playing
            print("")
            print(self.dealer,"\nThe dealer has won no players left in the game.") # prints the BJ-dealer object which shows name,hand and score
        else:
            print("")
            print(self.dealer) # while there are others still playing the dealer keeps hitting until he has a number
            self.__additional_cards(self.dealer) # greater than 17 or busts. but invoking the additonal cards method
                                        # which invokles is_hitting method for the dealer which is true until terms of 17 or more is met.
            if self.dealer.is_busted(): # once the dealers parameters are met it checks if the dealer is busted.
                for player in self.still_playing: # if the dealer is busted it checks which players are still playing
                    player.win(self.dealer.total) # it then invokes the win method for every player that is still playing.

            else:# if the dealer is not busted then it needs to compare scores.
                print("The dealer holds at",self.dealer.total)
                print("\nCalculating the winners...")
                for player in self.still_playing: # for every player still playing
                    if player.total > self.dealer.total: # check if the players score is higher than dealer
                        player.win(self.dealer.total) # if it is higher than that player wins
                    elif player.total < self.dealer.total: # if the players total is less than the dealer                      
                        player.lose() # invoke that the player loses
                    else: # if the player gets the same as the dealer its a draw
                        player.push() # invoke the push method

        for player in self.players: # for ever player that played in the list
            player.clear() # clear their cards
        self.dealer.clear() # clear the dealers cards.
        self.names = names
        self.enough_funds()
        if self.players == []:
            print("There are no more players with sufficient funds. The table will now close. thanks for playing")
            import sys
            sys.exit()
        self.deck.check_deck(names)
        
def main():
    print("welcome to the black jack game")
    names = []
    number = games.ask_number("how many players would you like to player (1-4):  ", low = 1, high = 5)
    for i in range(number):
        name = input("Enter the name of player:  ")
        names.append(name)
    print()
    game = BJ_Game(names)
    
    again = None
    while again != "n":
        game.play(names)
        again = games.ask_yes_no("\ndo you want to play again? (Y / N):  ")

main()
print("Thanks for playing Blackjack")
input("\npress enter to exit")
