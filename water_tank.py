# TODO: Students, fill out statement of work header
# Student Name in Canvas: Anoushka Menon
# Penn ID: 30793147
# Did you do this homework on your own (yes / no): yes
# Resources used outside course materials: I used lecture materials to come up with the syntax and structural flow of the program.

# import statements
import random
from random import shuffle

# TODO: Write the functions as described in the instructions

"""
This function asks the user for input until a valid response is given. Question corresponds
to the prompt to the user.

Numeric responses are returned as integers.
Power cards are returned in uppercase.
"""
def get_user_input(question):
     while True:
            # prompt user with question & clean input
            user_input = input(question).strip()
            if len(user_input) == 0:
                    continue
            # if input is number return an integer 
            if user_input.isdigit():
                    return int(user_input)
            input_upper = user_input.upper()
            # return power card as uppercase string
            if input_upper in ["SOH", "DOT", "DMT"]:
                    return input_upper
            return user_input.lower()
"""
This function creates and shuffles the initial water cards pile. The deck includes water
cards with predefined values and quantities.

Function returns a shuffled list of water cards.
"""
def setup_water_cards():
        # initialize cards
        cards = []
        # add water cards of diff values & quantities
        cards.extend([1] * 30)
        cards.extend([5] * 15)
        cards.extend([10] * 8)
        # apply shuffle
        random.shuffle(cards)
        return cards

"""
This function creates and shuffles the initial power cards pile. The deck includes power
cards with predefined actions and quantities.

Function returns a shuffled list of power cards.
"""
def setup_power_cards():
        # initialize cards
        cards = []
        # add power cards of diff values & quantities
        cards.extend(["SOH"] * 10)
        cards.extend(["DOT"] * 2)
        cards.extend(["DMT"] * 3)
        # apply shuffle
        random.shuffle(cards)
        return cards

"""
This function initializes water and power card piles. It calls setup_water_cards and
setup_power_cards functions.

Function returns a 2-tuple containing a list of
"""
def setup_cards():
        # return a 2-tuple with water and power card piles 
        return(setup_water_cards(), setup_power_cards())


"""
This function removes and returns a card from a pile at a given index.

pile is the card pile to draw from.
index is the position of the card for removal.

Function returns the card that was removed from the pile
"""
def get_card_from_pile(pile, index):
        # remove entry at specified index of given pile 
        return pile.pop(index)

"""
This function sorts a mixed list of water and power cards. Water cards are integers in
ascending numerical order, and power cards are alphabetical. 

Cards_list is the list of cards that needs to be arranged.

Function does not return any output.
"""
def arrange_cards(cards_list):
        # classify water cards as ints and power cards as strs 
        water_cards = [c for c in cards_list if isinstance(c, int)]
        power_cards = [c for c in cards_list if isinstance(c, str)]

        # sort water cards in asc numerical order
        water_cards_sorted = sorted(water_cards)
        # sort power cards alphabetically
        power_cards_sorted = sorted(power_cards)

        # combine sorted cards
        cards_list[:] = water_cards_sorted + power_cards_sorted 
        
"""
This function deals hands to two players (human & computer). Each player gets 3 water cards
& 2 power cards, drawn from the top of the respective piles. Within each hand, cards arrange_cards
function is called to sort cards accordingly.

water_cards_pile and power_cards_pile are the shuffled piles of water and power cards to pull from.

The function returns a 2-tuple consisting of both players' hands.
"""
def deal_cards(water_cards_pile, power_cards_pile):
        # initialize player cards
        player1 = []
        player2 = []

        # deal 3 water cards to each player
        for i in range(3):
                player1.append(get_card_from_pile(water_cards_pile, 0))
                player2.append(get_card_from_pile(water_cards_pile, 0))

        # deal 2 power cards to each player
        for i in range(2):
                player1.append(get_card_from_pile(power_cards_pile, 0))
                player2.append(get_card_from_pile(power_cards_pile, 0))

        # call arrange cards function
        arrange_cards(player1)
        arrange_cards(player2)

        # return hands
        return(player1, player2)

"""
This function sets a maximum fill of 80 units, where any overflow is subtracted from the
maximum, resulting in a loss from the tank. The tank level is set to not go below 0.

tank_level corresponds to the current level of the tank.

Function returns an integer value. 
"""
def apply_overflow(tank_level):
        # set max fill
        max_fill = 80

        # check if tank level exceeds max 
        if tank_level > max_fill:
                # deduct overflow from max fill to update tank level
                overflow = tank_level - max_fill  
                tank_level = max_fill - overflow

                # ensure tank level not < 0
                if tank_level < 0:
                     tank_level = 0
        return tank_level
        
