#include "calc1to1_base.h"

/*******************************************************************************************

    AUTO-GENERATED CODE. DO NOT MODIFY

    The following class functions are for the base class for the component class. To
    customize any of these functions, do not modify them here. Instead, overload them
    on the child class

******************************************************************************************/

calc1to1_base::calc1to1_base(const char *uuid, const char *label) :
    Resource_impl(uuid, label),
    ThreadedComponent()
{
    loadProperties();

    input_double = new bulkio::InDoublePort("input_double");
    addPort("input_double", input_double);
    output_double = new bulkio::OutDoublePort("output_double");
    addPort("output_double", output_double);
}

calc1to1_base::~calc1to1_base()
{
    delete input_double;
    input_double = 0;
    delete output_double;
    output_double = 0;
}

/*******************************************************************************************
    Framework-level functions
    These functions are generally called by the framework to perform housekeeping.
*******************************************************************************************/
void calc1to1_base::start() throw (CORBA::SystemException, CF::Resource::StartError)
{
    Resource_impl::start();
    ThreadedComponent::startThread();
}

void calc1to1_base::stop() throw (CORBA::SystemException, CF::Resource::StopError)
{
    Resource_impl::stop();
    if (!ThreadedComponent::stopThread()) {
        throw CF::Resource::StopError(CF::CF_NOTSET, "Processing thread did not die");
    }
}

void calc1to1_base::releaseObject() throw (CORBA::SystemException, CF::LifeCycle::ReleaseError)
{
    // This function clears the component running condition so main shuts down everything
    try {
        stop();
    } catch (CF::Resource::StopError& ex) {
        // TODO - this should probably be logged instead of ignored
    }

    Resource_impl::releaseObject();
}

void calc1to1_base::loadProperties()
{
    addProperty(operation,
                0,
                "operation",
                "",
                "readwrite",
                "",
                "external",
                "configure");

    addProperty(operand,
                std::complex<double>(0.0,0.0),
                "operand",
                "",
                "readwrite",
                "",
                "external",
                "configure");

    addProperty(trig_input,
                true,
                "trig_input",
                "",
                "readwrite",
                "",
                "external",
                "configure");

}


