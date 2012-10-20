SMA - Social Media Analyser
===

What is it?
-----------
A application used to monitor and analyse new social media such as Twitter

Table of contents
---
* nosy
 * nosy - Contains the algorithms and utilites
  * algorithm 
   * lang.py - Try to determine the language. Currently uses word matching to a english dictionary and counts the number of matches.
   * persistent_classifier.py - An abstract classifier class that defines logic for saving/loading states to/from redis database.
   * naive_bayes.py - A persistent classifier implementing/using naive bayes
   * random_classifier.py - A classifier that emits random classifications, used for testing.
  * open_struct.py - a class that allows arbitrary fields to be set on it, modelled after Ruby's OpenStruct class.
  * mongo_open_struct.py - An OpenStruct that can be persisted to MongoDB, and also loaded by searching.
  * base.py - Base class for both Classification and Classified Objects. Contains logic for normalizing text before insertion into the database.
  * model.py - Defines ClassificationObject and ClassifiedObject, which are MongoOpenStructs. ClassificationObjects are stored in the corpus, before classification, and ClassifiedObjects are ClassificationObjects that have been classified.
  * stream_handler.py - StreamHandler is an abstract class that consumes HTTP streams. TwitterHandler is a StreamHandler that connects to Twitter's API. 
 * classifier
  * classify_handler.py - A REST end-point for the classifiers. 
  See ADD for parameters
  * tweet_classifier.py - Consum JSON from the Twitter stream and saves it in the proper format to the mongoDB.
  * run_classifier.sh - Basch script to run the tweet_classifier.py with correct arguments.
  * stream_example.rb - A example demonstrating real-time publishing using Juggernaut library (JavaScript). NOTE: Deprecated. HTML5 offers server sent event which replicates the Juggernaut functionality.
 * corpus - Logic for interacting with the corpus
  * corpus_handler.py - A REST end-point for browsing the corpus
  * tweet_harvester.py - Runs a TwitterHandler and transforms Twitter's JSON into our classification objects.
 * flicktweet-scraper - Example tweets about movies from www.flicktweets.com. These were used in our demo session.
 * move_reviews - Corpus with positivite and negative move reviews. A script inserts these into the corpus as classification objects. Used in our demo session.
* setup.py and reinstall - installs the nosy library into Python's site-packages.