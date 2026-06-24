from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
import numpy as np

actual = [4,5,3,4]
predicted = [4.1,4.8,3.2,4.3]

mae = mean_absolute_error(
    actual,
    predicted
)

rmse = np.sqrt(
    mean_squared_error(
        actual,
        predicted
    )
)

print("MAE:", mae)
print("RMSE:", rmse)
