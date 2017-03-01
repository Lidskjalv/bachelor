#pragma once
#include <string>
#include <iostream>
#include <vector>
#include <fstream>
using namespace std;
class MapHandler
{
public:
	MapHandler();
	~MapHandler();
	void loadFromFile(string aFileName);
	vector<vector<int>>* getMapPtr();
	void writeToFile(vector<vector<int>> * outPutMap, string aFileName);
private:
	vector<vector<int>> * mapPtr;
	vector<vector<int>> map;
	int xPos, yPos, height, width;

};

