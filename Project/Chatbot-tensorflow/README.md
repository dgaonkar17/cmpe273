# tensorflow with NLTK:

Initially we created the intents in tensorflow and used deep-learning libraries of tensorflow to train the model. 

We used 2 layer neural network to train our model after stemming the words into documents and classes using NLTK.

Then we save the trained model using pickle and build our chatbot framework.

The contextual chatbot uses model.predict() which returns the probability with list of responses.

We are building the context inside the framework via context_set and context_filter which helps in switching from one context to another and follow a process like asking a user his details one after another in the process of booking.

There are various concepts of NLTK used in our code like tokenzing, tagging, using Named Entity for data extraction.
