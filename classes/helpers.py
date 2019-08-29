from classes.colours import Colours

# Returns an integer from zero to the (number of choices - 1).
# If the user cancels, it returns -1.
def get_choice(title, choice_list, cancel = False):
    index = 1
    low = 0 if cancel else 1
    high = len(choice_list)
    print("\n"+title+":")
    if cancel:
        print("  0 : cancel")
    for choice in choice_list:
        print("  "+str(index)+" : "+choice)
        index += 1
    x = -9999
    while x < low or x > high:
        try:
            x = int(input("Choice: "))
        except ValueError:
            x = -9999
        if x < low or x > high:
            print("Please enter a number between",low," and ",high)
    return x - 1

def stop_on_error(message):
    print(Colours.RED+message+Colours.END)
    exit(1)