import tensorflow as tf
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt
import pandas as pd
from tensorflow import keras


# inner function
def load_model_analyze(keyword_parameter, limit_parameter, model_name):

    model = keras.models.load_model(model_name)

    tweetTexts = []
    # need to declare the dataset for the loading encoder - this will be the basic training and tested dataset
    dataSet, info = tfds.load('imdb_reviews/subwords8k', with_info=True, as_supervised=True)
    encoder = info.features['text'].encoder

    # pad the vectors
    def pad_to_size(vec, size):
        zeros = [0] * (size - len(vec))
        vec.extend(zeros)
        return vec

    # generate a prediction
    def predict(post, pad):
        encoded_sample_pred_text = encoder.encode(post)
        if pad:
            encoded_sample_pred_text = pad_to_size(encoded_sample_pred_text, 64)
        encoded_sample_pred_text = tf.cast(encoded_sample_pred_text, tf.float32)
        predictions = model.predict(tf.expand_dims(encoded_sample_pred_text, 0))
        return predictions

    def train_dataset_setup():
        data_set = pd.read_csv("result.csv")
        # print(data_set['Tweet_text'])
        for line in data_set['Tweet_text']:
            tweetTexts.append(line)

    def percentage(part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def visualization(positive, wpositive, spositive, negative, wnegative, snegative, neutral, keyword, limit):
        labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]',
                  'Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]',
                  'Strongly Negative [' + str(snegative) + '%]']
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen', 'lightgreen', 'darkgreen', 'gold', 'red', 'lightsalmon', 'darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + keyword + ' by analyzing ' + str(limit) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()

    def tensorflow_model_analyze(keyword, limit):
        polarity = 0
        positive = 0
        wpositive = 0
        spositive = 0
        negative = 0
        wnegative = 0
        snegative = 0
        neutral = 0

        train_dataset_setup()
        for tweet in tweetTexts:
            analysis = predict(tweet, pad=True)
            print(analysis)
            polarity += analysis

            if analysis == 0.5:
                neutral += 1
            elif 0.6 < analysis <= 0.7:
                wpositive += 1
            elif 0.7 < analysis <= 0.9:
                positive += 1
            elif 0.9 < analysis <= 1:
                spositive += 1
            elif 0.3 < analysis <= 0.4:
                wnegative += 1
            elif 0.1 < analysis <= 0.3:
                negative += 1
            elif 0 < analysis <= 0.1:
                snegative += 1

        positive = percentage(part=positive, whole=limit)
        wpositive = percentage(part=wpositive, whole=limit)
        spositive = percentage(part=spositive, whole=limit)
        negative = percentage(part=negative, whole=limit)
        wnegative = percentage(part=wnegative, whole=limit)
        snegative = percentage(part=snegative, whole=limit)
        neutral = percentage(part=neutral, whole=limit)

        polarity = polarity / limit

        print("How people are reacting on " + keyword + " by analyzing " + str(limit) + " tweets.")
        print()
        print("General Report: ")

        if polarity == 0.5:
            print("Neutral")
        elif 0.6 < polarity <= 0.7:
            print("Weakly Positive")
        elif 0.7 < polarity <= 0.9:
            print("Positive")
        elif 0.9 < polarity <= 1:
            print("Strongly Positive")
        elif 0.3 < polarity <= 0.4:
            print("Weakly Negative")
        elif 0.1 < polarity <= 0.3:
            print("Negative")
        elif 0 < polarity <= 0.1:
            print("Strongly Negative")

        print()
        print("Detailed Report: ")
        print(str(positive) + "% people thought it was positive")
        print(str(wpositive) + "% people thought it was weakly positive")
        print(str(spositive) + "% people thought it was strongly positive")
        print(str(negative) + "% people thought it was negative")
        print(str(wnegative) + "% people thought it was weakly negative")
        print(str(snegative) + "% people thought it was strongly negative")
        print(str(neutral) + "% people thought it was neutral")

        visualization(positive=positive, wpositive=wpositive, spositive=spositive, negative=negative,
                      wnegative=wnegative, snegative=snegative, neutral=neutral, keyword=keyword,
                      limit=limit)

    tensorflow_model_analyze(keyword=keyword_parameter, limit=limit_parameter)
