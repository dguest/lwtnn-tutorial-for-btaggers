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

Getting this code
=================

You can clone from github:

```bash
git clone --recursive git@github.com:dguest/lwtnn-tutorial-for-btaggers.git
```

Note that the `--recursive` flag is important to get `lwtnn` as a
submodule. If you have trouble with authentication you may
[need to add your ssh keys][1] to your github account. Or just use the
`https:` clone method for now.

[1]: https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/

Setting up
==========

The ideal setup depends on where you're working.

Setup on machines with CVMFS
----------------------------

You should be able to get everything by running

```bash
source cvmfs-setup.sh
```

Setup elsewhere
---------------

You're shit out of luck. Or you can figure out how to install the
following:

 - Python 3 (for the converters)
 - Boost and Eigen3 (I might add the required headers to this package
   someday)

Building the code
-----------------

This is to build the C++ library that you'll have to link to.

```bash
cd lwtnn
make
```

It should just compile.

At some point we'll have this as a common package in AnalysisBase and
Athena, but it's not there yet. If you really want it soon
[create a JIRA ticket][2] or something, we don't know how to keep
track of how many people want this. Be sure to mention @dguest and @jwsmith.

[2]: https://its.cern.ch/jira/projects/ATLASG

Making a model to play with
===========================

There's a script to build a dummy model. You can run it with

```bash
./make-keras-model.py
```

This gives you trouble, you can also just grab the saved version out
of `/data`.

Converting a Keras model to lwtnn JSON
======================================

The Keras outputs will be in `/model`. To convert them to something
you can run in `lwtnn`, the one missing ingredient is the variable
specification. This is a JSON file that I force you to write, which
specifies the names, ordering, and normalizations for the inputs and
outputs.

The "variables" file
--------------------

Why am I such a jerk? I promise it's to save you work: remember that
when you trained your Keras model, you stuffed M input variables into
an N x M array? When you use this NN for inference, you'd better order
those M input variables the same way. To avoid confusion we just
insist that each input have a name. It's a good idea, I promise.

Anyway, you can generate a dummy "variables" file by running the
converter:

```bash
cd model
../lwtnn/converters/kerasfunc2json.py arch.json weights.h5 > vars.json
```

This will spit out `vars.json` which has entries for `input_sequences`
(the tracks), `inputs` (the vertices), and `outputs` (the labels and
jet charge). You should go in and change the `"name"` entries to
something you'll remember, and make sure the `"labels"` in the outputs
correspond to the class labels you used. Or, since this is tedious and the name conventions will have to match what you use in the C++ code, you can just use the file `/data/variables.json`.

Making the lwtnn JSON configuration
-----------------------------------

Now that you've created (or found) the "variables" file, you can make save the entire NN to the lwtnn JSON format.

```bash
../lwtnn/converters/kerasfunc2json.py arch.json weights.h5 ../data/variables.json > nn-config.json
```

To make sure this works within lwtnn, you can run

```bash
../lwtnn/bin/lwtnn-test-lightweight-graph nn-config.json
```

This should print out the same numbers that were printed from
`make-keras-model.py`.

