positionsConst = ['QB', 'WR1', 'WR2', 'RB1', 'RB2', 'TE']

def getPlayerName(Players, player_id):
  name = Players.query.filter_by(PlayerID=player_id).first()
  return f'{name.PlayerFname} {name.PlayerLname}'

def getPlayerNames(Players, roster):
  player_ids = [roster.QB, roster.WR1, roster.WR2, roster.RB1, roster.RB2, roster.TE]
  names = {
    'QB': '',
    'WR1': '',
    'WR2': '',
    'RB1': '',
    'RB2': '',
    'TE': ''
  }
  for pid, pos in zip(player_ids, positionsConst):
    name = Players.query.filter_by(PlayerID=pid).first()
    names[pos] = f'{name.PlayerFname} {name.PlayerLname}'

  return names

def getRosterPlayers(Players, User, rosters):
  players = []
  for r in rosters:
    owner = User.query.filter_by(RosterID = r.RosterID).first()
    player_ids = [r.QB, r.WR1, r.WR2, r.RB1, r.RB2, r.TE]
    obj = {
      'names': {
        'QB': '',
        'WR1': '',
        'WR2': '',
        'RB1': '',
        'RB2': '',
        'TE': ''
      },
      'points': 0,
      'owner': owner.username
    }
    for pid, pos in zip(player_ids, positionsConst):
      name = Players.query.filter_by(PlayerID=pid).first()
      obj['names'][pos] = f'{name.PlayerFname} {name.PlayerLname}'
    players.append(obj)
  return players
