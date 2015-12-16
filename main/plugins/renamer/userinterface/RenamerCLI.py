class RenamerCLI():
    
    def __init__(self):
        print()
        
    def start(self):
        while True:
            userInput = input("User Input:\n").lower()
            if userInput in ["quit", "exit"]:
                break
            else:
                print("User Input not understood")