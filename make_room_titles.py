import os
import sys
import random


with open(os.path.join(sys.path[0], 'ingredients.txt'), 'r') as f:
    ingredients = f.read().split("\n")

with open(os.path.join(sys.path[0], 'rooms.txt'), 'r') as f:
    places = f.read().split("\n")


with open(os.path.join(sys.path[0], 'adjectives.txt'), 'r') as f:
    adjectives = f.read().split("\n")

with open(os.path.join(sys.path[0], 'smell_adjectives.txt'), 'r') as f:
    smell_adjectives = f.read().split("\n")

with open(os.path.join(sys.path[0], 'feelings.txt'), 'r') as f:
    feelings = f.read().split("\n")

with open(os.path.join(sys.path[0], 'demons.txt'), 'r') as f:
    demons = f.read().split("\n")


def text_gen():
    title = "123456789012345678901234567890123456789012345678901234567890"

    while len(title) > 50:
        adjective = adjectives[random.randint(0, len(adjectives) - 1)]
        place = places[random.randint(0, len(places) - 1)]
        ingredient = ingredients[random.randint(0, len(ingredients) - 1)]
        title = f'The {adjective.upper()} {ingredient.title()} {place.title()}'

    demon = demons[random.randint(0, len(demons) - 1)]
    adjective2 = smell_adjectives[random.randint(0, len(smell_adjectives) - 1)]
    feeling = feelings[random.randint(0, len(feelings) - 1)]
    description = f'Entering this room fills you with {feeling}. The {adjective2} aroma of {ingredient} fills the air. Watch out for the {demon}!\n'
    return title, description
    
