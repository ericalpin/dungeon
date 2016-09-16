import random

player_base_health, player_base_defense, player_base_strike = [11, 2, 2]
inv = { 'dagger': 1 }
goblin_counters = { 'health point': 0, 'defense point': 0, 'strike point': 0 }
curr_loot = []
loot_options = ['ruby','coin','strike point','health point','defense point']
player = { 'health': player_base_health, 'defense': player_base_defense, 'strike': player_base_strike }
base_goblin = { 'health': 8, 'defense': 3, 'strike': 2 }
goblins_fought = 0

def generateValues(attacker):
  results = []
  if attacker == 'player':
    strike = random.randint(0,player['strike'])
    defense = random.randint(0,goblin['defense'])
  else:
    strike = random.randint(0,goblin['strike'])
    defense = random.randint(0,player['defense'])
  results.extend((strike, defense))
  return results

def getLoot():
  results = []
  results_str = ''
  for i in range(3):
    item = loot_options[random.randint(0,len(loot_options)-1)]
    results.append(item)
    if len(results_str) > 0:
      results_str += ', '
    results_str += item
  for x in range(len(results)):
    item = results[x]
    if item in inv.keys():
      inv[item] += 1
    else:
      inv[item] = 1
  setNewStats()
  return results_str

def setNewStats():
  h_points = inv.get('health point', 0)
  d_points = inv.get('defense point', 0)
  s_points = inv.get('strike point', 0)
  player['health'] = player_base_health + h_points
  player['defense'] = player_base_defense + d_points
  player['strike'] = player_base_strike + s_points

def buffGoblin(goblin):
  options = ['health point', 'defense point', 'strike point']
  stats_str = ''
  range_num = 0
  if player['strike'] - goblin['defense'] >= 2 or player['defense'] - goblin['strike']:
    range_num = 2
  else:
    range_num = 1
  for i in range(range_num):
    item = options[random.randint(0,len(options)-1)]
    if item in inv.keys():
      goblin_counters[item] += 1
    else:
      goblin_counters[item] = 1
  new_health = base_goblin['health'] + goblin_counters['health point']
  new_defense = base_goblin['defense'] + goblin_counters['defense point']
  new_strike = base_goblin['strike'] + goblin_counters['strike point']
  stats_str = 'Goblins new stats: HEALTH: ' + str(new_health) + ' DEFENSE: ' + str(new_defense) + ' STRIKE: ' + str(new_strike)
  return stats_str

def createGoblin():
  h_points = goblin_counters.get('health point', 0)
  d_points = goblin_counters.get('defense point', 0)
  s_points = goblin_counters.get('strike point', 0)
  new_health = base_goblin['health'] + h_points
  new_defense = base_goblin['defense'] + d_points
  new_strike = base_goblin['strike'] + s_points
  return { 'health': new_health, 'defense': new_defense, 'strike': new_strike }

def printStats():
  print('Your final stats were... HEALTH: ' + str(player['health']) + ' DEFENSE: ' + str(player['defense']) + ' STRIKE: ' + str(player['strike']) +
        ' GOBLINS FOUGHT: ' + str(goblins_fought))

while True:
  print('Do you want to fight another goblin? Y/N')
  answer = input()
  if answer.lower() == 'y':
    goblins_fought += 1
    goblin = createGoblin()
    turn = 'player'
    while goblin['health'] > 0 and player['health'] > 0:
      strike, defense = generateValues(turn)
      if turn == 'player':
        if strike == defense:
          goblin['health'] -= 1
          print('Your strike and the goblin\'s defense were EQUAL so you did 1 point of damage')
        elif strike > defense:
          diff = strike - defense
          goblin['health'] -= diff
          print('Your strike was GREATER than the goblin\'s defense so you did ' + str(diff) + ' point(s) of damage')
        else:
          print('The goblin completely blocked your strike')
      else:
        if strike == defense:
          player['health'] -= 1
          print('The goblin\'s strike and your defense were EQUAL so you took 1 point of damage')
        elif strike > defense:
          diff = strike - defense
          player['health'] -= diff
          print('The goblin\'s strike was GREATER than the your defense so you took ' + str(diff) + ' point(s) of damage')
        else:
          print('You completely blocked the goblin\'s strike')
      print('YOU: ' + str(player['health']) + ' GOBLIN: ' + str(goblin['health']))
      print('Press any key to continue to fight...')
      press = input()
      if turn == 'player':
        turn = 'goblin'
      else:
        turn = 'player'
    if goblin['health'] <= 0:
      loot_str = getLoot()
      goblin_str = buffGoblin(goblin)
      print('You defeated the goblin!')
      print('Your loot was: ' + loot_str)
      print('Your new stats: HEALTH: ' + str(player['health']) + ' DEFENSE: ' + str(player['defense']) + ' STRIKE: ' + str(player['strike']))
      print(goblin_str)
    else:
      print('You were defeated!')
      printStats()
      break
  else:
    printStats()
    break