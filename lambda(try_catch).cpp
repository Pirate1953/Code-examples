#include <iostream>

int main()
{
	double a, b;
	char c;
	std::cin >> a >> c >> b;
	auto f = [c](double a, double b)
	{
		if (c == '+') std::cout << a + b;
		if (c == '-') std::cout << a - b;
		if (c == '*') std::cout << a * b;
		if (c == '/')
		{
			try
			{
				if (b == 0)
				{
					throw 0;
				}
				std::cout << a / b;
			}
			catch (int thr)
			{
				if (thr == 0)
				{
					std::cout << "Division by zero!!!";
				}
			}
		}
	};
	f(a, b);
	return 0;
}
