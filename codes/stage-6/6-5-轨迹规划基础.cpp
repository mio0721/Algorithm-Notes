// 轨迹规划基础
// 学习重点：先给出起终位置、速度和加速度要求。
// 选择一条满足边界条件的平滑位移曲线。
// 求速度与加速度，检查峰值是否超过约束。
// C++17；直接编译运行 main() 中的示例。
#include <iostream>  // 控制台输入与输出
#include <algorithm>  // 排序、取最值、合并或反转等标准算法
#include <cmath>  // 距离、幂、平方根或数值判断
#include <iomanip>  // 控制输出精度与格式
#include <stdexcept>  // 明确报告非法输入
#include <array>  // 固定长度坐标或障碍边界

using namespace std;

// 按物理时刻求五次位移曲线及其一、二阶时间导数。
array<double,3> trajectory(double displacement, double duration, double time) {
    // 不符合本算法前提的输入要明确拒绝，不能带着错误条件继续计算。
    if (duration <= 0 || time < 0 || time > duration) throw invalid_argument("invalid time");
    // 把物理时间转换为0到1的归一化时间；求导后仍需除以实际时长。
    double tau = time/duration;
    double s = displacement*(10*pow(tau,3)-15*pow(tau,4)+6*pow(tau,5));
    // 一次时间导数带1/T，得到米每秒。
    double v = displacement/duration*(30*pow(tau,2)-60*pow(tau,3)+30*pow(tau,4));
    // 二次时间导数带1/T²，得到米每二次方秒。
    double a = displacement/(duration*duration)*(60*tau-180*pow(tau,2)+120*pow(tau,3));
    return {s,v,a};
}

// 程序入口：准备示例数据，调用算法，并输出结果供手算核对。
int main() {
    double displacement = 10, maxVelocity = 2, maxAcceleration = 1;
    double duration = max(15.0/8*abs(displacement)/maxVelocity,
                          sqrt(10*sqrt(3.0)/3*abs(displacement)/maxAcceleration));
    // 输出计算结果，便于与课程例子或自行推演的答案核对。
    cout << fixed << setprecision(6) << "T=" << duration << '\n';
    cout << "t,s,v,a\n";
    for (int i = 0; i <= 40; ++i) {
        double time = duration*i/40;
        auto [s,v,a] = trajectory(displacement,duration,time);
        cout << time << ',' << s << ',' << v << ',' << a << '\n';
    }
}
