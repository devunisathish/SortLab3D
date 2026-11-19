# SortLab 3D

Local web-based sorting visualizer. It compiles and runs built-in C sorting code with GCC, captures JSON events emitted by the C executable, and replays those events in the browser.

Algorithms: Bubble, Selection, Insertion, Quick, Merge, Heap, Counting and Radix Sort.

## Requirements
Python 3.9+ and GCC available on PATH.

## Windows
1. Extract the ZIP.
2. Install GCC (MSYS2 MinGW-w64 is one option) and add its bin folder to PATH.
3. In this folder run `py -m pip install -r requirements.txt`
4. Run `py app.py`
5. Open http://127.0.0.1:5000

Linux/macOS: `python3 -m pip install -r requirements.txt`, then `python3 app.py`.

Caveat: the C executable generates a recorded trace, which the UI replays; this is not an interactive native debugger pause. Only built-in algorithms are compiled, not arbitrary submitted C code. Localhost-only educational prototype. Inputs: 2–40 integers from 0–99.


## HOW TO RUN THIS SYSTEM

1. python -m venv venv
2. venv\Scripts\activate
3. pip install -r requirements.txt
4. python -c "import flask; print('Flask installed successfully')"
Flask installed successfully IT SHOULD PRINT
5. python app.py
6. COPY / OPEN THE IP ADDRESS