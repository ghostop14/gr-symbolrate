/* -*- c++ -*- */
/* 
 * Copyright 2017 <+YOU OR YOUR COMPANY+>.
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

#ifndef INCLUDED_SYMBOLRATE_SYMBOLRATE_IMPL_H
#define INCLUDED_SYMBOLRATE_SYMBOLRATE_IMPL_H

#include <symbolrate/symbolrate.h>

namespace gr {
  namespace symbolrate {

    class symbolrate_impl : public symbolrate
    {
     private:
      // Nothing to declare in this block.
    float d_samp_rate = 0.0f;

    float d_valid_min = 0.0f;
    float d_valid_max = 0.0f;

    bool bLogRates = false;

    // transition tracking
    unsigned long samples_since_transition = 0;
    float lastSymbolRate = 0.0f;
    bool lastSymbol = false;  // Used a boolean so I can NOT it to flip it.

    float long_average = 0.0f;
    unsigned long long_avg_samples = 0;

     public:
      symbolrate_impl(float samp_rate, float valid_min, float valid_max, bool logRates);
      ~symbolrate_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);
    };

  } // namespace symbolrate
} // namespace gr

#endif /* INCLUDED_SYMBOLRATE_SYMBOLRATE_IMPL_H */

