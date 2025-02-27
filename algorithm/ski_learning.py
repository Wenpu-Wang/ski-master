
import numpy as np
import cv2
from keras import layers
from keras import models
# from keras import optimizers
from tensorflow.keras import optimizers

def get_actions_for_env(env):

    # Assume this is a Discrete Space from the Atari environments.
    # TODO figure out how to remove this assumption (if neccesary for
    # project)
    all_actions = list(range(env.action_space.n))
    
    def actions_function(state):
        return all_actions

    return actions_function
    

def ski_ram_base_feature_extractor(observation, action):
    """ Observation is the content of the RAM as an array.

    Simply make features 

    name: position in ram,
    value: it value
    
    """

    features = [('action', action)]
    for i, v in enumerate(observation):
        features.append(("ram[{}]".format(i), v))
    return features


def ski_image_base_feature_extractor(observation, action):
    """ Observation is the content of the RAM as an array.

    Simply make features 

    name: position in ram,
    value: it value
    
    """
    
    features = [('action', action)]
    for y in range(len(observation)):
        for x in range(len(observation[0])):
            features.append(("img[{y}][{x}]".format(y=y, x=x),
                             sum(observation[y][x])/(3.0 * 256)))
            
    return features


def ski_image_resized_feature_extractor(observation, action):
    """ Observation is the content of the RAM as an array.

    Simply make features 

    name: position in ram,
    value: it value
    
    """
    
    features = [('action-{}'.format(action), 1)]

    image = np.array(observation)
    image = cv2.resize(image, (0,0), fx=0.1, fy=0.1)
    # image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) /256.0
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) /256.0

    cv2.imshow("According to AI", image)
    cv2.waitKey(1)
    
    for y in range(len(image)):
        for x in range(len(image[0])):
            for c in range(len(observation[0][0])):
                features.append(("img[{y}][{x}][{c}]".format(y=y, x=x, c=c),
                                 observation[y][x][c]))

            # # RGB
            # features.append(("img[{y}][{x}]".format(y=y, x=x),
            #                  sum(image[y][x])/(3.0 * 256)))

            # # GRAY
            # features.append(("img[{y}][{x}]".format(y=y, x=x),
            #                  image[y][x]))
            
    return features



def ski_image_resized_action_feature_extractor(observation, action):
    """ Observation is the content of the RAM as an array.

    Simply make features 

    name: position in ram,
    value: it value
    
    """
    
    features = []
    image = np.array(observation)
    image = cv2.resize(image, (0,0), fx=0.1, fy=0.1, interpolation=cv2.INTER_AREA)
    # image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) /256.0
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) /256.0

    
    cv2.imshow("According to AI", image)
    cv2.waitKey(1)
    
    for y in range(len(image)):
        for x in range(len(image[0])):
            for c in range(len(observation[0][0])):
                features.append(("img[{y}][{x}][{c}]_{action}".format(y=y, x=x, c=c, action=action),
                                 observation[y][x][c]))
            
    return features



def ski_ram_nn_model():
    input_layer = layers.Input(shape=(128,))
    input_action = layers.Input(shape=(3,))

    inputs = layers.Concatenate()([input_layer, input_action])
    l1 = layers.Dense(128, activation='sigmoid')(inputs)
    l2 = layers.Dense(128, activation='sigmoid')(l1)

    output = layers.Dense(1)(l2)
    m = models.Model(inputs=[input_layer, input_action], outputs=output)
    opt = optimizers.SGD(lr=.0000000000000001, momentum=0.01)
    m.compile(optimizer=opt, loss="mean_squared_error")
    return m


def ski_image_nn_model():
    
    input_layer = layers.Input(shape=(250, 160, 3))
    # input_layer = layers.Input(shape=(210, 160, 3))
    
    reduced = layers.MaxPooling2D(5)(input_layer)
    conv1 = layers.Conv2D(filters=3, kernel_size=3, strides=1, activation="relu")(reduced)
    conv2 = layers.Conv2D(filters=5, kernel_size=5, strides=2, activation="relu")(conv1)
    conv3 = layers.Conv2D(filters=5, kernel_size=5, strides=2, activation="relu")(conv2)
    conv4 = layers.Conv2D(filters=10, kernel_size=(7,5), strides=1, activation="relu")(conv3)
    flat = layers.Flatten()(conv4)

    input_action = layers.Input(shape=(3,))
    joined = layers.Concatenate()([flat, input_action])
    output = layers.Dense(1)(joined)

    m = models.Model(inputs=[input_layer, input_action], outputs=output)
    opt = optimizers.SGD(lr=.01)
    m.compile(optimizer=opt, loss="mean_squared_error")
    return m


def ski_image_nn_model_2():
    
    input_layer = layers.Input(shape=(250, 160, 3))
    
    conv1 = layers.Conv2D(filters=3, kernel_size=3, strides=1, activation="relu")(input_layer)
    conv2 = layers.Conv2D(filters=5, kernel_size=3, strides=1, activation="relu")(conv1)
    conv3 = layers.Conv2D(filters=5, kernel_size=5, strides=3, activation="relu")(conv2)
    conv4 = layers.Conv2D(filters=5, kernel_size=5, strides=3, activation="relu")(conv3)
    conv5 = layers.Conv2D(filters=5, kernel_size=5, strides=3, activation="relu")(conv4)
    conv6 = layers.Conv2D(filters=10, kernel_size=(8,4), strides=1, activation="relu")(conv5)
    flat = layers.Flatten()(conv6)

    input_action = layers.Input(shape=(3,))
    joined = layers.Concatenate()([flat, input_action])
    output = layers.Dense(1)(joined)

    m = models.Model(inputs=[input_layer, input_action], outputs=output)
    opt = optimizers.SGD(lr=.01)
    m.compile(optimizer=opt, loss="mean_squared_error")
    return m



def ski_image_nn_model_flow():
    
    # input_layer = layers.Input(shape=(250, 160, 9))
    input_layer = layers.Input(shape=(210, 160, 9))
    
    conv1 = layers.Conv2D(filters=6, kernel_size=3, strides=1, activation="relu")(input_layer)
    pool1 = layers.MaxPooling2D(2)(conv1)
    conv2 = layers.Conv2D(filters=6, kernel_size=3, strides=1, activation="relu")(pool1)
    pool2 = layers.MaxPooling2D(2)(conv2)
    conv3 = layers.Conv2D(filters=6, kernel_size=5, strides=3, activation="relu")(pool2)
    pool3 = layers.MaxPooling2D(2)(conv3)
    flat = layers.Flatten()(pool3)

    input_action = layers.Input(shape=(3,))
    joined = layers.Concatenate()([flat, input_action])
    output = layers.Dense(1)(joined)

    m = models.Model(inputs=[input_layer, input_action], outputs=output)
    opt = optimizers.SGD(lr=.01)
    m.compile(optimizer=opt, loss="mean_squared_error")
    return m
