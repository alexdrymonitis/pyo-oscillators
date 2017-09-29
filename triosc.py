# Copyright 2017 Alexandros Drymonitis
#
# This code is based on the Pyo Python module and code by Olivier Belanger
# Pyo is released under the GNU GPL 3 Licence, so is this file
# A Licence copy should come with this code
# If not, please check <http://www.gnu.org/licenses/>
#
# This is a simple triangle wave oscillator


from pyo import *

class TriOsc(PyoObject):
    """
    A simple triangle wave oscillator.

    :Parent: :py:class:`PyoObject`

    :Args:

        freq: float or PyoObject, optional
            Frequency in cycles per second. Defaults to 100.
        phase: float or PyoObject, optional
            Phase of sampling, expressed as a fraction of a cycle (0 to 1).
            Defaults to 0.

    >>> s = Server().boot()
    >>> s.start()
    >>> a = TriOsc(200, mul=.2).out()

    """
    def __init__(self, freq=100, phase=0, mul=1, add=0):
        PyoObject.__init__(self,mul,add)
        self._freq = freq
        self._phase = phase
        self._phasor = Phasor(freq=self._freq, phase=self._phase)
        self._inv_phasor = self._phasor * (-1) + 1
        self._min = Min(self._phasor, self._inv_phasor, mul=4, add=-1)
        # A Sig is the best way to properly handle "mul" and "add" arguments.
        self._output = Sig(self._min, mul, add)
        # Create the "_base_objs" attribute. This is the object's audio output.
        self._base_objs = self._output.getBaseObjects()

    def setFreq(self, x):
        """
        Replace the `freq` attribute.

        :Args:

            x: float or PyoObject
                New `freq` attribute.

        """
        self._freq = x
        self._phasor.freq = x

    def setPhase(self, x):
        """
        Replace the `phase` attribute.

        :Args:

            x: float or PyoObject
                New `phase` attribute.

        """
        self._phase = x
        self._phasor.phase = x

    def play(self, dur=0, delay=0):
        for key in self.__dict__.keys():
            if isinstance(self.__dict__[key], PyoObject):
                self.__dict__[key].play(dur, delay)
        return PyoObject.play(self, dur, delay)

    def stop(self):
        for key in self.__dict__.keys():
            if isinstance(self.__dict__[key], PyoObject):
                self.__dict__[key].stop()
        return PyoObject.stop(self)

    def out(self, chnl=0, inc=1, dur=0, delay=0):
        for key in self.__dict__.keys():
            if isinstance(self.__dict__[key], PyoObject):
                self.__dict__[key].play(dur, delay)
        return PyoObject.out(self, chnl, inc, dur, delay)

    @property
    def freq(self):
        """float or PyoObject. Fundamental frequency in cycles per second."""
        return self._freq
    @freq.setter
    def freq(self, x): self.setFreq(x)

    @property
    def phase(self):
        """float or PyoObject. Phase of sampling between 0 and 1."""
        return self._phase
    @phase.setter
    def phase(self, x): self.setPhase(x)

if __name__ == "__main__":
    # Test case...
    s = Server().boot()

    tri = TriOsc(freq=200, mul=.2).out()

    sc = Scope(tri)

    s.gui(locals())
