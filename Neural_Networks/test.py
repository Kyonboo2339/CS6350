import numpy as np

# layer_1 = np.ones([3,2])
# print(layer_1)

# L = .5
# loss = np.array([[.5, 1]])

# x = np.array([[1, 2]])
# print(loss)

# deriv_2 = (layer_1*loss)
# deriv_2 = np.sum(deriv_2, axis= 1, keepdims=True)
# print(deriv_2)
# print(np.matmul(deriv_2, x))

# print(layer_1- 2)

def half(x):
    return x/2

func = np.vectorize(half)

a = np.ones(shape=(3,3))
b = np.array([[1,2,3]])
print(a*b)
# print(np.sum(layer_1, axis=0, keepdims=True))


