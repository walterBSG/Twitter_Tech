# Twitter Tech

Twitter Tech is a real-time sentiment analysis tool for tweets. It evaluates tweets as positive or negative and generates three types of outputs: a graph, a bar graph, and a word cloud.

## Outputs

1. Sentiment Analysis Graph: A graph showing the distribution of positive and negative tweets over time.

![Sentiment Analysis Graph Example](https://github.com/walterBSG/Twitter_Tech/blob/main/img/Example.png)

2. Tweet Bar Graph: A bar graph showing the number of positive and negative tweets.

![Tweet Bar Graph Example](https://github.com/walterBSG/Twitter_Tech/blob/main/img/tweetBar.png)

3. Word Cloud: A word cloud visualizing the most common words used in the tweets.

![Word Cloud Example](https://github.com/walterBSG/Twitter_Tech/blob/main/img/wordcloud.png)

## Usage

To run the program, open a command line interface and enter `python twitterJITClass.py`. You will be prompted for two inputs: the query and the number of searches. For each search, you will receive up to 100 tweets. The first 100 tweets are the most recent ones. For each additional request, you will receive tweets from one hour prior (due to limitations of the free Twitter API).

Before using the program, you must add your Twitter API credentials to the `config.py` file.

## Requirements

This project requires [Python 3](https://www.python.org/downloads/) and the following packages:
- [tweepy](https://github.com/tweepy/tweepy)
- [matplotlib](https://matplotlib.org/stable/index.html)
- [wordcloud](https://github.com/amueller/word_cloud)

## Contributions

Contributions are welcome!

## License

This project is licensed under the [MIT License](LICENSE).

