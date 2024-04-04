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
details = []  # 用于存储详细的计算过程

# RNN前向传播
for x in X:
    # 计算线性组合前的A*h和B*x
    Ah = A.dot(h)
    Bx = B * x
    # 计算新的隐藏状态
    #h = relu(A.dot(h) + B * x)
    h = relu(Ah + Bx)
    # 计算输出
    y = C.dot(h)
    outputs.append(y)
    # 存储详细计算过程
    details.append({'Ah': Ah, 'Bx': Bx, 'h_after_activation': h, 'y': y})

# 输出每一时间步的隐藏状态和输出，以及A*h和B*x
hidden_states_outputs = [(t+1, h, outputs[t]) for t in range(len(X))]
print(details)
