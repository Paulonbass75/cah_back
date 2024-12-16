import json

# Load JSON data from a file
with open('D:/Code/my_first/cah_cards_full.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Access the nested data
for pack in data:
    print(f"Pack Name: {pack['name']}")
    for card in pack['white']:
        print(f"White Card Text: {card['text']}, Pack: {card['pack']}")
    if 'black' in pack:
        for card in pack['black']:
            print(f"Black Card Text: {card['text']}, Pack: {card['pack']}")