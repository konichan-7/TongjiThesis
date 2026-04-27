这是一份按照学术论文体例整理的关于平面五连杆机构雅可比矩阵与虚拟模型控制（VMC）力矩映射的推导报告。在双轮足等复杂机器人的分层轻量化控制框架中，此类底层静力学映射尤为关键，它使得内环独立计算的腿长支撑力（如基于重力前馈与腿长 PID 计算得到的作用力）与期望力矩能够被精准转化为底层关节电机的执行力矩。

***

# 平面五连杆机构雅可比解析推导与 VMC 力矩映射理论分析

## 摘要
[cite_start]虚拟模型控制（VMC）通过在机器人工作空间构造虚拟元件产生期望的虚拟力，并利用雅可比矩阵将其映射为关节空间力矩 [cite: 43][cite_start]。本文针对双电机驱动的平面五连杆机构，首先建立其闭环正运动学模型。为避免直接对高度非线性的正运动学方程求偏导带来的符号膨胀与计算灾难，本文采用基于速度映射与微分几何约束的方法解析推导了机构的雅可比矩阵 [cite: 61, 62][cite_start]。最后，基于虚功原理，严格推导了从末端工作空间虚拟力向底层电机驱动力矩的静力学映射关系 [cite: 53]。

## 1. 机构描述与正运动学建模
[cite_start]在平面五连杆机构中，定义转动副 A 和 E 为主动关节，分别由两台电机驱动，其关节角记为 $\phi_1$ 和 $\phi_4$ [cite: 27][cite_start]。控制目标主要关注机构末端点 C 的工作空间状态，可分别用直角坐标 $(x_C, y_C)$ 或极坐标 $(L_0, \phi_0)$ 表示 [cite: 27]。

基于闭环矢量法，通过五连杆左右两部分列写点 B 和点 D 到点 C 的几何约束，可建立以下方程：
[cite_start]$$\begin{cases} x_B + l_2 \cos \phi_2 = x_D + l_3 \cos \phi_3 \\ y_B + l_2 \sin \phi_2 = y_D + l_3 \sin \phi_3 \end{cases}$$ [cite: 31]
消去 $\phi_3$ 后，可求解出被动关节角 $\phi_2$ 随主动关节变化的非线性解析式：
[cite_start]$$\phi_2 = 2 \arctan\left(\frac{B_0 + \sqrt{A_0^2 + B_0^2 - C_0^2}}{A_0 + C_0}\right)$$ [cite: 33]
进而可得末端点 C 的直角坐标系正运动学映射：
[cite_start]$$\begin{cases} x_C = l_1 \cos \phi_1 + l_2 \cos \phi_2 \\ y_C = l_1 \sin \phi_1 + l_2 \sin \phi_2 \end{cases}$$ [cite: 39]

## 2. 雅可比矩阵的解析推导
[cite_start]雅可比矩阵 $J$ 描述了关节空间速度（或微小位移）到工作空间速度（或微小位移）的线性映射关系，即 $\delta x = J \delta q$ [cite: 52][cite_start]。对于上述包含复杂嵌套和反三角函数的正运动学解析解，直接调用符号运算工具求导会得到极其复杂的结果，难以部署于运算资源受限的 MCU 等嵌入式平台 [cite: 61]。

