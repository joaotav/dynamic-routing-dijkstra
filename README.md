# Dynamic Routing Visualization

This project simulates dynamic routing within a network based on a network topology received as input. The simulation generates routing trees and updates route weights using Dijkstra's algorithm for optimal path identification. For each iteration, the program saves the network configuration as a graph using GraphViz.

## Requirements

To run the program in this repository, you will need:

- **Python 3**: Ensure you have `python3` installed on your system. You can download it from [the official Python website](https://www.python.org/downloads/). You will also need to install the `NumPy` python library.

You can install `NumPy` using `pip`, the Python package installer. Run the following command in your terminal application:

```
pip install numpy
```
- **GraphViz**: This program requires GraphViz, an open source graph visualization software, to generate visualizations for the routing trees. You can install GraphViz by using the following command:

```
sudo apt install graphviz
```

## Usage

Clone this repository using the following command:

   ```
   git clone https://github.com/joaotav/dynamic-routing-dijkstra.git
   ```

Navigate into the cloned repository's directory and run the script with the following command:

```
python3 dynamic_routing.py -i <INPUT_MATRIX> -o <OUTPUT_FILE> -t <TIME_INTERVAL> -n <N_ITERATIONS>
```

Where:
- `<INPUT_MATRIX>` is the name of the file containing the adjacency matrix.
- `<OUTPUT_FILE>` is the name for the configuration file for GraphViz.
- `<TIME_INTERVAL>` defines the time interval in seconds for route generation and update.
- `<N_ITERATIONS>` defines the number of iterations with `<TIME_INTERVAL>` seconds between each.

### Input File Format:

The input file should contain the adjacency matrix representing the network topology. The first line should specify the matrix dimensions, followed by the matrix itself, where each line represents a row. A `0` indicates the absence of a link between two routers, and a `1` represents the presence of a direct link. For example:

```
4 4
0 1 0 0
1 0 1 0
0 1 0 1
0 0 1 0
```

### Output:

The script will generate a routing tree for each iteration and each vertex/router. A global routing tree image will also be generated within the program's folder for each iteration. Additionally, a `history.txt` file will be created to log the routing paths and their minimum distances in each iteration.

### Example Execution

Initiate a simulation with `4` iterations, updating route weights every `5` seconds.

```
python3 dynamic_routing_visualization.py -i matrix.txt -o graphviz.dot -t 5 -n 4
```

#### Routing path history:

```
2024-03-24 17:39:22.250761

Router --- Minimum Distance --- Path
0 -> 0		0		0
0 -> 1		18		0 1
0 -> 2		27		0 1 2
0 -> 3		45		0 1 2 3
--------------------------------------------------
2024-03-24 17:39:22.271071

Router --- Minimum Distance --- Path
1 -> 0		10		1 0
1 -> 1		0		1
1 -> 2		9		1 2
1 -> 3		27		1 2 3
--------------------------------------------------
2024-03-24 17:39:22.289872

Router --- Minimum Distance --- Path
2 -> 0		15		2 1 0
2 -> 1		5		2 1
2 -> 2		0		2
2 -> 3		18		2 3
--------------------------------------------------
2024-03-24 17:39:22.308852

Router --- Minimum Distance --- Path
3 -> 0		21		3 2 1 0
3 -> 1		11		3 2 1
3 -> 2		6		3 2
3 -> 3		0		3
--------------------------------------------------
2024-03-24 17:39:27.354143

Router --- Minimum Distance --- Path
0 -> 0		0		0
0 -> 1		22		0 1
0 -> 2		25		0 1 2
0 -> 3		45		0 1 2 3
--------------------------------------------------
2024-03-24 17:39:27.374333

Router --- Minimum Distance --- Path
1 -> 0		16		1 0
1 -> 1		0		1
1 -> 2		3		1 2
1 -> 3		23		1 2 3
--------------------------------------------------
2024-03-24 17:39:27.393686

Router --- Minimum Distance --- Path
2 -> 0		17		2 1 0
2 -> 1		1		2 1
2 -> 2		0		2
2 -> 3		20		2 3
--------------------------------------------------
2024-03-24 17:39:27.412934

Router --- Minimum Distance --- Path
3 -> 0		30		3 2 1 0
3 -> 1		14		3 2 1
3 -> 2		13		3 2
3 -> 3		0		3
--------------------------------------------------
2024-03-24 17:39:32.460360

Router --- Minimum Distance --- Path
0 -> 0		0		0
0 -> 1		29		0 1
0 -> 2		37		0 1 2
0 -> 3		47		0 1 2 3
--------------------------------------------------
2024-03-24 17:39:32.480666

Router --- Minimum Distance --- Path
1 -> 0		23		1 0
1 -> 1		0		1
1 -> 2		8		1 2
1 -> 3		18		1 2 3
--------------------------------------------------
2024-03-24 17:39:32.499903

Router --- Minimum Distance --- Path
2 -> 0		31		2 1 0
2 -> 1		8		2 1
2 -> 2		0		2
2 -> 3		10		2 3
--------------------------------------------------
2024-03-24 17:39:32.519278

Router --- Minimum Distance --- Path
3 -> 0		38		3 2 1 0
3 -> 1		15		3 2 1
3 -> 2		7		3 2
3 -> 3		0		3
--------------------------------------------------
2024-03-24 17:39:37.567055

Router --- Minimum Distance --- Path
0 -> 0		0		0
0 -> 1		26		0 1
0 -> 2		36		0 1 2
0 -> 3		54		0 1 2 3
--------------------------------------------------
2024-03-24 17:39:37.588523

Router --- Minimum Distance --- Path
1 -> 0		23		1 0
1 -> 1		0		1
1 -> 2		10		1 2
1 -> 3		28		1 2 3
--------------------------------------------------
2024-03-24 17:39:37.607535

Router --- Minimum Distance --- Path
2 -> 0		41		2 1 0
2 -> 1		18		2 1
2 -> 2		0		2
2 -> 3		18		2 3
--------------------------------------------------
2024-03-24 17:39:37.626653

Router --- Minimum Distance --- Path
3 -> 0		58		3 2 1 0
3 -> 1		35		3 2 1
3 -> 2		17		3 2
3 -> 3		0		3
```
