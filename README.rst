**********************************
 ICC Test Cricket Ranking Package
**********************************

:Date: April 7, 2012
:Version: 0.1
:Authors: Berian James
:Web site: https://github.com/berianjames/ICCRankings
:Copyright: This document has been placed in the public domain.
:License: This code is released under the MIT license.
:Requires: BeautifulSoup4, urllib2, datetime, dateutil

====================
ICC Rankings package
====================

ICCRankings.py is a module to obtain and update the `ICC Test Cricket rankings`__. To get started, run ``python test_script.py`` from the command line and explore the results.

.. __: http://icc-cricket.yahoo.net/match_zone/team_ranking.php

The ICC Test Cricket rankings are computed with statistical methodology that has not been publically verified by the ICC. `This algorithm`__ has been followed in the construction of this module, and appears to function correctly. Nevertheless, slight differences may be noticed with respect to the `online predictor`__, as this implementation does not remove the impact of series that are more than three years old, or downweight series that are more than 18 months old, as the official algorithm supposedly requires. 

.. __: http://en.wikipedia.org/wiki/ICC_Test_Championship#Test_championship_calculations

.. __: http://icc-cricket.yahoo.net/match_zone/test_predictor.php

The purpose of this package is to study the ranking methodology currently used by the ICC and to consider whether an alternative system---in particular, the Elo rating system---will perform better.

Module details
==============

The module provides three classes: Team, Series, and TeamDict.

* A Team object contains a unicode team name, rating points, matches played, rating in rounded and floating-point form, and a datetime.date representing the timestamp for these data.

* A Series object takes two Team objects, a number of matches, wins for each team and a datestamp. Draws are inferred from these data. Note that matches returning No Result should be excluded from the Series object; ties are considered to be draws for rating purposes. A Series object will also hold the resulting series points for each team. 

* A TeamDict object is a dictionary of Teams, with keys set to the Team name, and a datestamp for the dictionary data. Printing a TeamDict will automatically order the teams in the dictionary by their ratings and output a formatted table. Teams can be appended to the dictionary using the .append(Team) method. A Series result can be incorporated into the team dictionary using the .add_series(Series) method.

In addition, the module provides one function, get_current_teams, to pull the current ranking data from the ICC website into a TeamDict object.

Typical use
===========

Typical use of the module might be to obtain the current ranking data from the ICC website, create a Series representing a future test series to be played (with predicted results input), and then update the ranking data based on that result. The driver script test_script.py shows how this is done.
