from keras.layers import Input, Embedding, LSTM, Dense, Concatenate
from keras.models import Model

main_input = Input(shape=(featuresLength,), dtype='int32', name='main_input')
name_input = Input(shape=(maxNameLength,), dtype='int32', name='name_input')

Embedding(
   input_dim=len(alphabet), # e.g, 10 if you have 10 words in your vocabulary
   output_dim=embedding_size, # size of the embedded vectors
   input_length=time_steps,
   batch_input_shape=(batch_size,time_steps)
)

lstm_out = LSTM(32)(name_input)

x = Concatenate([main_input, lstm_out])

x = Dense(64, activation='relu')(x)
x = Dense(64, activation='relu')(x)
x = Dense(64, activation='relu')(x)

# And finally we add the main logistic regression layer
main_output = Dense(13, activation='softmax', name='main_output')(x)

model = Model(inputs=[main_input, name_input], outputs=[main_output])

model.compile(optimizer='adam', loss='binary_crossentropy', loss_weights=[1., 0.2])

model.fit([main_input_data, name_input_data], [main_output_labels], epochs=50, batch_size=32)