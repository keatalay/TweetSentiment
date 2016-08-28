import csv
import tokenizer
import nltk.classify
from nltk.classify import NaiveBayesClassifier as nbc
from nltk.probability import FreqDist


class TweetClassifier:

    def __init__(self, training_file, training_features=None,
                 classifier=None):
        self.training_file = training_file
        self.tok = tokenizer.Tokenizer()

    # readTweets tokenizes training data and returns a list of tuples,
    # the first element of which containins the contents of each tweet
    # (represented as a list of strings) and the second element of which
    # is a string representing the sentiment of the associated tweet

    def readTweets(self):
        tweets = []
        with open(self.training_file, 'rb') as csvfile:
            tweet_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in tweet_reader:
                if '0' in row[0]:
                    tweets.append((self.tok.tokenize(row[5]), 'negative'))
                elif '2' in row[0]:
                    tweets.append((self.tok.tokenize(row[5]), 'neutral'))
                elif '4' in row[0]:
                    tweets.append((self.tok.tokenize(row[5]), 'positive'))
        return tweets

    # getTweetContents returns a list of all of tokens found in the
    # tweets read in using readTweets

    def getTrainingTweetContents(self, tweets):
        all_tokens = []
        for (words, sentiment) in tweets:
            all_tokens.extend(words)
        return all_tokens

    def getTestingTweetContents(self, tweets):
        all_tokens = []
        for words in tweets:
            all_tokens.extend(words)
            # print(words)
        return all_tokens

    # getFeatures takes the list of tokens found in the tweets
    # previously read in and returns a collection associating each
    # token with the frequency of its occurance amongst the corpus of tweets

    def getFeatures(self, words):
        word_list = FreqDist(words)
        # for entry in word_list:
        #    print(entry)
        word_features = word_list.keys()
#        for entry in word_features:
#            print(entry)
        return word_features

    # extractTrainingFeatures returns a dictionary indicating which words in
    # word_feats are also in document

    def extractTrFeatures(self, document):
        document_words = set(document)
        # for word in document_words:
        #    print(word)
        features = {}
        for word in self.training_features:
            features['contains(%s)' % word] = (word in document_words)
        return features

    def trainClassifier(self):
        tweets = self.readTweets()
        self.training_features = self.getFeatures(
            self.getTrainingTweetContents(tweets))
        print('Constructing training_set. . .')
        training_set = nltk.classify.apply_features(self.extractTrFeatures,
                                                    tweets)
        print('Training Classifier. . .')
        self.classifier = nbc.train(training_set)

    def classifyTweet(self, tweet):
        tokenized_tweet = self.tok.tokenize(tweet)
        return self.classifier.classify((self.extractTrFeatures(
            (tokenized_tweet))))

    def showMostInformative(self):
        return self.classifier.show_most_informative_features(10)
