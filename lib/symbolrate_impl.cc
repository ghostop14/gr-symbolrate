/* -*- c++ -*- */
/* 
 * Copyright 2017 ghostop14.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "symbolrate_impl.h"
#include <stdio.h>

namespace gr {
  namespace symbolrate {

    symbolrate::sptr
    symbolrate::make(float samp_rate, float valid_min, float valid_max, bool logRates)
    {
      return gnuradio::get_initial_sptr
        (new symbolrate_impl(samp_rate, valid_min, valid_max,logRates));
    }

    /*
     * The private constructor
     */
    symbolrate_impl::symbolrate_impl(float samp_rate, float valid_min, float valid_max,bool logRates)
      : gr::block("symbolrate",
              gr::io_signature::make(1, 1, sizeof(float)), // input array
              gr::io_signature::make(2, 2, sizeof(float))), // output array
              d_samp_rate(samp_rate),
              d_valid_min(valid_min),
              d_valid_max(valid_max),
              bLogRates(logRates)
    {
    }

    /*
     * Our virtual destructor.
     */
    symbolrate_impl::~symbolrate_impl()
    {
    }

    void
    symbolrate_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      /* <+forecast+> e.g. ninput_items_required[0] = noutput_items */
    }

    int
    symbolrate_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const float *in = (const float *) input_items[0];
      // float *out = (float *) output_items[0];
      // moved to 2 channels out.
      int inst_channel = 0;
      int avg_channel = 1;
      float **out = (float **)&output_items[0];
      bool curSymbol;

      int i;
      unsigned long nAvgSymbols = 0;
      double symbolRateTotal = 0.0;

      // Note: we have sample rate as d_samp_rate.  So 1 sample occurs at 1/d_samp_rate s
      for (i=0;i<noutput_items;i++) {
          if (in[i]==1.0) {
              curSymbol = true;
          }
          else {
              curSymbol = false;
          }

          // symbol change
          if (curSymbol != lastSymbol) {
              if (samples_since_transition > 0) {
                  // Hz = samp/sec / samp
                  lastSymbolRate = d_samp_rate / (float)samples_since_transition;

                  // If we provided boundaries for legitimate symbol rates, then let's use it as a sanity check.
                  // If we're not within bounds then just set it to zero.
                  if (d_valid_max > 0.0) {
                      if (lastSymbolRate > d_valid_max) {
                          lastSymbolRate = 0.0;
                      }
                      else {
                          if (lastSymbolRate < d_valid_min) {
                              lastSymbolRate = 0.0;
                          }
                      }
                  }
              }
              else {
                  lastSymbolRate=0.0;
              }

              samples_since_transition=0;
              lastSymbol = curSymbol;
          }
          else {
              samples_since_transition++;
          }

          out[inst_channel][i]=lastSymbolRate;

          if (lastSymbolRate > 0) {
              symbolRateTotal += lastSymbolRate;
              nAvgSymbols++;

              out[avg_channel][i] = (float)(symbolRateTotal / (float)nAvgSymbols);
          }
          else {
              out[avg_channel][i] = 0.0;
              symbolRateTotal = 0.0;
              nAvgSymbols = 0;
          }

          // Now check if we've had a transition in the last 2 seconds.  If not reset symbol rates.
          if ((float)samples_since_transition > ((d_samp_rate)*2.0)) {
              samples_since_transition = 0;
              lastSymbol = curSymbol;
              lastSymbolRate=0.0;
          }
      }

      // The averages take time to settle, so once the data has all been collected, work backwards
      // and "settle" the averages
      float lastAvg = 0.0;
      bool bGotTransition = false;

      for (i=noutput_items-1;i>=0;i--) {
          if (out[avg_channel][i] > 0.0) {
              if (!bGotTransition) {
                  lastAvg = out[avg_channel][i];
                  bGotTransition = true;

                  if (bLogRates) {
                      std::cout << "Symbol Transition Rate: " << lastAvg << "\n";
                  }
              }
              else {
                  out[avg_channel][i] = lastAvg;
              }


          }
          else {
              lastAvg = 0.0;
              bGotTransition = false;
          }
      }

      // Do <+signal processing+>
      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each(noutput_items);

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace symbolrate */
} /* namespace gr */

