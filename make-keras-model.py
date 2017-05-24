#!/usr/bin/env python3

import keras
from keras import layers
from keras.models import Model
import numpy as np
import os

# setup inputs
tracks = layers.Input(shape=(None, 4))
vertex = layers.Input(shape=(8,))

# add GRU to process tracks
gru = layers.GRU(5)(tracks)

# merge with the vertex inputs
merged = layers.concatenate([gru, vertex])

# add flavors output
flavor = layers.Dense(4, activation='softmax')(merged)

# add charge output
charge = layers.Dense(1)(merged)

model = Model(inputs=[tracks, vertex], outputs=[flavor, charge])
model.compile(optimizer='adam', loss='categorical_crossentropy')

model_dir = 'model'
if not os.path.isdir('model'):
    os.mkdir('model')

with open('{}/arch.json'.format(model_dir),'w') as archetecture:
    archetecture.write(model.to_json(indent=2, sort_keys=True) )

model.save_weights('{}/weights.h5'.format(model_dir))

trk = np.linspace(-1, 1, 20)[:,None] * np.linspace(-1, 1, 4)[None,:]
vx = np.linspace(-1, 1, 8)[None,:]
for output in model.predict([trk[None,:], vx]):
    print(output)

from keras.utils.vis_utils import model_to_dot
model_to_dot(model).write_pdf('{}/model.pdf'.format(model_dir))

