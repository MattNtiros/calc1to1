#!/usr/bin/env python
import unittest
import ossie.utils.testing
from ossie.utils import sb
import os
import time
import math
from omniORB import any

class ResourceTests(ossie.utils.testing.ScaComponentTestCase):
    """Test for all resource implementations in calc1to1"""

    def startComponent(self):
        #######################################################################
        # Launch the resource with the default execparams
        execparams = self.getPropertySet(kinds=("execparam",), modes=("readwrite", "writeonly"), includeNil=False)
        execparams = dict([(x.id, any.from_any(x.value)) for x in execparams])
        self.launch(execparams)

        #######################################################################
        # Verify the basic state of the resource
        self.assertNotEqual(self.comp, None)
        self.assertEqual(self.comp.ref._non_existent(), False)

        self.assertEqual(self.comp.ref._is_a("IDL:CF/Resource:1.0"), True)

        #######################################################################
        # Validate that query returns all expected parameters
        # Query of '[]' should return the following set of properties
        expectedProps = []
        expectedProps.extend(self.getPropertySet(kinds=("configure", "execparam"), modes=("readwrite", "readonly"), includeNil=True))
        expectedProps.extend(self.getPropertySet(kinds=("allocate",), action="external", includeNil=True))
        props = self.comp.query([])
        props = dict((x.id, any.from_any(x.value)) for x in props)
        # Query may return more than expected, but not less
        for expectedProp in expectedProps:
            self.assertEquals(props.has_key(expectedProp.id), True)

        #######################################################################
        # Verify that all expected ports are available
        for port in self.scd.get_componentfeatures().get_ports().get_uses():
            port_obj = self.comp.getPort(str(port.get_usesname()))
            self.assertNotEqual(port_obj, None)
            self.assertEqual(port_obj._non_existent(), False)
            self.assertEqual(port_obj._is_a("IDL:CF/Port:1.0"),  True)

        for port in self.scd.get_componentfeatures().get_ports().get_provides():
            port_obj = self.comp.getPort(str(port.get_providesname()))
            self.assertNotEqual(port_obj, None)
            self.assertEqual(port_obj._non_existent(), False)
            self.assertEqual(port_obj._is_a(port.get_repid()),  True)

        #######################################################################
        # Make sure start and stop can be called without throwing exceptions
        self.comp.start()


    # TODO Add additional tests here
    #
    # See:
    #   ossie.utils.bulkio.bulkio_helpers,
    #   ossie.utils.bluefile.bluefile_helpers
    # for modules that will assist with testing resource with BULKIO ports
    def setUp(self):
        """ Set up unit test - run before every method that starts with test """
        ossie.utils.testing.ScaComponentTestCase.setUp(self)
        self.src = sb.DataSource()
        self.sink = sb.DataSink()

        # connect components
        self.startComponent()
        self.src.connect(self.comp)
        self.comp.connect(self.sink)

        # starts sandbox
        sb.start()

        # variables
        self.operand = 10
        self.LEN = 100
        self.dataIn = [float(x) for x in xrange(self.LEN)]
        

    def tearDown(self):
        """ Stops unit test - run after every method that starts with test """
        #######################################################################
        # Simulate regular resource shutdown
        self.comp.releaseObject()

        # stops everything
        self.comp.stop()
        sb.reset()
        sb.stop()
        ossie.utils.testing.ScaComponentTestCase.tearDown(self)


    def testAdd(self):
        print "Testing add functionality"
        outData = []
        self.comp.operand = self.operand
        self.comp.operation = 0 # add
        self.src.push(self.dataIn)

        count = 0
        while True:
            outData = self.sink.getData()
            if outData:
                break
            if count == 100:
                break;
            time.sleep(.01)
            count+=1
        actual = [float(x)+self.comp.operand for x in xrange(self.LEN)]
        self.assertEqual(outData, actual)



    def testSubtract(self):
        print "Testing subtract functionality"
        outData = []
        self.comp.operand = self.operand
        self.comp.operation = 1 # subtract
        self.src.push(self.dataIn)

        count = 0
        while True:
            outData = self.sink.getData()
            if outData:
                break
            if count == 100:
                break;
            time.sleep(.01)
            count+=1
        actual = [float(x)-self.comp.operand for x in xrange(self.LEN)]
        self.assertEqual(outData, actual)

    def testDivide(self):
        print "Testing divide functionality"
        outData = []
        self.comp.operand = self.operand
        self.comp.operation = 2 # divide
        self.src.push(self.dataIn)

        count = 0
        while True:
            outData = self.sink.getData()
            if outData:
                break
            if count == 100:
                break;
            time.sleep(.01)
            count+=1
        actual = [float(x)/self.comp.operand for x in xrange(self.LEN)]
        self.assertEqual(outData, actual)

    def testMultiply(self):
        print "Testing multiply functionality"
        outData = []
        self.comp.operand = self.operand
        self.comp.operation = 3 # mulitply
        self.src.push(self.dataIn)

        count = 0
        while True:
            outData = self.sink.getData()
            if outData:
                break
            if count == 100:
                break;
            time.sleep(.01)
            count+=1
        actual = [float(x)*self.comp.operand for x in xrange(self.LEN)]
        self.assertEqual(outData, actual)

    def testPow(self):
        print "Testing pow functionality"
        outData = []
        self.comp.operand = self.operand
        self.comp.operation = 4 # pow
        self.src.push(self.dataIn)

        count = 0
        while True:
            outData = self.sink.getData()
            if outData:
                break
            if count == 100:
                break;
            time.sleep(.01)
            count+=1
        actual = [pow(float(x), self.comp.operand) for x in xrange(self.LEN)]
        self.assertEqual(outData, actual)


    def testComplexOperand(self):
        print "Testing complex operand functionality"
        outData = []
        self.comp.operand = complex(self.operand, 1)
        self.comp.operation = 0 # add
        self.src.push(self.dataIn)

        count = 0
        while True:
            outData = self.sink.getData()
            if outData:
                break
            if count == 100:
                break;
            time.sleep(.01)
            count+=1
        actual = [float(x)+self.comp.operand for x in xrange(self.LEN)]
        complexDataOut = [] 
        for x in range(len(outData)/2):
            r = x*2
            i = x*2+1
            z = complex(outData[r], outData[i])
            complexDataOut.append(z)
        self.assertEqual(complexDataOut, actual)


    def testComplexInput(self):
        print "Testing complex input functionality"
        outData = []
        self.comp.operand = 10
        self.comp.operation = 0 # add
        inData = []
        for i in xrange(0, self.LEN, 2):
            z = complex(self.dataIn[i], self.dataIn[i+1])
            inData.append(z)
        inData = self.dataIn
        self.src.push(inData)

        count = 0
        while True:
            outData = self.sink.getData()
            if outData:
                break
            if count == 100:
                break;
            time.sleep(.01)
            count+=1
        actual = [float(x)+self.comp.operand for x in xrange(self.LEN)]
        self.assertEqual(outData, actual)

    def testSin(self):
        print "Testing sin functionality"
        outData = []
        self.comp.operand = self.operand
        self.comp.operation = 5 # sin
        self.src.push(self.dataIn)

        count = 0
        while True:
            outData = self.sink.getData()
            if outData:
                break
            if count == 100:
                break;
            time.sleep(.01)
            count+=1
        actual = [math.sin(float(x)) for x in xrange(self.LEN)]
        self.assertEqual(outData, actual)

    def testCos(self):
        print "Testing cos functionality"
        outData = []
        self.comp.operand = self.operand
        self.comp.operation = 6 # cos
        self.src.push(self.dataIn)

        count = 0
        while True:
            outData = self.sink.getData()
            if outData:
                break
            if count == 100:
                break;
            time.sleep(.01)
            count+=1
        actual = [math.cos(float(x)) for x in xrange(self.LEN)]
        self.assertEqual(outData, actual)


    def testTan(self):
        print "Testing tan functionality"
        outData = []
        self.comp.operand = self.operand
        self.comp.operation = 7 # tan
        self.src.push(self.dataIn)

        count = 0
        while True:
            outData = self.sink.getData()
            if outData:
                break
            if count == 100:
                break;
            time.sleep(.01)
            count+=1
        actual = [math.tan(float(x)) for x in xrange(self.LEN)]
        self.assertEqual(outData, actual)

if __name__ == "__main__":
    ossie.utils.testing.main("../calc1to1.spd.xml") # By default tests all implementations
