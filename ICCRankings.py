import datetime
from bs4 import BeautifulSoup
import urllib2

class Team:

    def __init__(self,name=None,points=float('nan'),matches=float('nan'),
                 date=datetime.date.today()):
        """Define a team."""
        self.name = name
        self.points = points
        self.matches = matches
        self.rating = self.points / self.matches
        self.frating = float(self.points) / self.matches
        self.date = datetime.date.today()
        return

    def __str__(self):
        """Display team information."""
        return str( "Name: %s\nDate: %s\nPoints: %s\nMatches: %s\nRating: %s (%.3f)\n" % ( 
                self.name,
                self.date,
                self.points,
                self.matches,
                self.rating, self.frating ) )

    def __shortstr__(self):
        """Display team data in a single line, perhaps for use in a table."""
        return str( "{0:15} {1:^6n} {2:^8n} {3:4n} ({4:.4f})\n".format(
                    self.name, self.points, self.matches, 
                    self.rating, self.frating) )

class Series:

    def __init__(self,teamA=None,teamB=None,nmatches=float('nan'),
                 winsA=float('nan'),winsB=float('nan'),
                 date = datetime.date.today()):
        """Define a series."""
        # Parse series data
        self.nmatches = nmatches
        self.teamA = teamA
        self.teamB = teamB
        self.winsA = winsA
        self.winsB = winsB
        self.draws = self.nmatches - self.winsA - self.winsB
        self.date = date

        ## Compute series points
        # One point for each win, half point for a draw ...
        self.pointsA = self.winsA + 0.5*self.draws
        self.pointsB = self.winsB + 0.5*self.draws

        # ... and one point to series winner or half point to each
        if self.winsA > self.winsB:
            self.pointsA += 1
        elif self.winsA < self.winsB:
            self.pointsB += 1
        else:
            self.pointsA += 0.5
            self.pointsB += 0.5

        return


    def __str__(self):
        """Display series information"""
        fullstr = "{0} vs. {1}, {2} matches\n".format(
                self.teamA.name,self.teamB.name,self.nmatches )
        fullstr += "{0:15} {1:3} {2:3}\n".format("Team","Wns","Pts")
        fullstr += "{0:15} {1:3} {2:3}\n".format(self.teamA.name,self.winsA,self.pointsA)
        fullstr += "{0:15} {1:3} {2:3}\n".format(self.teamB.name,self.winsB,self.pointsB)
        return str(fullstr)
                
class TeamDict():

    def __init__(self,date=datetime.date.today()):
        """Define a dictionary of teams."""
        self.date = date
        self.lookup = {}
        self.nteams = len(self.lookup)
        return
 
    def __str__(self):
        fullstr = "\n#  {0:15} {1}  {2}  {3}\n".format(
            "Team","Points","Matches","Rating")
        teamlist = self.rank()
        rank = 0
        for team in teamlist:
            rank += 1
            fullstr = fullstr + str(rank) + '  ' + team.__shortstr__()
        return str(fullstr)

    def append(self,team=Team()):
        """Append Team to TeamDict."""
        self.lookup[team.name] = team
        self.nteams += 1
        return

    def rank(self):
        """Convert TeamDict to ranked list of teams"""
        teamlist = self.lookup.values()
        return sorted(teamlist,key = lambda team: team.frating, reverse=True)
        
    def add_series(self,series):
        """Update to include series."""
        # Get basic team information
        date = series.date
        teamA = self.lookup[series.teamA.name]
        teamB = self.lookup[series.teamB.name]
        spointsA = series.pointsA
        spointsB = series.pointsB

        # Compute points change based on series points and previous rating difference
        if abs(teamA.rating - teamB.rating) < 40:
            dpointsA = spointsA * (teamB.rating + 50)
            dpointsB = spointsB * (teamA.rating + 50)

            dpointsA += spointsB * (teamB.rating - 50)
            dpointsB += spointsA * (teamA.rating - 50)
        else:
            # If team A is the stronger team
            if teamA.rating > teamB.rating:
                dpointsA = spointsA * (teamA.rating + 10)
                dpointsB = spointsB * (teamB.rating + 90)

                dpointsA += spointsB * (teamA.rating - 90)
                dpointsB += spointsA * (teamB.rating - 10)
            else:
                dpointsA = spointsA * (teamA.rating + 90)
                dpointsB = spointsB * (teamB.rating + 10)

                dpointsA += spointsB * (teamA.rating - 10)
                dpointsB += spointsA * (teamB.rating - 90)

        # Compute new points and ratings
        teamA.points += dpointsA
        teamB.points += dpointsB

        teamA.matches += series.nmatches + 1
        teamB.matches += series.nmatches + 1
        
        teamA.rating = round(teamA.points / teamA.matches)
        teamB.rating = round(teamB.points / teamB.matches)
        teamA.frating = float(teamA.points) / teamA.matches
        teamB.frating = float(teamB.points) / teamB.matches

        return

