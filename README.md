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
When you're analyzing a signal and you have no point of reference on symbol rate, rate recovery can
involve some iterations before you get symbols out.  ASK and FSK are a little easier because you can
visualize it on a waterfall and use other tools like inspectrum to measure it.  PSK is a bit harder.

In the examples directory are flowgraphs for ASK/OOK, FSK, and BPSK.  You'll notice that each flowgraph
starts with an initial low-pass filter and some power squelch to eliminate some noise.  
Once you hae a reasonably clean input, you'll notice a demod block.  This block varies depending on the
modulation but once the signal leaves the demod block there's another low-pass filter.  This filter
just further helps smooth out the symbol signal before going through symbol recovery.  Having this
filter in there tends to make symbol extraction more accurate.  For best 
performance the cutoff should be around the sample rate.... which you may not know on the first pass.  
So start with a higher cutoff than you think you need (or just bypass it on the first run) just to be safe. 
Also leverage the valid_min and valid_max values discussed below once you have a ballpark for better accuracy.
 
The other catch for actually recovering the symbols is the clock recovery block.  This block takes
the symbol rate as part of one of it's parameters that act as an initial guess when the block starts...
which again you won't know till you get some averages out.  So don't trust the clock recovery symbols
until you have an average rate and have tuned the post-demod filter.  Then take that symbol rate number
to feed the clock recovery to get reasonable symbols out.

The other issue to be careful with is decimation.  If you decimate the hardware sampling rate down to a 
working sample rate that isn't an integer multiple, I've seen this rounding affect the accuracy of the results.
For example, decimating 1.25 Msps with a 400K working rate produced a 3-5% variation.
With the clock recovery block this will be enough of a difference in the initial symbol rate to get garbage out.

For reference, the example ASK grc was for a 2970 sps signal, the FSK for a 
3975 sps signal, and the BPSK for BPSK31 at 31.25 sps.  Using this process the average rate were
calculated by the averaging block as 3000, and 32 respectively.  Close enough for good symbol recovery.
There's also a more real-world example of finding the symbol rate for an LRIT satellite signal at 
around 293 symbols/sec.  You'll also need to adjust the y axis range and threshold values in the 
symbol rate time sink along with the level meter max.

Also, the valid_min and valid_max parameters discussed below should be leveraged to get the most accurate
results.  Once you start to see an average form, remember that back-to-back 1's or 0's will show up as 
transitions at 1/2 the actual rate.  So once you see the average forming, it's recommended that you set 
the valid_min to about 0.7 x long_avg and the valid_max at 1.3 x long_avg.  In general 25-30% deviations
work well.  This will act like a filter on the results and help narrow in on a more accurate average the next pass.

Once you think you have good symbols out, you can also use the byte_receiver.py script in the examples directory
to print the bits out.  The grc.bitprinter.py example script does the same thing for saved binary files.

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

		(these rate are set in the module constructor, so you can't change them at runtime.  If you need to adjust
		them you'll need to stop the flowgraph and change them)
Log Rates - If enabled, will write rates to stdout.

NOTES: 
For best results in feeding the binary slicer, watch your filters and cutoffs.  If the slope continues too wide
past your cutoff, it could make the symbol look "faster" than it is, which may cause garbage to come out of
a clock recovery block.

## Output streams
inst_rate - current symbol/transition rate.

short avg - average symbol rate for current detected transmission sequence.

long avg - long-term running rate.

