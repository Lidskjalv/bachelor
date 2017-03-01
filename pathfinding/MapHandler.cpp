#include "MapHandler.h"



MapHandler::MapHandler()
{
}

MapHandler::~MapHandler()
{
}

void MapHandler::loadFromFile(string aFileName)
{
	char c;
	string line;
	ifstream inputStream(aFileName); //Opening a file with inputStream as identifier
	if (inputStream.is_open())
	{
		getline(inputStream, line); //First line contains the width
		width = stoi(line);
		getline(inputStream, line); //Second line contains the height
		height = stoi(line);
		getline(inputStream, line); //3rd line contains the x position of the robot
		xPos = stoi(line);
		getline(inputStream, line); //4th line contains the y position of the robot
		yPos = stoi(line);
		map.resize(width); //Resizing vector<vector<int>> map
		for (int i = 0; i < width; i++) 
		{
			map[i].resize(height);
		}
		int xi = 0, digit = 0;
		for (int yi = 0; yi < height; yi++) //Loop through all y's
		{
			xi = 0; //X value at each y starts at zero
			
			getline(inputStream, line); //Get one line (All the x's at the y value)
			
			for (int i = 0; i < line.size(); i++)
			{
				
				if (isdigit(line[i])) //IF it's a digit (not a space)
				{
					//cout << xi << " " << yi << endl;
					digit = line[i] - '0'; //Go from char to int
					map[xi][yi] = digit; //Put the digit in the map
					xi++;  //Count x one up
				}
			}
		}
		
	}
	else
		cout << "Unable to open file" << endl;
	inputStream.close();
	
}

vector<vector<int>>* MapHandler::getMapPtr()
{
	mapPtr = &map;
	return mapPtr;
}

void MapHandler::writeToFile(vector<vector<int>>* outputMap, string aFileName)
{
	ofstream outputStream;
	outputStream.open(aFileName);
	outputStream << width << endl << height << endl << 50 << endl << 50 << endl; //Width height and the robots position (50, 50 is just a constant value for now...)
	for (int yi = 0; yi < height; yi++)
	{
		for (int xi = 0; xi < width; xi++)
		{
			outputStream << (*outputMap)[xi][yi] << " ";
		}
		outputStream << endl;
	}

	outputStream.close();


}
