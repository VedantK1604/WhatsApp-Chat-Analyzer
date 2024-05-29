from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji
import pandas as pd
extractor = URLExtract()

def fetch_stats(selected_user, df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    # Fetch number of messages
    num_messages = df.shape[0]

    # Fetch number of words
    words = []
    for word in df['message']:
        words.extend(word.split())

    words = len(words)

    #fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    #Fetch number of link shared
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    links = len(links)
    return num_messages, words, num_media_messages, links


def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    return x, df

def word_cloud(selected_user,df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    # Remove words 'group_notification, media_omitted and other stop words'
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=350, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    # Remove words 'group_notification, media_omitted and other stop words'
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_analysis(selected_user,df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month', 'month_num']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

# def week_activity_map(selected_user,df):
#     if selected_user != "Overall":
#         df = df[df['user'] == selected_user]

#     daily_activity = df['day_name'].value_counts().reset_index().rename(columns={'index':'day_name','day_name':'count'})
#     return daily_activity

def month_activity_map(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    return df['month'].value_counts().reset_index()

def activity_heat_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    activity_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return activity_heatmap