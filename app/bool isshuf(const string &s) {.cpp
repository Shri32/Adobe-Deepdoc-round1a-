bool isshuf(const string &s) {
    return s.find("FFT") != string::npos || s.find("NTT") != string::npos;
}

string shuf(string s) {
    if (!isshuf(s)) return s;

    default_random_engine engine(time(0));  

    int a = 0;
    do {
        shuffle(s.begin(), s.end(), engine);
        attempts++;
    } while (isshuf(s) && attempts < 1000);

    return s;
}
int main() {
    int n;
    cin >> n;
    cin.ignore();

    for (int i = 0; i < n; ++i) {
        string s;
        getline(cin, s);
        cout << shuf(s) << endl;
    }

    return 0;
}