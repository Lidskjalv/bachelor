#include "astar.h"
#include <vector>
#include "MapHandler.h"
using namespace std;

int main(int argc, char** argv) {
	MapHandler handler;
	handler.loadFromFile(argv[1]);
	vector<vector<int> > testMap = { { 0, 0, 0, 0 ,9 ,0, 0, 0, 0 ,0 }, 
									{ 1, 1, 1 ,1 ,1, 1, 1, 1, 0 ,0 },
									{ 0, 1, 1 ,1 ,1, 0, 0, 0, 0 ,0 },
									{ 0, 1, 1 ,1 ,0, 0, 0, 0, 0 ,0 },
									{ 0, 0, 0 ,0 ,0, 0, 0, 0, 0 ,0 },
									{ 0, 0, 0 ,0 ,0, 0, 0, 0, 0 ,0 },
									{ 0, 1, 1 ,1 ,1, 1, 1 ,1 ,1, 1 },
									{ 0, 1, 1 ,1 ,1, 1, 1 ,1 ,1, 1 },
									{ 0, 0, 0 ,0 ,0, 0, 0, 0, 0 ,0 },
									{ 0, 0, 0 ,0 ,0, 0, 0, 0, 0 ,0 } };
	vector<vector<int>> * mapPtr = &testMap;
	aStar dummy(handler.getMapPtr(), 1, 1, 500, 300);
	handler.writeToFile(dummy.getMap(), "testoutput1.txt");
	return 0;
}
