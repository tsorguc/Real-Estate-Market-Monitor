import numpy as np
from utils.logger import logging

def demonstrate_numpy_features():
    """
    Demonstrates NumPy array creation and vectorized operations.
    As per Lab 8 requirements.
    """
    logging.info("--- NumPy Foundations ---")
    
    # 1. Create NumPy arrays using 4+ methods
    # Method 1: From a list (e.g., sample property prices)
    prices_list = [350000, 420000, 580000, 290000, 950000, 1200000]
    arr_prices = np.array(prices_list)
    
    # Method 2: Using arange (e.g., indices)
    arr_indices = np.arange(len(prices_list))
    
    # Method 3: Using zeros or ones (e.g., placeholder for ratings)
    arr_ones = np.ones((2, 3), dtype=float)
    
    # Method 4: Using random (e.g., simulated growth factors)
    arr_random = np.random.rand(6)
    
    # Print attributes for one of the arrays
    logging.info(f"Price Array - Shape: {arr_prices.shape}, Dtype: {arr_prices.dtype}, Ndim: {arr_prices.ndim}")
    print(f"📊 Price Array - Shape: {arr_prices.shape}, Dtype: {arr_prices.dtype}, Ndim: {arr_prices.ndim}")

    # 2. Vectorized arithmetic - no Python loops for math
    # Calculate price after a 5% increase
    increased_prices = arr_prices * 1.05
    logging.info(f"Increased Prices (vectorized): {increased_prices}")
    
    # Calculate price per sqft (simulated)
    sqft_list = [1500, 1800, 2200, 1200, 3500, 4500]
    arr_sqft = np.array(sqft_list)
    price_per_sqft = arr_prices / arr_sqft
    logging.info(f"Price per SqFt (vectorized): {price_per_sqft}")

    # Return some structured results for the pipeline
    return {
        "mean_price": np.mean(arr_prices),
        "max_price": np.max(arr_prices),
        "total_sqft": np.sum(arr_sqft)
    }

if __name__ == "__main__":
    results = demonstrate_numpy_features()
    print(results)
