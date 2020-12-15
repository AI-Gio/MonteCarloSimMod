import pandas as pd

"__==** Middle Squared Method Section**==__"
def findMid(num, seed_length):
    """
    Finds the number of middle numbers based on the seed length in the given number
    :param num: the square of the seed number/ the past middle number
    :param seed_length: the length of the number you start with (seed)
    :return: string with the middle number of "num"
    """
    number = str(num)
    newNum = number[1:]
    while True:
        if len(newNum) < seed_length:
            newNum += "000"
        if len(newNum) == seed_length:
            return newNum
        newNum = newNum[:-1]
        if len(newNum) == seed_length:
            return newNum
        newNum = newNum[1:]

def MSM(seed, random_num_len):
    """
    Calculates a random numbers using the Middle Squared Method
    :param seed: the number to create the random number and can be inserted again later on to get the same random number back
    :param random_num_len: the number of times the calculation of the new middle number is repeated
    :return: a string that contains the generated random number
    """
    random_str = ""
    num = seed
    for i in range(random_num_len):
        newNum = findMid(num**2, len(str(seed)))
        random_str += newNum
        num = int(newNum)
    return random_str

"__==** Monte Carlo Simulation Soccer Matches Section**==__"
def matchgame(home, rand_num):
    """
    calculates the result of the match
    :param home: list with the chances: win, tie, lose
    :param rand_num: 2 digit random number
    :return: home_points, away_points (int)
    """
    win = home[0]
    tie = home[0] + home[1]
    lose = sum(home)
    if int(rand_num) <= win:
        return 3, 0
    elif tie >= int(rand_num) > win:
        return 1, 1
    elif lose >= int(rand_num) > tie:
        return 0, 3

def competition(chance_matrix, ran_str):
    """
    Plays all of the matches in a pool and updates the points the teams get
    :param chance_matrix: matrix with the chances of winning/tie/losing for all of the teams
    :param ran_str: a 40 char string with random numbers
    :return: the status of points for each team after all of the matches are played (list)
    """
    rankings = [['ajax', 0], ['feynoord', 0], ['psv', 0], ['fcutrecht', 0], ['willem2', 0]]

    for h_i, home in enumerate(chance_matrix):
        for a_i, away in enumerate(chance_matrix[h_i]):
            if away == []:
                continue
            home_points, away_points = matchgame(away, ran_str[:2])
            rankings[h_i][1] += home_points
            rankings[a_i][1] += away_points
            ran_str = ran_str[2:]
    return rankings

def simulation(ran_str, run_times, df):
    """
    Gives the possibility to run competitions multiple times and creates an overview with the chance of placements for each team
    :param ran_str: a string with a random number
    :param run_times: the number of times a competition is being played
    :param df: a pandas df with as index the teams and as columns the possible placements
    :return: a pandas df with for each team the chance in percentage of what placement they get
    """
    if (run_times * 40) > len(ran_str):
        print("You need to create a larger random number. Try a larger seed or increase the repetition value")
        return None

    for i in range(run_times):
        rankings_sorted = sorted(competition(match_chances, ran_str[:41]), key = lambda x: x[1], reverse=True)
        for index, team in enumerate(rankings_sorted):
            df.at[team[0], (index+1)] += 1
        ran_str = ran_str[41:]
    df = df.apply(lambda x: x / run_times * 100)
    return df

"__==** Run Section **==__"
# indexes are based on order ajax, feynoord, psv, fc utrecht, willem II
match_chances = [[[],[65,17,18],[54,21,25],[74,14,12],[78,13,9]],
                 [[30,21,49],[],[37,24,39],[51,22,27],[60,21,19]],
                 [[39,22,39],[54,22,24],[],[62,20,18],[62,22,16]],
                 [[25,14,61],[37,23,40],[29,24,47],[],[52,23,25]],
                 [[17,18,65],[20,26,54],[23,24,53],[37,25,38],[]]]

ranks = pd.DataFrame({'Team': ['ajax', 'feynoord', 'psv', 'fcutrecht', 'willem2'],
                   1: [0, 0, 0, 0, 0],
                   2: [0, 0, 0, 0, 0],
                   3: [0, 0, 0, 0, 0],
                   4: [0, 0, 0, 0, 0],
                   5: [0, 0, 0, 0, 0]
                   })
ranks = ranks.set_index('Team')

random_number = MSM(93485902348275093847, 100000)
print(simulation(random_number, 10000, ranks))