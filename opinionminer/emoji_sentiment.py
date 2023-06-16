import csv
import re

emoji_sentiment_dict = {}

with open('Emoji_Sentiment_Data_v1.0.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        emoji = row['Emoji']
        positive = int(row['Positive'])
        negative = int(row['Negative'])
        neutral = int(row['Neutral'])
        sentiment_score = (positive - negative) / (positive + negative + neutral)
        emoji_sentiment_dict[emoji] = sentiment_score


def get_emoji_sentiment(text):
    emojis = re.findall(r'[^\w\s,]', text)
    sentiment_scores = [emoji_sentiment_dict.get(emoji, 0) for emoji in emojis]

    # Return average sentiment score if there are any emojis, else return 0
    return sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0



def is_emoji(s):
    emojis = re.findall(r'[^\w\s,]', s)
    for emoji in emojis:
        if '\U0001F300' <= emoji <= '\U0001F5FF' or '\U0001F600' <= emoji <= '\U0001F64F' or '\U0001F680' <= emoji <= '\U0001F6FF' or '\U0001F700' <= emoji <= '\U0001F77F' or '\U0001F780' <= emoji <= '\U0001F7FF' or '\U0001F800' <= emoji <= '\U0001F8FF' or '\U0001F900' <= emoji <= '\U0001F9FF' or '\U0001FA00' <= emoji <= '\U0001FA6F' or '\U0001FA70' <= emoji <= '\U0001FAFF' or '\U00002702' <= emoji <= '\U000027B0' or '\U0001F1E6' <= emoji <= '\U0001F1FF':
            return True
    return False

text = "Joe Biden is the easiest President to criticize in American History.  And yet the American Media refuses to do it. If it’s not Fox or the New York Post you won’t see any criticism about Joe Biden."
print(is_emoji(text))

def get_emojis(s):
    emojis = re.findall(r'[^\w\s,]', s)
    emoji_list = [emoji for emoji in emojis if '\U0001F300' <= emoji <= '\U0001F5FF' or '\U0001F600' <= emoji <= '\U0001F64F' or '\U0001F680' <= emoji <= '\U0001F6FF' or '\U0001F700' <= emoji <= '\U0001F77F' or '\U0001F780' <= emoji <= '\U0001F7FF' or '\U0001F800' <= emoji <= '\U0001F8FF' or '\U0001F900' <= emoji <= '\U0001F9FF' or '\U0001FA00' <= emoji <= '\U0001FA6F' or '\U0001FA70' <= emoji <= '\U0001FAFF' or '\U00002702' <= emoji <= '\U000027B0' or '\U0001F1E6' <= emoji <= '\U0001F1FF']
    return emoji_list


def get_emoji_sentiment(emojis):
    sentiment_scores = [emoji_sentiment_dict.get(emoji, 0) for emoji in emojis]
    filtered_scores = [score for score in sentiment_scores if score != 0] # the filter is applied since not all the emojis included in our Emoji Sentiment data
    return filtered_scores


emoji_list = get_emojis("I love pizza 🍕, 🥳, ❤️, 🪩")
sentiment_scores = get_emoji_sentiment(emoji_list)
print(sentiment_scores)

def emoji_scoring(s):
    emojis = re.findall(r'[^\w\s,]', s)
    emoji_list = [emoji for emoji in emojis if '\U0001F300' <= emoji <= '\U0001F5FF' or '\U0001F600' <= emoji <= '\U0001F64F' or '\U0001F680' <= emoji <= '\U0001F6FF' or '\U0001F700' <= emoji <= '\U0001F77F' or '\U0001F780' <= emoji <= '\U0001F7FF' or '\U0001F800' <= emoji <= '\U0001F8FF' or '\U0001F900' <= emoji <= '\U0001F9FF' or '\U0001FA00' <= emoji <= '\U0001FA6F' or '\U0001FA70' <= emoji <= '\U0001FAFF' or '\U00002702' <= emoji <= '\U000027B0' or '\U0001F1E6' <= emoji <= '\U0001F1FF']
    return get_emoji_sentiment(emoji_list)

print("HERE!")
print(emoji_scoring("I love pizza 😡"))

