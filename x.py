import numpy as np

# ReLU激活函数
def relu(x):
    return np.maximum(0, x)

# 初始化参数
A = np.array([[1, -1], [1, 1]])
B = np.array([[1], [2]])
C = np.array([[-1, 1]])

# 初始隐藏状态
h = np.array([[0], [0]])

# 输入序列
X = [3, 4, 5, 6]

# 用于存储每一时间步的输出
outputs = []

# RNN前向传播
for x in X:
    h = relu(A.dot(h) + B * x)
    print(h)
    y = C.dot(h)
    outputs.append(y)

# 输出每一时间步的隐藏状态和输出
print("Hidden states and outputs for each time step:")
for t in range(len(X)):
    print(f"Time step {t+1}: Hidden state: {h}, Output: {outputs[t]}")
