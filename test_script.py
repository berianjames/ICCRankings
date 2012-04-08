import ICCRankings

# Test generation of empty team
x = ICCRankings.Team()
print x

# Test scraping of rankings from ICC
teams = ICCRankings.get_current_teams()
print teams # __str__ will rank teams automatically

# Test generation of series
S1 = ICCRankings.Series( teams.lookup['Australia'],
                        teams.lookup['West Indies'],
                        nmatches = 3, winsA=2, winsB=0 )

S2 = ICCRankings.Series(teams.lookup['Sri Lanka'],
                        teams.lookup['England'],
                        nmatches = 2, winsA=1, winsB=1 )

print S1, S2 # Print series

# Add series results and print updated rankings
teams.add_series(S1)
teams.add_series(S2)
print teams
