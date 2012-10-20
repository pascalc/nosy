(ns flicktweet-scraper.core
  (:require [net.cgrand.enlive-html :as html]
            [clojure.string :as string]
            [cheshire.core :as cheshire])
  (:import [java.util Date])
  (:gen-class))

(def base-url "http://www.flicktweets.com/")
(def out-file "movie-tweets.json")

(defn fetch-url [url]
  (html/html-resource (java.net.URL. url)))

(defn scrape [selector]
  (map html/text (html/select (fetch-url base-url) selector)))

(def tweet-text (map string/trim (scrape [:p.tweet_text])))

(defn jsonify [text]
  {:text text
   :created_at (.toString (Date.))
   :user { :screen_name "EXAMPLE" }
   :geo nil})

(defn print-tweets-to-file [filename]
  (spit filename (cheshire/generate-string (map jsonify tweet-text))))

(defn -main []
  (println (str "Fetching tweets from " base-url " and saving them to " out-file))
  (print-tweets-to-file out-file))