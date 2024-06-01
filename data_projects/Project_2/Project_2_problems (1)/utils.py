import numpy as np
import tensorflow as tf

def get_data_extract():
    (X, Y), (X_test, Y_test) = tf.keras.datasets.mnist.load_data()

    X_val = X[55000:]
    Y_val = Y[55000:]
    X = X[:55000]
    Y = Y[:55000]

    prop = 0.3
    train_max_points = np.shape(X)[0]
    val_max_points = np.shape(X_val)[0]
    test_max_points = np.shape(X_test)[0]

    np.random.seed(1031) # this is to ensure the same random subsets
    random_rows_train = np.random.choice(range(0, train_max_points), int(prop * train_max_points), replace=False)
    random_rows_val = np.random.choice(range(0, val_max_points), int(prop * val_max_points), replace=False)
    random_rows_test = np.random.choice(range(0, test_max_points), int(prop * test_max_points), replace=False)

    X = X[random_rows_train, :].reshape(len(random_rows_train), 28 * 28)
    Y = Y[random_rows_train]

    X_val = X_val[random_rows_val, :].reshape(len(random_rows_val), 28 * 28)
    Y_val = Y_val[random_rows_val]

    X_test = X_test[random_rows_test, :].reshape(len(random_rows_test), 28 * 28)
    Y_test = Y_test[random_rows_test]

    return (X/255.0, Y, X_val/255.0, Y_val, X_test/255.0, Y_test)