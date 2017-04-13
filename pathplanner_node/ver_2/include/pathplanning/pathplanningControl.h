#pragma once
#include <vector>
#include <iostream>
#include <cmath>
#include <string>
#include <math.h>
using namespace std;

struct coordsMsg{
    int tx, ty, fx, fy;
    float theta;

};

struct waypoint{
    vector<double> wpX;
    vector<double> wpY;
};

class pathplanningControl
{
public:
    pathplanningControl();
    pathplanningControl();
    ~pathplanningControl();

private:



};
