# 算法与数据结构：从基础到机器人路径规划

双击 index.html 可离线打开课程首页。

- 已制作页面：阶段 0 至阶段 6 的全部规划课程。阶段 1 页面支持自定义数组、预设、逐步操作与自动播放。
- `build_tools/` 集中存放构建脚本、课程正文和示例生成数据；`assets/` 存放网页样式和交互脚本。
- 其他阶段的目录按学习规划展示为待制作，不代表已完成。


数组课程支持指针与区间状态的逐步动画；可使用上一步、下一步或自动播放。开启系统减少动态效果选项时将关闭过渡动画。

课程网页在 `lessons/stage-阶段号/`，完整代码页面及源码在 `codes/stage-阶段号/`。

带图课程支持多种预设：图结构可修改节点数、连边及搜索起终点；网格地图支持选择形状与尺寸，并通过格子表编辑障碍、起点、终点。更改后重新生成演示轨迹，完整代码页仍提供课程固定示例。

在项目根目录运行以下命令，更新全部网页与示例源码：

```powershell
python build_tools/build.py
```

根目录的 `index.html` 是网站首页，`lessons/` 是课程页面，`codes/` 是完整代码页面与源码，`assets/` 是网页资源，`build_tools/` 是构建与维护文件。


阶段 4–6 已提供18课：经典算法设计、图论最短路径、机器人规划。每课包含原理、手算表、正确性解释、边界反例、分层练习、三组预设与完整 C++17 / Python 3 程序。动态规划有状态表，带权图有权值与结果边，D* Lite 展示保留 g/rhs 的增量修复，RRT / RRT* 展示连续采样树，轨迹课分别绘制位置、速度、加速度。

阶段 5.3、6.1 支持点击编辑地图、切换地图形状、设置起终点，并比较 A* 与 h=0 搜索；阶段 7 保留为课程规划。

维护检查（在项目根目录运行）：

```powershell
python build_tools/build.py
python build_tools/verify_advanced.py
```

`verify_advanced.py` 包含随机小样本交叉核对与18组独立程序运行检查；C++ 编译器路径可在脚本中按本机安装位置修改。浏览器回归脚本 `build_tools/check_advanced_browser.cjs` 需要 Playwright，截图保存在已忽略的 `build_tools/.checks/`。


公式使用与控制笔记相同的本地 MathJax SVG 渲染，双击 HTML 离线阅读也可用。正文段落首行缩进两字符，代码、操作区与公式块不缩进。

栅格演示在格内展示真实状态：BFS 距离、DFS 递归深度、A* 的 w/g/h/f、D* Lite 的 g/rhs；当前示例单步代价 w=1。窄屏可在地图内部横向滚动，数值更新不会改变播放按钮位置。

`build_tools/check_math_grid.cjs` 检查全部课程的公式渲染、正文缩进、格内数值及移动端布局（需要 Playwright）。


窄屏导航：宽度不超过1100px时，目录与侧栏内容改为顶部按钮入口。打开面板后只滚动面板内部，锁定背景课程位置；支持触摸、Esc关闭、面板内链接跳转，以及恢复桌面侧栏布局。共同交互实现保存在 `assets/mobile-panels.js` 和 `assets/mobile-panels.css`。

格内数值随搜索发现逐步显示，未发现的格子留空；统一的单步代价1仅在图例说明。D* Lite保留上轮搜索已知状态，再展示修复变化。`build_tools/check_mobile_panels.cjs` 覆盖两套笔记的触摸滚动、背景锁定、位置恢复、目录跳转和尺寸切换检查。


课程阅读顺序统一为：具体场景与小例子 → 大白话步骤 → 交互演示 → 深入原理 → 复杂度与易错反例 → 练习及代码实现入口。正文不再嵌入整段C++程序。完整代码页通过C++ / Python按钮切换，一次展示一种语言，支持下载、复制、键盘切换与语言偏好记忆。

`build_tools/course_flow.py` 维护45课各自的导入例子、操作前问题、易错反例与参考链接；`build_tools/code_teaching.py` 负责代码中文注释、头文件精简与依赖说明。可下载Python程序不携带页面动画事件记录逻辑。RRT基础课不提前混入RRT*重连实现。

`python build_tools/verify_course_code.py` 编译并运行全部45份C++17与45份Python程序（编译器路径可用CXX环境变量指定）；`node build_tools/check_course_flow.cjs` 检查学习顺序、语言切换以及页面代码与下载源码一致性（需要Playwright）。
