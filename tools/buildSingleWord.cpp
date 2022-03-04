#include <bits/stdc++.h>
#define ll long long
#define rep(i, a, b) for (ll i = (a); i <= (b); i++)
#define dec(i, a, b) for (ll i = (a); i >= (b); i--)
#define pll pair<ll, ll>
using namespace std;
ll INF = 0x7f7f7f7f7f7f7f7f;
const int N = 2e5 + 5;

int main() {
#ifdef _DEBUG
  freopen("input.txt", "r", stdin);
  freopen("output.txt", "w", stdout);
#endif
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  string s;
  while (cin >> s) {
    string tmp;
    rep(i, 0, s.size() - 1) { tmp += (char)(s[i] - 32); }
    ll sz = tmp.size();
    cout << tmp << tmp.size() - 1 << " = '" << s[sz - 1] << "'\n";
    dec(i, sz - 2, 1) {
      cout << tmp << i << " = '" << s[i] << "' " << tmp << i + 1 << endl;
    }
    cout << "END_" << tmp << " = '" << s[0] << "' " << tmp << 1 << endl;
  }
  return 0;
}