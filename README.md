# gr-symbolrate
GNURadio block to output observed symbol rates. The goal is to help with real-time blind signal analysis 
by extracting the key symbol rate parameter.

gr-symbolrate takes a demodulated signal that's been stabilized through a binary slicer and reports 
instantaneous and average symbol rates based on transitions.  Although consecutive 1's or 0's would
be detected as a single symbol/transition, given the digital communications goal of maintaining a 
high number of transmissions to aid in clock recovery, in general symbol rate will be close to transition
rate when combined with a "valid_min" parameter discussed below.

Build is standard:
mkdir build
cd build
cmake ..
make
make install
ldconfig

The block takes 4 parameters:
samp_rate - The current flowgraph stream flow rate (used to calculate transitions/sec)
valid_min - Sometimes noise is picked up as a transition, once a reasonable range is 
	    visible, valid_min can be used to filter out symbol rates below this threshold.
	    The default value is 0.
valid_max - Like valid_min but for a maximum rate.  Sometimes a quick spike in noise is
	    detected as a quick instantaneous symbol rate.  This value filters out those
	    high-frequency spikes.  Setting this value to zero (the default) disables
	    this filtering.
Log Rates - If enabled, will write rates to stdout.

NOTES: 
For best results in feeding the binary slicer, watch your filters and cutoffs.  If the slope continues too wide
past your cutoff, it could make the symbol look "faster" than it is.
For best results feeding a clock recovery MM block for runtime, take the average values written out and average them.
Then add 2% as the initial starting point for the MM block.  This accounts in some part for the slicer cutoff.

Output:
out - current symbol/transition rate.
avg - average symbol rate for current detected transmission sequence.


