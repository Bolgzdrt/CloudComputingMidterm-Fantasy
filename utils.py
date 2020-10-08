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
  for pid, pos in zip(player_ids, ['QB', 'WR1', 'WR2', 'RB1', 'RB2', 'TE']):
    name = Players.query.filter_by(PlayerID=pid).first()
    names[pos] = f'{name.PlayerFname} {name.PlayerLname}'

  return names