因此，本文采用**对位置方程隐式求导提取速度映射系数**的方法。对点 C 的正运动学方程求时间导数：
[cite_start]$$\begin{cases} \dot{x}_C = -l_1 \dot{\phi}_1 \sin \phi_1 - l_2 \dot{\phi}_2 \sin \phi_2 \\ \dot{y}_C = l_1 \dot{\phi}_1 \cos \phi_1 + l_2 \dot{\phi}_2 \cos \phi_2 \end{cases}$$ [cite: 64]
为消去中间不可测变量 $\dot{\phi}_2$，对闭环约束等式求导得：
[cite_start]$$\begin{cases} \dot{x}_B - l_2 \dot{\phi}_2 \sin \phi_2 = \dot{x}_D - l_3 \dot{\phi}_3 \sin \phi_3 \\ \dot{y}_B + l_2 \dot{\phi}_2 \cos \phi_2 = \dot{y}_D + l_3 \dot{\phi}_3 \cos \phi_3 \end{cases}$$ [cite: 68]
消去 $\dot{\phi}_3$ 即可解析解出 $\dot{\phi}_2$ 关于已知参量的表达式：
[cite_start]$$\dot{\phi}_2 = \frac{(\dot{x}_D - \dot{x}_B)\cos \phi_3 + (\dot{y}_D - \dot{y}_B)\sin \phi_3}{l_2 \sin(\phi_3 - \phi_2)}$$ [cite: 71]
将该式代回末端速度方程，并经过三角函数两角和差公式的化简合并，最终可提取出只包含基础三角函数的标准雅可比矩阵形式：
[cite_start]$$\begin{bmatrix} \dot{x}_C \\ \dot{y}_C \end{bmatrix} = J \begin{bmatrix} \dot{\phi}_1 \\ \dot{\phi}_4 \end{bmatrix}$$ [cite: 114]
[cite_start]这种基于速度映射推导出的 $J$ 避免了根号与复杂代数分式，大幅提升了控制周期的实时计算效率 [cite: 61, 75]。

## 3. 基于虚功原理的力矩映射
[cite_start]在获取了表征运动微分关系的雅可比矩阵后，需建立动力学或静力学层面的力/力矩映射。根据虚功原理（Principle of Virtual Work），处于平衡状态的系统，其在任意兼容的微小虚位移下，外力所做总虚功为零 [cite: 53]。

假设系统输入侧的电机执行力矩向量为 $T = \begin{bmatrix} T_1 & T_2 \end{bmatrix}^T$，关节产生的微小虚位移为 $\delta q$；工作空间末端输出对抗环境的虚拟力向量为 $F$，末端产生的微小虚位移为 $\delta x$。
电机力矩输入的虚功为 $T^T \delta q$。
末端向环境输出虚拟力的做功为 $(-F)^T \delta x$。
由能量守恒建立虚功平衡方程：
[cite_start]$$T^T \delta q + (-F)^T \delta x = 0$$ [cite: 55]
将微分运动学关系 $\delta x = J \delta q$ 代入上式得：
$$T^T \delta q - F^T (J \delta q) = 0$$
$$(T^T - F^T J) \delta q = 0$$
由于 $\delta q$ 是任意独立的微小虚位移，其系数矩阵必须恒为零，即 $T^T = F^T J$。等式两端取转置，最终推导出极其重要的静力学映射核心公式：
[cite_start]$$T = J^T F$$ [cite: 58]

## 4. 极坐标系下的完整控制映射闭环
[cite_start]在双轮足机器人等实际应用中，内环控制器（如用于腿长控制的 PID 或重力前馈）通常输出的是沿极径方向的腿推力 $F$ 和控制姿态的髋关节扭矩 $T_p$ [cite: 44][cite_start]。需要通过坐标变换矩阵将其转换到直角坐标系下 [cite: 122]。

首先，利用变换矩阵 $M$ 将极坐标系下的期望力向量 $[F, T_p]^T$ 映射为末端沿 $L_0$ 及其垂向的虚拟力 $[F_t, F_c]^T$：
$$\begin{bmatrix} F_t \\ F_c \end{bmatrix} = M \begin{bmatrix} F \\ T_p \end{bmatrix}$$
[cite_start]随后，利用旋转矩阵 $R$ 将力向量旋转到全局的 XY 直角坐标系中，得到 $[F_x, F_y]^T$ [cite: 118]：
$$\begin{bmatrix} F_x \\ F_y \end{bmatrix} = R \begin{bmatrix} F_c \\ F_t \end{bmatrix}$$
[cite_start]最终，将直角坐标系的期望力代入前述推导的虚功方程 $T = J^T F$ 中，即可获得完整串联的控制算法部署级力矩映射公式 [cite: 124, 125]：
[cite_start]$$\begin{bmatrix} T_1 \\ T_2 \end{bmatrix} = J^T R M \begin{bmatrix} F \\ T_p \end{bmatrix}$$ [cite: 125]