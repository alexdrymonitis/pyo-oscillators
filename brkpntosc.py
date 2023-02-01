# Copyright 2017 Alexandros Drymonitis
#
# This code is based on the Pyo Python module and code by Olivier Belanger
# Pyo is released under the GNU GPL 3 Licence, so is this file
# A Licence copy should come with this code
# If not, please check <http://www.gnu.org/licenses/>
#
# This is an oscillator with a settable breakpoin

from pyo import *

class BrkPntOsc(PyoObject):
    """
    An oscillator with a settable breakpoint resulting in a waveform
    that goes from a backward sawtooth to a forward sawtooth.

    :Parent: :py:class:`PyoObject`

    :Args:

        freq: float or PyoObject, optional
            Frequency in cycles per second. Defaults to 100.
        phase: float or PyoObject, optional
            Phase of sampling, expressed as a fraction of a cycle (0 to 1).
            Defaults to 0.
        breakpoint: float or PyoObject, optional
            Point where the waveform breaks. From 0 to 1. Defaults to 0.5.

    >>> s = Server().boot()
    >>> lfo = Sine(freq=.2, mul=.4, add=.5)
    >>> brk = BrkPntOsc(freq=[200,202], breakpoint=lfo, mul=.2).out()
    >>> s.gui(locals())

    """
    def __init__(self, freq=100, phase=0, breakpoint=0.5, mul=1, add=0):
        PyoObject.__init__(self,mul,add)
        self._freq = freq
        self._phase = phase
        self._breakpoint = Sig(breakpoint)
        self._invbrk = 1.0 - self._breakpoint
        self._phasor = Phasor(freq=self._freq, phase=self._phase)
        self._rising = (self._phasor / self._breakpoint) * (self._phasor < self._breakpoint)
        self._falling = (((self._phasor - self._breakpoint) / self._invbrk) * (-1) + 1) * (self._phasor >= self._breakpoint)
        self._osc = Sig((self._rising + self._falling), mul=2, add=-1)
        # A Sig is the best way to properly handle "mul" and "add" arguments.
        self._output = Sig(self._osc, mul, add)
        # Create the "_base_objs" attribute. This is the object's audio output.
        self._base_objs = self._output.getBaseObjects()

    def setFreq(self, freq):
        """
        Replace the `freq` attribute.

        :Args:

            x: float or PyoObject
                New `freq` attribute.

        """
        self._freq = freq
        self._phasor.setFreq(self._freq)

    def setPhase(self, phase):
        """
        Replace the `phase` attribute.

        :Args:

            x: float or PyoObject
                New `phase` attribute.

        """
        self._phase = phase
        self._phasor.setPhase(self._phase)

    def setBrkPnt(self, brkpnt):
        """
        Replace the `breakpoint` attribute.

        :Args:

            x: float or PyoObject
                New `phase` attribute.

        """
        self._breakpoint.setValue(brkpnt)

    @property
    def freq(self):
        """float or PyoObject. Fundamental frequency in cycles per second."""
        return self._freq
    
    @freq.setter
    def freq(self, freq):
        self.setFreq(freq)

    @property
    def phase(self):
        """float or PyoObject. Phase of sampling between 0 and 1."""
        return self._phase
    
    @phase.setter
    def phase(self, phase):
        self.setPhase(phase)

    @property
    def breakpoint(self):
        """float or PyoObject. Breakpoint of oscillator between 0 and 1."""
        return self._breakpoint
    
    @breakpoint.setter
    def breakpoint(self, brkpnt):
        self.setBrkPnt(brkpnt)

if __name__ == "__main__":
    # Test case...
    s = Server().boot()
    lfo = Sine(freq=.2, mul=.4, add=.5)
    brk = BrkPntOsc(freq=[200,202], breakpoint=lfo, mul=.2).out()
    sc = Scope(brk)
    s.gui(locals())
