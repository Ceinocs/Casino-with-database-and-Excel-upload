import random

simvols = ['🍒', '🍋', '🍇']
item = simvols[random.randint(0, 2)]
item_2 = simvols[random.randint(0, 2)]
item_3 = simvols[random.randint(0, 2)]
point_to_add = 0
if (item == item_2 == item_3 == '🍒'):
    point_to_add = 20
if (item == item_2 == item_3 == '🍋'):
    point_to_add = 40
if (item == item_2 == item_3 == '🍇'):
    point_to_add = 80

print(point_to_add)



print(item,item_2,item_3)