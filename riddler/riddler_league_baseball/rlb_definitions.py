'''
Riddler League Baseball, also known as the RLB, consists of three teams: the Mississippi Moonwalkers, the Delaware Doubloons and the Tennessee Taters.

Each time a batter for the Moonwalkers comes to the plate, they have a 40 percent chance of getting a walk and a 60 percent chance of striking out. Each batter for the Doubloons, meanwhile, hits a double 20 percent percent of the time, driving in any teammates who are on base, and strikes out the remaining 80 percent of the time. Finally, each batter for the Taters has a 10 percent chance of hitting a home run and a 90 percent chance of striking out.

During the RLB season, each team plays an equal number of games against each opponent. Games are nine innings long and can go into extra innings just like in other baseball leagues. Which of the three teams is most likely to have the best record at the end of the season?
'''
from random import choices
from random import uniform
import itertools
from time import gmtime, strftime

class Team:
    def __init__(self, name, k_rate, bb_rate, hr_rate, double_rate):
        self.name = name
        self.k_rate = k_rate
        self.bb_rate = bb_rate
        self.hr_rate = hr_rate
        self.double_rate = double_rate
        
    def print_rates(self):
        print(f'strikeout rate: {round(self.k_rate,2)}, walk rate: {round(self.bb_rate,2)}, double rate: {round(self.double_rate,2)}, home run rate: {round(self.hr_rate,2)}')

    def have_at_bat(self):
        baseball_options = ['k', 'bb', 'hr', 'double']
        return choices(baseball_options, [self.k_rate, self.bb_rate, self.hr_rate, self.double_rate])[0]
        
    def play_inning(self):
        score = 0
        outs = 0
        baserunners = [0,0,0]
        while outs < 3:
            outcome = self.have_at_bat()
            if outcome == 'k':
                outs += 1
            elif outcome == 'bb':
                if baserunners[0] == 0:
                    baserunners[0] = 1
                elif sum(baserunners) == 3:
                    score += 1
                else:
                    baserunners[2] = baserunners[1]
                    baserunners[1] = baserunners[0]
            elif outcome == 'double':
                score += sum(baserunners)
                baserunners = [0, 1, 0]
            else:
                score += (sum(baserunners) + 1)
                baserunners = [0, 0, 0]
        return score

class Game:
    score = [0, 0]
    inning = 0

    def __init__(self, visitor, home):
        self.visitor = visitor
        self.home = home
        self.result = {'away':visitor.name, 'home':home.name, 'away_score': 0, 'home_score': 0, 'total_innings': 9, 'winner': None, 'loser': None, 
        'extra_innings': False}
    def print_scoreboard(self):
        print(f'After {self.inning} innings, the score is: {self.visitor.name}: {self.score[0]}, {self.home.name}: {self.score[1]}')

    def play_ball(self):
        self.score = [0, 0]
        self.inning = 0
        while self.inning < 9:
            self.score[0] += self.visitor.play_inning()
            self.inning += .5
            self.score[1] += self.home.play_inning()
            self.inning += .5
            if self.inning == 8:
                self.score[0] += self.visitor.play_inning()
                self.inning += .5
                if self.score[1] > self.score[0]:
                    self.result['away_score'] = self.score[0]
                    self.result['home_score'] = self.score[1]
                    self.result['total_innings'] = self.inning
                    self.result['winner'] = self.home.name
                    self.result['loser'] = self.visitor.name
                    return self.result
                else:
                    self.score[1] += self.home.play_inning()
                    self.inning += .5
                while self.score[0] == self.score[1]:
                    self.result['extra_innings'] = True
                    self.score[0] += self.visitor.play_inning()
                    self.inning += .5
                    self.score[1] += self.home.play_inning()
                    self.inning += .5
                self.result['away_score'] = self.score[0]
                self.result['home_score'] = self.score[1]
                self.result['total_innings'] = self.inning
                if self.score[1] > self.score[0]:
                    self.result['winner'] = self.home.name
                    self.result['loser'] = self.visitor.name                    
                else:
                    self.result['winner'] = self.visitor.name
                    self.result['loser'] = self.home.name                    
                return self.result

def make_random_team(name = f'Random Team-{strftime("%Y-%m-%d %H:%M:%S", gmtime())}', k_rate = None):
    if k_rate == None:
        k_rate = uniform(0, 1)
    bb_rate = uniform(0, 1 - k_rate)
    double_rate = uniform(0, 1 - k_rate - bb_rate)
    hr_rate = uniform(0, 1 - k_rate - bb_rate - double_rate)
    return Team(name=name, k_rate=k_rate, bb_rate=bb_rate, hr_rate=hr_rate, double_rate=double_rate)

def simulation(teams=[make_random_team(name='Random1'), make_random_team(name='Random2')], num=10_000):
    game_types = list(itertools.permutations(teams,2))
    sim_results = []
    for _ in range(num):
        for matchup in game_types:
            game = Game(visitor=matchup[0], home=matchup[1]).play_ball()
            sim_results.append(game)
    return sim_results