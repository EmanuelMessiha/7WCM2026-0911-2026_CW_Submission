# Emanuel Messiha
# 7WCM2026-0911-2026 - Data Structure and Algorithms 2
# Question 3 Recursion

# Importing the random libarary, allows us to generate a random lists of colours to test our function
import random

# Below is the program signature that we were required to use as is:
def follow_instructions(instructions: list[str]) -> list[int]:
    
    # The function below helps us recursively visit each index and record the indexes that have been visited.
    def visit(index: int) -> list[int]:

        #The if statement below allows us to stop the recursion once the index goes outside the list.
        if index >= len(instructions):
            return []

        # This gets the colour at the current index that we are visiting:
        colour = instructions[index]

        #Below we have our if, else if statements and else statements:

        # If the colour is blue, we search for the next blue in the list.
        # We then move to the element immediately after that blue as we were required to do such:
        if colour == "blue":
            try:
                next_blue = instructions.index("blue", index + 1)
            except ValueError:
                #If there is no next blue, we then record the current index and stop.
                return [index]
            next_index = next_blue + 1

        #If the colour is red, we calculate the next index using 2 * index + 1 as we were required to do such:
        elif colour == "red":
            next_index = 2 * index + 1

        # If the colour is green, we then move on to the next element in the list.
        elif colour == "green":
            next_index = index + 1

        else:
            #Else, there is another colour other than blue, red or green in which we print out an invalid colour error message:
            raise ValueError(f"Invalid colour at index {index}: {colour}")

        #This adds the current index to our result and recursively visits the next index:
        return [index] + visit(next_index)

    # This starts the recursion from the first element, which is at index 0
    return visit(0)

if __name__ == "__main__":

    #Below tests the example that we were provided in the documentation to check if my function works correctly:
    example = ["blue", "green", "red", "blue", "green", "red"]
    assert follow_instructions(example) == [0, 4, 5] 

    #Below are print statements which display the provided example in the question and the expected outcome:
    print("Example provided in the question:")
    print("Example list: ", example)
    print("Visited indexes: ", follow_instructions(example))
    print()

    #These are the three possible colours that can appear in our generated lists:
    colours = ["blue", "red", "green"]

    # This generates two random lists, one with 15 elements and one with 18 elements.
    # I used a fixed seed value so that the same lists are generated each time the code is run:
    for test_number, (seed, length) in enumerate([(42, 15), (100, 18)], start=1):
        generator = random.Random(seed)
        instructions = [generator.choice(colours) for _ in range(length)]

        # Lastly i used print statements below, that displays the generated lists and indexes visited by my function:
        print(f"Test {test_number}")
        print("Generated list: ", instructions)
        print("Visited indexes: ", follow_instructions(instructions))
        print()