"""
This function applies the effect of the card to the tank and hand status. The chosen card is
removed from the hand and applied to player or opponent hand. The apply_overflow function is
called to make sure any overflow is accounted for.

player_tank corresponds to the current water level in player's tank
card_to_use is the card chosen by the player, player_cards corresponds to the player's hand
opponent_tank corresponds to the water level in the other player's tank.

Function returns a 2-tuple consisting of water levels in both tanks.
"""
def use_card(player_tank, card_to_use, player_cards, opponent_tank):
        # check is chosen card is in player hand
        if card_to_use in player_cards:
                player_cards.remove(card_to_use)
        else:
                raise ValueError("Card not found in player's stack")

        # check type of card being used
        if isinstance(card_to_use, int):
                # apply water card value
                player_tank += card_to_use

        # apply power card strategy
        elif isinstance(card_to_use, str):
                if card_to_use == "SOH":
                        stolen = opponent_tank // 2
                        player_tank += stolen
                        opponent_tank -= stolen
                elif card_to_use == "DOT":
                        opponent_tank = 0
                elif card_to_use == "DMT":
                        player_tank *= 2

        # apply overflow rule to relevant tank
        player_tank = apply_overflow(player_tank)
        opponent_tank = apply_overflow(opponent_tank)

        return player_tank, opponent_tank

"""
This function discards a card from the player's hand and returns it to the bottom of the right
pile.

card_to_discard correponds to the card at hand.
player_cards corresponds to the player's current hand.
water_cards_pile corresponds to the pile of water cards.
power_cards_pile corresponds to the same for power cards.

Function does not return anything.
"""
def discard_card(card_to_discard, player_cards, water_cards_pile, power_cards_pile):
        # check is chosen card is in player hand
        if card_to_discard in player_cards:
                player_cards.remove(card_to_discard)
        else:
                raise ValueError("Card not found in player's stack")

        # check is card is water or power card & add to bottom of relevant pile
        if isinstance(card_to_discard, int):
                water_cards_pile.append(card_to_discard)
        elif isinstance(card_to_discard, str):
                power_cards_pile.append(card_to_discard)

"""
This function checks if a tank is in the full threshold (between 75 to 80 inclusive.

tank refers to the current water level of the tank.

The function returns a boolean, True if the tank is full and False if not.
"""
def filled_tank(tank):
        # set min and max bounds for full tank
        min_fill = 75
        max_fill = 80
        if min_fill <= tank <= max_fill:
                return True
        else:
                return False

"""
This function refills an empty card pile, and refills a shuffled pile with correct card type, calling
the setup functions.

pile corresponds to the card pile to check and refill.
pile_type corresponds to water or power types.

Function does not return anything.
"""
def check_pile(pile, pile_type):
        # check is card pile is empty
        if len(pile) == 0:
                # check pile type & extend accordingly 
                if pile_type.lower() == "water":
                        pile.extend(setup_water_cards())
                elif pile_type.lower() == "power":
                        pile.extend(setup_power_cards())

"""
This function executes the human player turn. Function displays the current state of human and
computer tanks, current state of human card hand. Asks user if they would like to use or discard a card,
and asks to choose which card to carry out the action. Then applies the water or power card to player or
opponent's tank via use_card or discard_card functions. New card is drawn from the pile that a card was
used from, to maintain a hand of 5 cards with the correct ratio of water to power cards.

human_tank refers to the current water level of the human player's tank.
human_cards refers to the human player's current card hand
water_cards_pile refers to the pile of water cards
power_cards_pile refers to the pile of power cards
opponent_tank refers to the current water level of the opponent's tank

Function returns a 2-type of the current water level of human and opponent tanks. 
"""
def human_play(human_tank, human_cards, water_cards_pile, power_cards_pile, opponent_tank):
        # display current state of tanks & card hand
        print("Your water level:", human_tank)
        print("Computer water level:", opponent_tank)
        print("Your hand:", human_cards)
        
        action = ""
        # loop until user enters valid action
        while action not in ["use", "discard"]:
                action = get_user_input("Do you want to use or discard a card? (use / discard)")

        chosen_card = None
        # loop until user chooses valid card
        while True:
                chosen_card = get_user_input("Which card would you like to " + action + "?")
                if chosen_card in human_cards:
                        break
                else:
                        print("Card is not in your hand. Try again!")

        # if action is to use card call use card function
        if action.lower() == "use":
                print("You used card:", chosen_card)
                human_tank, opponent_tank = use_card(human_tank, chosen_card, human_cards, opponent_tank)
        # if action is to discard card call discard card function
        elif action.lower() == "discard":
                discard_card(chosen_card, human_cards, water_cards_pile, power_cards_pile)

        # draw new card of same pile type as one that was used or discarded
        if isinstance(chosen_card, int):
                check_pile(water_cards_pile, "water")
                new_card = get_card_from_pile(water_cards_pile, 0)
                print("Drawing water card:", new_card)
        elif isinstance(chosen_card, str):
                check_pile(power_cards_pile, "power")
                new_card = get_card_from_pile(power_cards_pile, 0)
                print("Drawing power card:", new_card)

        # add new card to existing hand
        human_cards.append(new_card)
        arrange_cards(human_cards)

        # display new state of tanks & hand after turn
        print("Your water level is now:", human_tank)
        print("Computer water level is now:", opponent_tank)
        print("Your cards are now:", human_cards)

        # return updated tank levels for next turn
        return human_tank, opponent_tank

