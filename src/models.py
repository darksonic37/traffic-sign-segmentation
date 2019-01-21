import tensorflow as tf


def vgg16(img_height, img_width, output_activation, loss, optimizer, metrics, dropout, nb_layers=None):
    # Freeze the model's first nb_layers layers
    vgg16 = tf.keras.applications.vgg16.VGG16(weights='imagenet')
    for layer in vgg16.layers[:nb_layers]:
        layer.trainable = False

    # Dropout after each existing fully-connected layer
    fc1 = vgg16.get_layer('fc1')
    fc2 = vgg16.get_layer('fc2')
    dropout1 = tf.keras.layers.Dropout(rate=dropout)
    dropout2 = tf.keras.layers.Dropout(rate=dropout)
    x = dropout1(fc1.output)
    x = fc2(x)
    x = dropout2(x)

    # Install our own fully-connected layer to classify each of the image's pixels
    x = tf.keras.layers.Dense(units=img_height*img_width, activation=output_activation)(x)
    x = tf.keras.layers.Reshape((img_height, img_width, 1))(x)

    # Stitch model
    model = tf.keras.models.Model(inputs=vgg16.input, outputs=x)
    model.compile(loss=loss, optimizer=optimizer, metrics=metrics)
    return model
