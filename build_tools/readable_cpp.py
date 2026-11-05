"""Readable main-function bodies for the newer teaching examples."""
BODIES = {
'1.7': '''string s = "abcabcbbd";
unordered_map<char, int> last;
int left = 0, best = 0;

for (int right = 0; right < static_cast<int>(s.size()); ++right) {
    char ch = s[right];
    if (last.count(ch)) {
        // 左边界不能后退。
        left = max(left, last[ch] + 1);
    }
    last[ch] = right;
    best = max(best, right - left + 1);
}

cout << best << endl;''',
'1.8': '''vector<int> a{9, 3, 7, 1, 8, 2, 6, 4, 5};

for (int i = 1; i < static_cast<int>(a.size()); ++i) {
    int value = a[i];
    int j = i - 1;

    // 大于待插入值的元素依次右移。
    while (j >= 0 && a[j] > value) {
        a[j + 1] = a[j];
        --j;
    }
    a[j + 1] = value;
}

for (int value : a) {
    cout << value << " ";
}
cout << endl;''',
'3.1': '''vector<vector<int>> g = GRAPH;
vector<bool> seen(g.size(), false);

function<void(int)> dfs = [&](int u) {
    seen[u] = true;
    cout << char('A' + u) << " ";

    for (int v : g[u]) {
        if (!seen[v]) {
            dfs(v);
        }
    }
};

dfs(0);
cout << endl;''',
'3.2': '''vector<vector<int>> g = GRAPH;
vector<bool> seen(g.size(), false);
stack<int> pending;
pending.push(0);
seen[0] = true;

while (!pending.empty()) {
    int u = pending.top();
    pending.pop();
    cout << char('A' + u) << " ";

    // 倒序压栈，使编号较小的邻居先出栈。
    for (auto it = g[u].rbegin(); it != g[u].rend(); ++it) {
        int v = *it;
        if (!seen[v]) {
            seen[v] = true;
            pending.push(v);
        }
    }
}
cout << endl;''',
'3.3': '''vector<vector<int>> g = GRAPH;
vector<bool> onPath(g.size(), false);
vector<int> path;
const int goal = 9;

function<void(int)> dfs = [&](int u) {
    onPath[u] = true;
    path.push_back(u);

    if (u == goal) {
        for (int v : path) {
            cout << char('A' + v) << " ";
        }
        cout << endl;
    } else {
        for (int v : g[u]) {
            if (!onPath[v]) {
                dfs(v);
            }
        }
    }

    // 撤销当前选择，让其他路径可以使用这个节点。
    path.pop_back();
    onPath[u] = false;
};

dfs(0);''',
'3.4': '''vector<vector<int>> g = GRAPH;
vector<bool> seen(g.size(), false);
queue<int> pending;
pending.push(0);
seen[0] = true;

while (!pending.empty()) {
    int u = pending.front();
    pending.pop();
    cout << char('A' + u) << " ";

    for (int v : g[u]) {
        if (!seen[v]) {
            seen[v] = true;  // 入队时就标记。
            pending.push(v);
        }
    }
}
cout << endl;''',
'3.5': '''vector<vector<int>> children = GRAPH;
queue<int> pending;
pending.push(0);

while (!pending.empty()) {
    // 先保存本层长度，避免把下一层混入当前层。
    int count = static_cast<int>(pending.size());
    for (int i = 0; i < count; ++i) {
        int u = pending.front();
        pending.pop();
        cout << u + 1 << " ";

        for (int v : children[u]) {
            pending.push(v);
        }
    }
    cout << endl;
}''',
'3.6': '''vector<vector<int>> g = GRAPH;
vector<int> parent(g.size(), -1);
vector<int> distance(g.size(), -1);
queue<int> pending;
const int start = 0, goal = 9;
pending.push(start);
distance[start] = 0;

while (!pending.empty()) {
    int u = pending.front();
    pending.pop();

    for (int v : g[u]) {
        if (distance[v] == -1) {
            distance[v] = distance[u] + 1;
            parent[v] = u;
            pending.push(v);
        }
    }
}

if (distance[goal] == -1) {
    cout << "unreachable" << endl;
    return 0;
}

vector<int> path;
for (int u = goal; u != -1; u = parent[u]) {
    path.push_back(u);
}
reverse(path.begin(), path.end());

for (int u : path) {
    cout << char('A' + u) << " ";
}
cout << "steps=" << distance[goal] << endl;''',
'3.7': '''vector<string> grid{"....", ".##.", "...."};
int rows = static_cast<int>(grid.size());
int cols = static_cast<int>(grid[0].size());
vector<vector<bool>> seen(rows, vector<bool>(cols, false));
int dr[]{1, -1, 0, 0};
int dc[]{0, 0, 1, -1};

function<bool(int, int)> dfs = [&](int r, int c) {
    if (r < 0 || r >= rows || c < 0 || c >= cols) {
        return false;
    }
    if (grid[r][c] == '#' || seen[r][c]) {
        return false;
    }

    seen[r][c] = true;
    if (r == rows - 1 && c == cols - 1) {
        return true;
    }

    for (int k = 0; k < 4; ++k) {
        if (dfs(r + dr[k], c + dc[k])) {
            return true;
        }
    }
    return false;
};

cout << (dfs(0, 0) ? "reachable" : "unreachable") << endl;''',
'3.8': '''vector<string> grid{"....", ".##.", "...."};
int rows = static_cast<int>(grid.size());
int cols = static_cast<int>(grid[0].size());
vector<vector<int>> distance(rows, vector<int>(cols, -1));
queue<pair<int, int>> pending;
int dr[]{1, -1, 0, 0};
int dc[]{0, 0, 1, -1};

if (grid[0][0] != '#') {
    pending.push({0, 0});
    distance[0][0] = 0;
}

while (!pending.empty()) {
    auto [r, c] = pending.front();
    pending.pop();

    for (int k = 0; k < 4; ++k) {
        int nr = r + dr[k];
        int nc = c + dc[k];
        if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) {
            continue;
        }
        if (grid[nr][nc] == '#' || distance[nr][nc] != -1) {
            continue;
        }
        distance[nr][nc] = distance[r][c] + 1;
        pending.push({nr, nc});
    }
}

cout << "steps=" << distance[rows - 1][cols - 1] << endl;'''
}

def body(id):
    from graph_examples import graph_for
    code = BODIES[id]
    if 'GRAPH' in code:
        graph, _, _ = graph_for(id)
        rows = ['    {' + ', '.join(map(str, row)) + '}' for row in graph]
        code = code.replace('GRAPH', '{\n' + ',\n'.join(rows) + '\n}')
    return code
