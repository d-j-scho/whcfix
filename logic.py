import data
def initAppStrings():
    return data.initAppStrings()

class TeamForm(object):
    def __init__(self, teamName, results):
        self.results = results
        self.teamName = teamName

    def __int__(self):
        return self.points()

    def __gt__(self, other):
        return int(self) > int(other)

    def __lt__(self, other):
        return int(self) < int(other)

    def _countRecentResultInitial(self, initial):
        return len([r for r in self.results[:4] if r.resultInitial == initial])

    def wins(self):
        return self._countRecentResultInitial('W')

    def draws(self):
        return self._countRecentResultInitial('D')

    def loses(self):
        return self._countRecentResultInitial('L')

    def points(self):
        return self.wins() * 3 + self.draws()

    def played(self):
        return len(self.results)


class Result(object):
    def __init__(self, resultInitial, resultIndicatorCssClass):
        self.resultInitial = resultInitial
        self.resultIndicatorCssClass = resultIndicatorCssClass

WIN = Result('W', 'win')
LOSE = Result('L', 'lose')
DRAW = Result('D', 'draw')

class Matches(object):

    def __init__(self, listOfMatches):
        self.listOfMatches = listOfMatches

    def getMatches(self, team):
        return [match for match in self.listOfMatches if match.doesFeature(team)]

    def getLastResults(self, listOfTeamNames):
        def _lastResult(team):
            for match in self.listOfMatches[::-1]:
                if match.doesFeature(team) and match.isResult():
                    return match

        lastResults = []
        for team in listOfTeamNames:
            lastResults.append(_lastResult(team))
        return [match for match in lastResults if match is not None]

    def getNextMatches(self, listOfTeamNames):
        def _nextMatch(team):
            teamFixtures = [match for match in self.listOfMatches[::-1] if match.doesFeature(team)]
            for n, match in enumerate(teamFixtures):
                if match.isResult():
                    return teamFixtures[n-1]

        nextMatches = []
        for team in listOfTeamNames:
            nextMatches.append(_nextMatch(team))
        return nextMatches

    def recentForm(self, listOfTeamNames):
        def _getLastFourResults(name):
            results = []
            for match in self.listOfMatches[::-1]:
                if match.doesFeature(name) and match.isResult():
                    if match.didWin(name):
                        results.append(WIN)
                    elif match.didLose(name):
                        results.append(LOSE)
                    elif match.isDraw():
                        results.append(DRAW)
                    else:
                        assert False
                if len(results) == 4:
                    return results

        teams = [(_getLastFourResults(team), team) for team in listOfTeamNames]
        return [TeamForm(name, results) for results, name in teams]


class Match(object):

    def __init__(self, date, time, venue, 
                 home, homeGoals, awayGoals, away, isPostponed, section):
        self.date = date
        self.time = time
        self.venue = venue
        self.home = "%s %s" % (home, section)
        self.homeGoals = homeGoals
        self.awayGoals = awayGoals
        self.away = "%s %s" % (away, section)
        self.isPostponed = isPostponed

    def __str__(self):
        return "%s %s - %s %s" % (self.home, self.homeGoals,
                                  self.awayGoals, self.away)

    def isFixture(self):
        return self.homeGoals == None and self.awayGoals == None

    def isHomeWin(self):
        return self.homeGoals > self.awayGoals

    def isAwayWin(self):
        return self.homeGoals < self.awayGoals

    def isDraw(self):
        return self.homeGoals == self.awayGoals

    def didWin(self, teamName):
        if teamName == self.home:
            return self.isHomeWin()
        elif teamName == self.away:
            return self.isAwayWin()
        else:
            return False

    def doesFeature(self, teamName):
        return teamName == self.home or teamName == self.away

    def doesFeatureSearch(self, teamNameSubString):
        return teamNameSubString in self.home or teamNameSubString in self.away

    def didLose(self, teamName):
        return not self.didWin(teamName) and not self.isDraw()

    def isResult(self):
        return self.homeGoals is not None and self.awayGoals is not None


def getMatchObjectFromDict(matchDict, section):
    date = matchDict['date']
    time = matchDict['time']
    venue = matchDict['venue']
    home = matchDict['home']
    homeGoals = matchDict['homeGoals']
    awayGoals = matchDict['awayGoals']
    isPostponed = matchDict['isPostponed']
    away = matchDict['away']
    return Match(date, time, venue, home, homeGoals, awayGoals, away,
                 isPostponed, section)

def getMatchesObject(mensLeagueId, womensLeagueId, clubId):
    mens = data.getMatchDicts(mensLeagueId, clubId)
    mens = [getMatchObjectFromDict(m, "Mens") for m in mens]
    
    womens = data.getMatchDicts(womensLeagueId, clubId)
    womens = [getMatchObjectFromDict(m, "Ladies") for m in womens]
    matches = mens + womens
    print len(matches)
    return Matches(matches)


def getConfig():
    return data.getConfig()
