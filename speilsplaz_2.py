
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Create a simple dataset (5 samples, 2 features)
data = np.array([[1],[2],[3],[4],[5]])

# Initialize MinMaxScaler to scale data between 0 and 1
scaler = MinMaxScaler(feature_range=(0, 1))

# Fit the scaler to the data and transform it
scaled_data = scaler.fit_transform(data)

# Now descaling (inverse scaling)
descaled_data = scaler.inverse_transform(scaled_data)

# Print the original data, scaled data, and descaled data
print("Original Data:")
print(data)
print("\nScaled Data (Min-Max Scaling):")
print(scaled_data)
print("\nDescaled Data (Inverse Min-Max Scaling):")
print(descaled_data)