def get_current_teams():

    from dateutil.parser import parse

    # Grab ICC test rankings from webpage
    soup = BeautifulSoup(
        urllib2.urlopen('http://icc-cricket.yahoo.net/match_zone/team_ranking.php')
        )
    table = soup.find_all("table")[0]
    rows = table.find_all('tr')[1:]

    # Parse date -- had to work that 19 out by hand
    rawdate = rows.pop().find_all('td')[-1].text[19:]
    rankingdate = parse(rawdate).date()

    # Generate TeamList from table
    current_teams = TeamDict(date=rankingdate)
    for row in rows:
        name = row.find_all('td')[1].text
        points = int(row.find_all('td')[3].text)
        matches = int(row.find_all('td')[2].text)
        current_teams.append(
            Team(name=name,
                 points=points,
                 matches=matches,
                 date=rankingdate)
            )

    return current_teams

def get_series_history(teamlist=[]):
    import re

    # Grab series list from ESPNcricinfo statsguru
    soup = BeautifulSoup(
        urllib2.urlopen('http://stats.espncricinfo.com/ci/content/records/335431.html')
        )

    tables = soup('table','engineTable')
    history = tables[0]
    future = tables[1]

    # Parse history into rows
    rows = history('tr')[1:]

    # Generate SeriesList from history
    nteamlist = []
    for row in rows:

        # Parse row into parts
        row_data = row('td')
        names_str = row_data[0]('a')[0].contents[0]
        year = row_data[1].contents[0]
        winner = row_data[3].contents[0]
        result = row_data[4].contents

        # Parse team names
        team_loc = [names_str.find(team) for team in teamlist]
        team_found = [loc>0 for loc in team_loc ]

        # Some error checking
        if len(result) == 0: # Skip series with no result data
            continue
        if sum(team_found) < 2: # Series not between two teams in teamlist
            continue
        if sum(team_found) > 2:
            # This (incorrectly) excludes three tests, where one of the teams
            #  named in the list in not playing, but hosting. Should be fixed later.
            # See serieslocs below.
        #    print names_str, team_found
            continue

        # Get team names
        seriesteams = [teamlist[i] for i in range(len(teamlist)) if team_found[i]]
        #serieslocs = [loc[i] for i in range(len(teamlist)) if team_found[i]]

        # Get scores
        scores_list = re.findall(r'\d',result[0])
        nmatches = int(scores_list[2])

        # Put teams and result in series object
        if winner == 'drawn':
            teamA = seriesteams[0]
            teamB = seriesteams[1]
            winsA = int(scores_list[0])
            winsB = int(scores_list[1])
        elif seriesteams[0] == winner:
            teamA = seriesteams[0]
            teamB = seriesteams[1]
            winsA = int(scores_list[0])
            winsB = int(scores_list[1])
        else:
            teamA = seriesteams[1]
            teamB = seriesteams[0]
            winsA = int(scores_list[0])
            winsB = int(scores_list[1])

        print teamA, winsA, ':', winsB, teamB, nmatches 

    return history
    
