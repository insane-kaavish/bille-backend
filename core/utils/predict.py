def mean_absolute_error(true_values, forecast):
    # Calculate Mean Absolute Error
    n = len(true_values)
    return sum(abs(true_values[i] - forecast[i]) for i in range(n)) / n

# Function to perform Holt-Winters Exponential Smoothing
def holt_winters_exponential_smoothing(data, alpha, beta, gamma, seasonal_periods):
    n = len(data)
    level = [0] * n
    trend = [0] * n
    seasonal = [0] * n
    forecast = [0] * n

    # Initialize the level, trend, and seasonal components
    level[0] = data[0]
    trend[0] = data[1] - data[0]
    seasonal[:seasonal_periods] = [data[i] - level[0] for i in range(seasonal_periods)]

    # Perform Holt-Winters Exponential Smoothing
    for t in range(1, n):
        level[t] = alpha * (data[t] - seasonal[t % seasonal_periods]) + (1 - alpha) * (level[t - 1] + trend[t - 1])
        trend[t] = beta * (level[t] - level[t - 1]) + (1 - beta) * trend[t - 1]
        seasonal[t % seasonal_periods] = gamma * (data[t] - level[t]) + (1 - gamma) * seasonal[t % seasonal_periods]
        forecast[t] = level[t] + trend[t] + seasonal[t % seasonal_periods]

    return forecast

def get_alpha(test_units,test_data):
    metrics = {}
    for alpha_value in range(1, 10):
        alpha = alpha_value / 10.0  # Convert to a decimal between 0 and 1

        # Perform Holt-Winters Exponential Smoothing
        forecast = holt_winters_exponential_smoothing(test_units, alpha, beta=0.7, gamma=0.7, seasonal_periods=12)
        # Calculate MAE
        mae = mean_absolute_error(test_units[-len(forecast):], forecast)

        # Store the alpha value and the corresponding MAE
        metrics[alpha] = mae

    # get best alpha from min mae
    best_alpha = min(metrics, key=metrics.get)

    return best_alpha

def predict(units):
    # get test data from last index in units
    test_data = units[-1]
    test_units = units[:-1]

    # get best alpha
    optimal_alpha = get_alpha(test_units,test_data)

    # Perform Holt-Winters Exponential Smoothing For Prediction
    forecast = holt_winters_exponential_smoothing(units, optimal_alpha, beta=0.7, gamma=0.7, seasonal_periods=12)

    # predicted forecast
    forecast = forecast[-1]

    return int(forecast)
