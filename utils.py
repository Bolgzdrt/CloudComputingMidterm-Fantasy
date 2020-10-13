from functools import reduce

positionsConst = ['QB', 'WR1', 'WR2', 'RB1', 'RB2', 'TE']
gameConst = ['Game1', 'Game2', 'Game3', 'Game4', 'Game5', 'Game6', 'Game7', 'Game8', 'Game9', 'Game10', 'Game11', 'Game12', 'Game13', 'Game14', 'Game15', 'Game16']

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

def getRosterPlayers(Players, User, Team, rosters):
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
    player_scores = getPlayerScores(r, Team, Players)
    obj['points'] = reduce(lambda acc, curr: acc + player_scores[curr], player_scores, 0)
    for pid, pos in zip(player_ids, positionsConst):
      name = Players.query.filter_by(PlayerID=pid).first()
      obj['names'][pos] = f'{name.PlayerFname} {name.PlayerLname}'
    players.append(obj)
  return players

def getPlayerStats(roster, Players):
  player_ids = [roster.QB, roster.WR1, roster.WR2, roster.RB1, roster.RB2, roster.TE]
  stats = {
    'QB': '',
    'WR1': '',
    'WR2': '',
    'RB1': '',
    'RB2': '',
    'TE': ''
  }
  for pid, pos in zip(player_ids, positionsConst):
    stat = Players.query.filter_by(PlayerID=pid).first()
    stats[pos] = f'{stat.TotalYardage}'

  return stats

def getPlayerScores(roster, Team, Players):
  player_ids = [roster.QB, roster.WR1, roster.WR2, roster.RB1, roster.RB2, roster.TE]
  player_teams = []
  for p in player_ids:
    player_teams.append(Players.query.filter_by(PlayerID=p).first().TeamID)

  scores = {
    'QB': 0,
    'WR1': 0,
    'WR2': 0,
    'RB1': 0,
    'RB2': 0,
    'TE': 0
  }
  for tid, pos in zip(player_teams, positionsConst):
    team = Team.query.filter_by(TeamID=tid).first()
    for w in range(1, 18):
      scores[pos] += __getUserWeekByWeekScoreHelper(w, team)
    # scores[pos] = Team.query.filter_by(TeamID=tid).first().Game1 + Team.query.filter_by(TeamID=tid).first().Game2 + Team.query.filter_by(TeamID=tid).first().Game3 + Team.query.filter_by(TeamID=tid).first().Game4 +  Team.query.filter_by(TeamID=tid).first().Game5 +  Team.query.filter_by(TeamID=tid).first().Game6 +  Team.query.filter_by(TeamID=tid).first().Game7 +  Team.query.filter_by(TeamID=tid).first().Game8 +  Team.query.filter_by(TeamID=tid).first().Game9 +  Team.query.filter_by(TeamID=tid).first().Game10 + Team.query.filter_by(TeamID=tid).first().Game11 + Team.query.filter_by(TeamID=tid).first().Game12 + Team.query.filter_by(TeamID=tid).first().Game13 + Team.query.filter_by(TeamID=tid).first().Game14 + Team.query.filter_by(TeamID=tid).first().Game15 + Team.query.filter_by(TeamID=tid).first().Game16

  return scores

def getUserWeekByWeekScore(roster, Players, Team, User):
  owner = User.query.filter_by(RosterID = roster[-1]).first()
  score = [0 for x in range(17)]
  for week in range(1, 18):
    for p in roster[:-1]:
      player_data = Players.query.filter_by(PlayerID=p).first()
      team = Team.query.filter_by(TeamID=player_data.TeamID).first()
      score[week-1] += __getUserWeekByWeekScoreHelper(week, team)

  return {
    'owner': owner.username,
    'weekly_score': score,
    'total': reduce(lambda acc, curr: acc + curr, score, 0)
  }

# Doesn't let you index with f'Game{i}' so gotta do it the bad way...
def __getUserWeekByWeekScoreHelper(week, team):
  options = {
    1: team.Game1,
    2: team.Game2,
    3: team.Game3,
    4: team.Game4,
    5: team.Game5,
    6: team.Game6,
    7: team.Game7,
    8: team.Game8,
    9: team.Game9,
    10: team.Game10,
    11: team.Game11,
    12: team.Game12,
    13: team.Game13,
    14: team.Game14,
    15: team.Game15,
    16: team.Game16,
    17: team.Game17
  }
  return options[week]
