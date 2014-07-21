#include <iostream>
#include "ossie/ossieSupport.h"

#include "calc1to1.h"
int main(int argc, char* argv[])
{
    calc1to1_i* calc1to1_servant;
    Resource_impl::start_component(calc1to1_servant, argc, argv);
    return 0;
}

