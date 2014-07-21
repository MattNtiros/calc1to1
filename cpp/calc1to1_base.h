#ifndef CALC1TO1_IMPL_BASE_H
#define CALC1TO1_IMPL_BASE_H

#include <boost/thread.hpp>
#include <ossie/Resource_impl.h>
#include <ossie/ThreadedComponent.h>

#include <bulkio/bulkio.h>

class calc1to1_base : public Resource_impl, protected ThreadedComponent
{
    public:
        calc1to1_base(const char *uuid, const char *label);
        ~calc1to1_base();

        void start() throw (CF::Resource::StartError, CORBA::SystemException);

        void stop() throw (CF::Resource::StopError, CORBA::SystemException);

        void releaseObject() throw (CF::LifeCycle::ReleaseError, CORBA::SystemException);

        void loadProperties();

    protected:
        // Member variables exposed as properties
        unsigned short operation;
        std::complex<double> operand;
        bool trig_input;

        // Ports
        bulkio::InDoublePort *input_double;
        bulkio::OutDoublePort *output_double;

    private:
};
#endif // CALC1TO1_IMPL_BASE_H
