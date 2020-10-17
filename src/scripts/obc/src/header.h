#include <iostream>
#include <queue> 
#pragma once

using namespace std;

class LatLng {
    public:
        LatLng(int lat, int lng);
    private:
        int lat;
        int lng;
};

class EulerAngles {
    public:
        EulerAngles(LatLng satLocation);
    private:
        int yaw;
        int pitch;
        int roll;
}

class Request {
    Public:
    // Given a location of where the sat needs to to take the picture
    EulerAngles getLocationOfSat(LatLng)

    private:
        EulerAngles ea;
        LatLng locationOfPhoto;
        LatLng locationOfSat

}



class RequestQueue {
    public:
        queue<Request> theQueue;   
};

EulerAngle getSatLocatoin(LatLng photoLocation) {
    // Find location inorbit where sat is closest to photo location
}