"""
This function executes the computer player turn. Function displays the current state of human and
computer tanks. Function applies a strategy categorizing choice of power card by current status of water
level in tank, or else chooses a highest-value water card accounting for possible overflow. Then applies
the water or power card to player or opponent's tank via use_card or discard_card functions. New card is
drawn from the pile that a card was used from, to maintain a hand of 5 cards with the correct ratio of
water to power cards.

computer_tank refers to the current water level of the computer player's tank.
computer_cards refers to the computer player's current card hand
water_cards_pile refers to the pile of water cards
power_cards_pile refers to the pile of power cards
opponent_tank refers to the current water level of the opponent's tank

Function returns a 2-type of the current water level of computer and opponent tanks. 
"""
def computer_play(computer_tank, computer_cards, water_cards_pile, power_cards_pile, opponent_tank):
        # display current state of tanks
        print("Computer water level:", computer_tank)
        print("Your water level:", opponent_tank)
        
        chosen_card_comp = None
        action = ""

        # strategy: prioritize using power cards based on certain tank conditions
        if "DMT" in computer_cards and 5 <= computer_tank <= 40:
                chosen_card_comp = "DMT"
                action = "use"

        elif "SOH" in computer_cards and opponent_tank >= 10:
                chosen_card_comp = "SOH"
                action = "use"

        elif "DOT" in computer_cards and opponent_tank >= 30:
                chosen_card_comp = "DOT"
                action = "use"
        else:
                # if no power card should be used, use the highest value water card
                water_cards_comp = [c for c in computer_cards if isinstance(c, int)]
                if action == "" and len(water_cards_comp) > 0:
                     highest_water_card = max(water_cards_comp)

                     if computer_tank + highest_water_card <= 80:
                          chosen_card_comp = highest_water_card
                          action = "use"
                     else:
                          # discard lowest card if using highest will overflow tank
                          chosen_card_comp = min(water_cards_comp)
                          action = "discard"

        # if action is to use card call use card function
        if action == "use":
             print("Computer used card:", chosen_card_comp)
             computer_tank, opponent_tank = use_card(computer_tank, chosen_card_comp, computer_cards, opponent_tank)
        # if action is to discard card call discard card function
        elif action == "discard":
             print("Computer discarded card:", chosen_card_comp)
             discard_card(chosen_card_comp, computer_cards, water_cards_pile, power_cards_pile)

        # draw new card of same pile type as one that was used or discarded
        if isinstance(chosen_card_comp, int):
                check_pile(water_cards_pile, "water")
                new_card = get_card_from_pile(water_cards_pile, 0)
        elif isinstance(chosen_card_comp, str):
                check_pile(power_cards_pile, "power")
                new_card = get_card_from_pile(power_cards_pile, 0)

        # add new card to existing hand
        computer_cards.append(new_card)
        arrange_cards(computer_cards)

        # display new state of tanks after turn
        print("Computer water level is now:", computer_tank)
        print("Your water level is now:", opponent_tank)

        # return updated tank levels for next turn
        return computer_tank, opponent_tank

"""
The main function runs the flow of the water tank game between human and computer players. The function
initializes the card piles, player hands, and respective water_tank levels. Functioon provides game
instructions, and randomly chooses which player to go first, hen alternates between players for rest of the
game. Applies a loop which continues until one player wins. The exhibits which player won and ends game by
breaking loop. Calls the human_play and computer_play functions to do so.
"""
def main():
     # call setup cards and deal cards function
     water_cards_pile, power_cards_pile = setup_cards()
     human_cards, computer_cards = deal_cards(water_cards_pile, power_cards_pile)

     # initialize water tanks for both players to zero
     human_tank = 0
     computer_tank = 0

     # print welcome message & rules
     print("""Welcome to the Water Tank game! You will be playing against the Computer.
You will have water cards (numbers), and power cards at your disposal.
The power cards allow you to
     Double Your Tank (DMT)
     Steal Opponent's Half (SOH)
     Drain Opponent's Tank (DOT)
Choose from the cards you have available.
The first player to fill their tank wins!
Good Luck!""")
     print("\n")

     # randomly select player to start game
     player_up = random.choice(["Human", "Computer"])
     print("The first player selected to go is:", player_up)
     print("\n")

     # main game loop runs until someone wins the game
     while True:
          print("--", player_up, " player's turn!", "--")

          # call human play function for human turn
          if player_up == "Human":
               human_tank, computer_tank = human_play(
                    human_tank, human_cards, water_cards_pile, power_cards_pile, computer_tank
               )
               # switch turn 
               player_up = "Computer"
               print("\n")

          # call computer play function for computer turn
          elif player_up == "Computer":
               computer_tank, human_tank = computer_play(
                    computer_tank, computer_cards, water_cards_pile, power_cards_pile, human_tank
               )
               # switch turn
               player_up = "Human"
               print("\n")

          # check for winner - check if human tank or computer tank is filled
          if filled_tank(human_tank):
               print("GAME OVER!")
               print("You win! Your final tank level:", human_tank)
               # end game 
               break
          elif filled_tank(computer_tank):
               print("GAME OVER!")
               print("Computer wins! Computer final tank level:", computer_tank)
               # end game
               break
        
    # TODO: Write your code as described in the instructions

if __name__ == '__main__':
    main()
