
# ============  writing a module  =============

"""
a module looks every similar to any other code but there is a piece of code at the end of the module that turns
it into a module that prevents it from being a directly runnable program.
"""

class Player(object):
    """ a player for a game"""
    def __init__(self, name, score = 0):
        self.name = name
        self.score = score
    
    def __str__(self):
        rep = self.name + ":\t" + str(self.score)
        return rep
    

def ask_yes_no(question):
    """ asks yes or no question"""
    response = None
    while response not in ("y", "n"):
        response = input(question).lower()
    return response

def ask_number(question, low, high):
    """ ask for a number within a range"""
    response = None
    while response not in range(low,high):
        try:
            response = int(input(question))
            if response >= high or response < low:
                print("you can only enter a figure between:",low,"-",high-1)
        except:
            print("That is not a figure. you can only enter a figure between",low,"-",high-1  )
    return response

if __name__ == "__main__":  # this is the key to it being a module and not being another py file.
    print("you ran this module directly and did not import it.(please use import games")
    input("please press enter to exit")




