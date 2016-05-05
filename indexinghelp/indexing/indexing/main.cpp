//
//  main.cpp
//  indexing
//
//  Created by desiree on 5/4/16.
//  Copyright (c) 2016 Desiree Lenart. All rights reserved.
//

#include <iostream>
#include <string>
using namespace std;

int main(int argc, const char * argv[]) {
    int page;
    int i=0;
    int day=5; //Friday
    int count = 0;
    for (i=180; i>=158; i-=4)
    {
        page = i;
        cout << "} else if (new Date(1930, 12, "<< day <<").getTime() <= selectedDate) {volume = ['08', " << page << "];\n";
        day--;
        count++;
        if(count ==5) //account for weekends
            day -=2;
    }
    return 0;
}
