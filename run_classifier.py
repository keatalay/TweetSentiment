import tweet_classifier

#training_file = './trainingandtestdata/testdata.manual.2009.06.14.csv'
training_file = './trainingandtestdata/training.1600000.processed.noemoticon.csv'
classifier = tweet_classifier.TweetClassifier(training_file)
print('Initializing Tweet Classifier. . .')
classifier.trainClassifier()

tweet = ' '

while(tweet != 'end'):
    tweet = input(
        'Enter Tweet to be classified (enter \'end\' to end script execution): ')
    print(classifier.classifyTweet(tweet))
#    print(classifier.showMostInformative())
