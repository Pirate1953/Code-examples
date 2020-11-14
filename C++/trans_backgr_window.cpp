#include <windows.h>
#include <stdio.h>

HWND winHandle;
HDC hdc;
PAINTSTRUCT ps;
POINT p;
HANDLE threadHandle;

/**
 * Adds text to the cursor and moves with cursor (using cursor coordinates)
 *
 * @param lParam - The thread data passed to the function
 *
 * @return indicates the success or failure of this function
 */
DWORD WINAPI AddTextToCursor(void* lParam);

/**
 * An application-defined function that processes messages sent to a window
 *
 * @param hwnd - A handle to the window
 * @param msg - The message
 * @param param - Additional message information. The contents of this parameter depend on the value of the msg parameter
 * @param lparam - Additional message information. The contents of this parameter depend on the value of the msg parameter
 *
 * @return the result of the message processing and depends on the message sent
 */
LRESULT CALLBACK WindowProcessMessages(HWND hwnd, UINT msg, WPARAM param, LPARAM lparam);

/**
 * The Application Entry Point
 *
 * @param currentInstance - A handle to the current instance of the application.
 * @param previousInstance - A handle to the previous instance of the application. This parameter is always NULL
 * @param cmdLine - The command line for the application, excluding the program name
 * @param cmdShow - Flag that says whether the main application window will be minimized, maximized, or shown normally
 *
 * @return If the function succeeds, terminating when it receives a WM_QUIT message, it should return the exit value contained in that message's wParam parameter. If the function terminates before entering the message loop, it should return zero
 */
int WINAPI WinMain(_In_ HINSTANCE currentInstance, _In_opt_ HINSTANCE previousInstance, _In_ PSTR cmdLine, _In_ INT cmdShow) {
	const char* CLASS_NAME = "Win32WindowClass";
	WNDCLASS wc{};
	wc.hInstance = currentInstance;
	wc.lpszClassName = CLASS_NAME;
	wc.hCursor = LoadCursor(nullptr, IDC_ARROW);
	wc.hbrBackground = reinterpret_cast<HBRUSH>(COLOR_GRAYTEXT);
	wc.lpfnWndProc = WindowProcessMessages;
	RegisterClass(&wc);

	// Creates the window
	winHandle = CreateWindowEx(WS_EX_TOPMOST,
		CLASS_NAME, "Transparent background window", WS_OVERLAPPEDWINDOW | WS_VISIBLE,
		50, 50, 600, 600, nullptr, nullptr, nullptr, nullptr);

	hdc = GetDC(winHandle);
	threadHandle = CreateThread(0, 0, &AddTextToCursor, 0, 0, 0); // Creates thread and executes function

	// Window loop
	MSG msg{};
	while (GetMessage(&msg, nullptr, 0, 0)) {
		TranslateMessage(&msg);
		DispatchMessage(&msg); //Dispatches a message to a window procedure
	}

	return 0;
}

LRESULT CALLBACK WindowProcessMessages(HWND hwnd, UINT msg, WPARAM param, LPARAM lparam) {
	switch (msg) {
	case WM_DESTROY: {
		CloseHandle(threadHandle);
		PostQuitMessage(0); //Indicates to the system that a thread has made a request to terminate (quit)
	}
	return 0;
	default:
		return DefWindowProc(hwnd, msg, param, lparam); //Calls the default window procedure to provide default processing for any window messages that an application does not process
	}
}

DWORD WINAPI AddTextToCursor(void* lParam) {
	SetBkMode(hdc, TRANSPARENT);
	SetTextAlign(hdc, TA_CENTER);
	SetBkColor(hdc, RGB(0, 0, 0));
	SetTextColor(hdc, RGB(0, 255, 0));

	while (true) {
		GetCursorPos(&p);
		ScreenToClient(winHandle, &p);
		TextOut(hdc, p.x, p.y, "Cursos", strlen("Cursos"));
	}
}