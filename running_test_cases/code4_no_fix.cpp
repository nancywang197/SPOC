#include "CommonLibs.h"
//row 20 
void fastIo() {}
int main() {
  fastIo();
  int n, m;
  cin >> n >> m;
  char MAT[n][m];
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < m; j++) cin >> MAT[i][j];
  }
  int LC = m, RC = -1, TR = n, BR = -1;
  for (int i = 0; i < n; i++) {
    bool first = false;
    for (int j = 0; j < m; j++) {
      if (MAT[i][j] == '*') {
        if (!first) {
          LC = min(LC, j);
          first = true;
        }
        RC = max(RC, j);
      }
    }
  }
  for (int j = 0; j < m; j++) {
    bool first = false;
    for (int i = 0; i < n; i++) {
      if (MAT[i][j] == '*') {
        if (!first) { TR = min(TR, i); }
        BR = max(BR, i);
      }
    }
  }
  for (int i = TR; i <= BR; i++) {
    for (int j = LC; j <= RC; j++) { cout << MAT[i][j]; }
    cout << '\n';
  }
}
