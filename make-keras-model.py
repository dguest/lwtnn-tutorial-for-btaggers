#!/usr/bin/env python3

import keras
from keras import layers
from keras.models import Model
import numpy as np
import os

# setup inputs
tracks = layers.Input(shape=(None, 4), name='tracks')
vertex = layers.Input(shape=(8,), name='vertices')

# add GRU to process tracks
gru = layers.GRU(5)(tracks)

# merge with the vertex inputs and feed to a dense layer
merged = layers.concatenate([gru, vertex])
dense = layers.Dense(10, activation='relu')(merged)

# add flavors output
flavor = layers.Dense(4, activation='softmax', name='flavor')(dense)

# add charge output
charge = layers.Dense(1, name='charge')(dense)

# build and compile the model
model = Model(inputs=[tracks, vertex], outputs=[flavor, charge])
model.compile(optimizer='adam',
              loss=['categorical_crossentropy', 'mean_squared_error'])

# now we save some things (create a subdirectory to keep it clean)
model_dir = 'model'
if not os.path.isdir('model'):
    os.mkdir('model')

# save the archetecture and weights
with open('{}/arch.json'.format(model_dir),'w') as archetecture:
    archetecture.write(model.to_json(indent=2, sort_keys=True) )
model.save_weights('{}/weights.h5'.format(model_dir))

# the model isn't trained, but we can still run it and get outputs
# with the initial weights. This is useful to make sure it gives the
# same predictions as lwtnn.
trk = np.linspace(-1, 1, 20)[:,None] * np.linspace(-1, 1, 4)[None,:]
vx = np.linspace(-1, 1, 8)[None,:]
for output in model.predict([trk[None,:], vx]):
    print(output)

# lastly, we can save a visualization of the model. This sometimes
# crashes because it relies on dependencies that Keras doesn't check
# for, but we don't striclly _need_ this anyway.
from keras.utils.vis_utils import model_to_dot
model_to_dot(model).write_pdf('{}/model.pdf'.format(model_dir))

