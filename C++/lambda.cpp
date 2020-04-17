#include <iostream>

int main()
{
	double a, b;
	char c;
	std::cin >> a >> c >> b;
	auto f = [c](double a, double b) -> double
	{
		if (c == '+') return a + b;
		if (c == '-') return a - b;
		if (c == '*') return a * b;
		if ((c == '/') && (b != 0)) return a / b; else return 0;
	};
	std::cout << f(a, b);
	return 0;
}