import json
from typing import List

def get_param_grid():    
    # Load param_grid from the JSON file
    with open('Prediction\param_grid.json', 'r') as f:
        loaded_param_grid = json.load(f)

    return loaded_param_grid

def initial_trend(series: List, uppercase_m: int) -> float:
    return sum([
        float(series[i+uppercase_m] - series[i]) / uppercase_m 
        for i in range(uppercase_m)
    ]) / uppercase_m

def initial_seasonality(series: List, uppercase_m: int) -> List:
    initial_season = []
    n_seasons = int(len(series)/uppercase_m)

    season_averages = [sum(
        series[uppercase_m * i:uppercase_m * i + uppercase_m]
    ) / uppercase_m for i in range(n_seasons)]

    initial_season.extend([
        sum([series[uppercase_m*j+i]-season_averages[j] 
             for j in range(n_seasons)]) / n_seasons 
        for i in range(uppercase_m)
    ])
    
    return initial_season

def winters_es(series: List,
               uppercase_m: int,
               alpha: float=0.9,
               beta: float=0.9,
               gamma: float=0.9,
               future_steps: int=1) -> List:
    
    i_l = [series[0]]
    i_t = [initial_trend(series, uppercase_m)]
    i_s = initial_seasonality(series, uppercase_m)

    forecasts = []
    for t in range(len(series) + future_steps):

        if t >= len(series):
            k = t - len(series) + 1
            forecasts.append(
                (i_l[-1] + k * i_t[-1]) + i_s[t % uppercase_m]
            )

        else:
            l_t = alpha * (series[t] - i_s[t % uppercase_m]) + (1 - alpha) * (i_l[-1] + i_t[-1])

            i_t[-1] = beta * (l_t - i_l[-1]) + (1 - beta) * i_t[-1]
            i_l[-1] = l_t

            i_s[t % uppercase_m] = gamma * (series[t] - l_t) + (1 - gamma) * i_s[t % uppercase_m]

            forecasts.append(
                (i_l[-1] + i_t[-1]) + i_s[t % uppercase_m]
            )

    return forecasts

def prep_data(units):
    train_data = units[:-1] # all values except the last one
    test_data = units[-1] # last value in the list
    return train_data, test_data
 
def optimal_params(units):
    param_grid = get_param_grid()
    optimal_params = None
    min_error = float('inf')

    train_data, test_data = prep_data(units)
    for params in param_grid:
        alpha, beta, gamma = params
        forecast = winters_es(train_data, 8, alpha, beta, gamma, 1)
        error = abs(test_data - forecast[-1])
        if error < min_error:
            min_error = error
            optimal_params = params

    return optimal_params

def predict(units):
    # get optimal parameters
    opt_params = optimal_params(units)

    # run on optimal parameters
    forecast = winters_es(units, 8, opt_params[0], opt_params[1], opt_params[2], 1)
    
    return int(forecast[-1])
