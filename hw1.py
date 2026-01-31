import random
import math

# Ordered weather states (forms the "bell curve axis")
weather_states = ["sunny", "cloudy", "rainy", "stormy", "snowy"]


# -------------------------------
# WEATHER PREDICTION (Gaussian State Model)
# -------------------------------
def predict_weather_from_last_year(last_year_weather, sigma=1.0):
    last_year_weather = last_year_weather.lower()
    
    if last_year_weather not in weather_states:
        raise ValueError("Invalid weather state entered.")
    
    center_index = weather_states.index(last_year_weather)
    
    probabilities = []
    
    # Gaussian probability across state positions
    for i in range(len(weather_states)):
        exponent = -((i - center_index) ** 2) / (2 * sigma ** 2)
        prob = math.exp(exponent)
        probabilities.append(prob)
    
    # Snow suppression rule
    if last_year_weather != "snowy":
        snow_index = weather_states.index("snowy")
        probabilities[snow_index] *= 0.3  # Dramatically reduce snow chance
    
    # Normalize
    total = sum(probabilities)
    probabilities = [p / total for p in probabilities]
    
    predicted_weather = random.choices(weather_states, weights=probabilities, k=1)[0]
    
    return predicted_weather, dict(zip(weather_states, probabilities))


# -------------------------------
# TEMPERATURE PREDICTION (Stochastic Bell Curve)
# -------------------------------
def predict_temperature_stochastic(last_year_temp, uncertainty_level=5.0):
    noise = random.gauss(0, uncertainty_level)
    predicted_temp = last_year_temp + noise
    return round(predicted_temp, 2), round(noise, 2)


# -------------------------------
# MAIN PROGRAM
# -------------------------------
def main():
    print("=== Stochastic Weather & Temperature Predictor ===\n")
    
    # User-friendly inputs
    last_year_temp = float(input("Enter last year's temperature (°C): "))
    last_year_weather = input("Enter last year's weather (sunny/cloudy/rainy/stormy/snowy): ").strip().lower()
    
    # Predictions
    weather_prediction, weather_probs = predict_weather_from_last_year(last_year_weather)
    temp_prediction, temp_noise = predict_temperature_stochastic(last_year_temp)
    
    # Output
    print("\n--- Weather Probability Distribution (Bell Curve Model) ---")
    for state, prob in weather_probs.items():
        print(f"{state.capitalize():<8}: {prob:.2f}")
    
    print("\n--- Forecast Result ---")
    print(f"Predicted Weather: {weather_prediction.capitalize()}")
    print(f"Predicted Temperature: {temp_prediction}°C (noise added: {temp_noise}°C)")
    print("\nModel: Gaussian state distribution + stochastic temperature noise")


if __name__ == "__main__":
    main()
