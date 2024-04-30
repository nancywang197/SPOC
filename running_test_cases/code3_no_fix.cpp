#include "CommonLibs.h"
int num[105][105];
int vis[105];
int n;
int counts;
int en;
void dfs(int k) {
  en = k;
  if (k == 1 && vis[1] == 1) return;
  vis[k] = 1;
  for (int i = 1; i <= n; i++) {
    if (vis[i] == 0) {
      if (num[k][i] == -1) {
        if (num[i][k] != -1) {
          counts += num[i][k];
          dfs(i);
        }
      } else {
        dfs(i);
      }
    }
  }
}
int main() {
  int x, y, l;
  int sum;
  while (cin >> n) {
    sum = 0;
    memset(num, -1, sizeof(num));
    memset(vis, 0, sizeof(vis));
    for (int i = 0; i < n; i++) {
      cin >> x >> y >> l;
      num[x][y] = l;
      sum += l;
    }
    counts = 0;
    dfs(1);
    if (num[en][1] == -1) counts += num[1][en];
    cout << min(counts, sum - counts) << endl;
  }
}
