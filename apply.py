import joblib
from matplotlib import rcParams
import pandas as pd
import crawlerPredict

def predict(index) :
    # print("Please give the index of the match you want to predict:")
    # index = input()
    crawlerPredict.mainClass(index)
    model = joblib.load('predict2.model')
    rcParams['figure.figsize'] = (25, 20)

    df = pd.read_csv('predict.csv', header=None)

    df.columns = ['homeTeam', 'awayTeam', 'fightRateDif', 'fightGoalDif', 'recentRateDif', 'recentGoalDif',
                  'leagueRateDif', 'leagueGoapDif',
                  'supportDif']

    all_info = df[
        ['homeTeam', 'awayTeam', 'fightRateDif', 'fightGoalDif', 'recentRateDif', 'recentGoalDif', 'leagueRateDif',
         'leagueGoapDif',
         'supportDif']].values

    X_var = df[['fightRateDif', 'fightGoalDif', 'recentRateDif', 'recentGoalDif', 'leagueRateDif', 'leagueGoapDif',
                'supportDif']].values
    y_pred = model.predict(X_var)

    for i in range(len(y_pred)-1, len(y_pred)):
        y = y_pred[i]
        homeTeam = all_info[i, 0]
        awayTeam = all_info[i, 1]
        if y == 0:
            # print("Team %s will get victorious" % awayTeam)
            return "Team " + awayTeam + " will get victorious"
        elif y == 1:
            # print("The two teams will play to a draw")
            return "The two teams will play to a draw"
        else:
            # print("Team %s will get victorious" % homeTeam)
            return "Team " + homeTeam + " will get victorious"
