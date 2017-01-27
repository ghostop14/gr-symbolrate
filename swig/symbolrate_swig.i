/* -*- c++ -*- */

#define SYMBOLRATE_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "symbolrate_swig_doc.i"

%{
#include "symbolrate/symbolrate.h"
%}


%include "symbolrate/symbolrate.h"
GR_SWIG_BLOCK_MAGIC2(symbolrate, symbolrate);
