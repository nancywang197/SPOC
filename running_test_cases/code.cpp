#include <iostream>
#include <vector>

int main() {
  int n;
  std::cin >> n;
  int cur = 1, cnt = 0;
  std::vector<int> ans;
  for (int i = 0; i < n; i++) {
    int x;
    std::cin >> x;
    if (x == cur) {
      cnt++;
      cur++;
    } else {
      ans.push_back(cnt);
      cnt = 1;
      cur = 2;
    }
    if (i == n - 1) { ans.push_back(cnt); }
  }
  std::cout << (int)ans.size() << std::endl;
  for (int i = 0; i < (int)ans.size(); i++) {
    if (i > 0) std::cout << " ";
      std::cout << ans[i];
  }
  std::cout << std::endl;
  return 0;
}