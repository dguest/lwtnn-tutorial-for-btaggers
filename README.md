Tutorial on using lwtnn on CERN machines
========================================

You've trained some boosted higgsonic stop tagger with Keras and found
that it's the most awesome thing for physics since cutting hard on
mT2. But now you're in a bind: someone stupid convener is asking how
you're going to calibrate it! You have no idea, but it will probably
involve making the tagger run in ~RootCore~ Analysis Base (?) so
everyone else can run the tagger without setting up 10 GB of conda
dependencies that you may or may not have documented.

This is what `lwtnn` is for. It has two components:

 - A set of converters to translate the Keras saved NNs to a standard
   JSON format.

 - I set of C++ classes that are initialized from this standard format
   and can be used for inference within your C++ framework.

We try to keep the C++ dependencies minimal, but we require boost and
Eigen3.

Setting up on a machine with CVMFS
==================================

You should be able to get everything by running

```bash
source cvmfs-setup.sh
```
