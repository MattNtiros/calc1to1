#ifndef CALC1TO1_IMPL_H
#define CALC1TO1_IMPL_H

#include "calc1to1_base.h"
#include "Calc.h"

using std::vector;
using std::cout;
using std::endl;

#define PI 3.14159265

class calc1to1_i;

class calc1to1_i : public calc1to1_base
{
	ENABLE_LOGGING
public:
	calc1to1_i(const char *uuid, const char *label);
	~calc1to1_i();
	int serviceFunction();

	unsigned short last_operation;
	vector<double> data;


	template<typename T, typename U, typename V>
	void doMath(vector<T> &in1, U &in2, vector<V> &d)
	{
		typedef typename Calc<T, U>::output_type typeIneed;
		vector<typeIneed> *castedData = (vector<typeIneed>*)&d;
		castedData->resize(in1.size());
		for(unsigned int i=0;i<castedData->size();i++)
		{
			Calc<T, U> math(in1[i], in2);
			switch(operation){
			case 0: // add
				(*castedData)[i] = math.add();
				break;
			case 1: // subtract
				(*castedData)[i] = math.subtract();
				break;
			case 2: // divide
				(*castedData)[i] = math.divide();
				break;
			case 3: // multiply
				(*castedData)[i] = math.multiply();
				break;
			case 4: // pow
				(*castedData)[i] = math.power();
				break;
			default:
				std::cerr << "Error: default case in switch statement called.. should never be called" << endl;
				break;
			}

		}
	}

	template<typename T, typename U, typename V>
	void doCalculation(vector<T> &in1, U &in2, vector<V> &d)
	{
		if(operation<5)
			doMath(in1, in2, d);
		else
		{
			double trig_f = 1;
			if(!trig_input)
				trig_f = M_PI/180;
			vector<T> *castedData = (vector<T>*)&d;
			castedData->resize(in1.size());
			for(unsigned int i=0;i<in1.size();i++)
			{
				switch(operation)
				{
				case 5: // sin
					(*castedData)[i] = sin(in1[i]*trig_f);
					break;
				case 6: // cos
					(*castedData)[i] = cos(in1[i]*trig_f);
					break;
				case 7: // tan
					(*castedData)[i] = tan(in1[i]*trig_f);
					break;
				default:
					std::cerr << "Error: default case in switch statement called.. should never be called" << endl;
					break;
				}
			}
		}
	}

};

#endif
