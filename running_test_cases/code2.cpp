#include <iostream>
#include <map>
using namespace std;
map<string, int> m;
map<string, int>::iterator it;
int main() {
  int n;
  cin >> n;
  getchar();
  for (int i = 0; i < n; i++) {
    string str;
    getline(cin, str);
    m[str] = 1;
  }
  int ans = 0;
  for (it = m.begin(); it != m.end(); it++) { ans++; }
  cout << ans << endl;
}
