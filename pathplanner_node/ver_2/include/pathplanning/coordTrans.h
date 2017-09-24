#pragma once
#include <vector>
#include <iostream>
#include <cmath>
#include <string>
#include <math.h>
using namespace std;


class coordTrans
{
public:
    coordTrans();
    coordTrans(vector<int> afrobitOffset, const double atheta);
    ~coordTrans();
    void setParams(vector<int> afrobitOffset, const double atheta);
    vector<double> calcPPrime(vector<double> point);
    int testThis();
    //Parameters for the frobits coordinate system
    vector<int> frobitOffset;
    double theta; //Running from -pi to +pi
    vector<vector<double>> rotationMatrix;
private:

    int objectId;

};
