# gr-symbolrate
GNURadio block to output observed symbol rates. The goal is to help with real-time blind signal analysis 
by extracting the key symbol rate parameter.

gr-symbolrate takes a demodulated signal that's been stabilized through a binary slicer and reports 
instantaneous and average symbol rates based on transitions.  Although consecutive 1's or 0's would
be detected as a single symbol/transition, given the digital communications goal of maintaining a 
high number of transmissions to aid in clock recovery, in general symbol rate will be close to transition
rate when combined with a "valid_min" parameter discussed below.

## Building
Build is pretty standard:

mkdir build

cd build

cmake ..

make

make install

ldconfig

## Recommendations for best results
In the examples directory are flowgraphs for ASK/OOK, FSK, and BPSK.  Each process does involve initial
low-pass filters and some power squelch to eliminate initial noise.  Note that the filters are tuned to
the ballpark of the potential input rates so if you copy them as a starting point make sure you adjust
the filters appropriately for your input signal.  The ASK grc was for a 2970 sps signal, the FSK for a 
3975 sps signal, and the BPSK for BPSK31 at 31.25 sps.  You'll also need to adjust the y axis range and 
threshold values in the symbol rate time sink.

Also, the valid_min and valid_max parameters discussed below should be leveraged to get the most accurate
results.  Once you start to see an average form, remember that back-to-back 1's or 0's will show up as 
transitions at 1/2 the actual rate.  So once you see the average forming, it's recommended that you set 
the valid_min to about 0.7*long_avg and the valid_max at 1.3*long_avg.  This will act like a filter on the 
results and help narrow in on a more accurate average the next pass.

If you're feeding the grc with an IQ file and you put it on repeat, remember that as it trails off the end 
of one file playback into the beginning of the next, you can get an unrealistic symbol transition (too fast 
or too slow).  Again, setting the valid_min and valid_max will help, but you may want to consider the 
gr-filerepeater OOT module and set a repeat delay of 500 - 1000 ms.  This would result in any spurious transition 
showing up as 1-2 Hz which can be filtered with a valid_min say greater than 10.

## Parameters
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
past your cutoff, it could make the symbol look "faster" than it is, which may cause garbage to come out of
a clock recovery block.

## Output streams
inst_rate - current symbol/transition rate.

short avg - average symbol rate for current detected transmission sequence.

long avg - long-term running rate.

