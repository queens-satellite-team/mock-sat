#include <iostream>
#include "header.h"

using namespace std;

LatLng::LatLng(int lat, int lng) {
    this.lat = lat;
    this.lng = lng;
}

EulerAngles::EulerAngles(LatLng satLocation) {
    //What my people are working on
}

EulerAngles Request::getLocationOfSat(LatLng) {
    // Find location inorbit where sat is closest to photo location
}

Request::Request(LatLng photo) {
    locationOfPhoto = photo;
    locationOfSat = getLocationOfSat(photo);
    ea = EulerAngles(photo);
}
