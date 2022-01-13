from HumanPlayer import HumanPlayer
from Player import Player
from State import State

if __name__ == '__main__':

    # Train the AI
    #p1 = Player("Play1")
    #p2 = Player("Play2")

    #state = State(p1,p2)
    #print("TRAIN")
    #state.train(150000)
    #p1.savePolicy()

    p1 = Player("Computer", e_val = 0)
    p1.loadPolicy("policy_Play1")

    p2 = HumanPlayer(input("Please enter a name: "))

    state = State(p1,p2)
    state.play_human()

    again = input("Do you want to play again? (y/n) ")
    while again == "y":
        state.play_human()
        print("")
        again = input("Do you want to play again? (y/n) ")

    print("Thank you for playing.")



