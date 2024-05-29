import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor, helper

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    #Converting byte data to string.
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    # st.dataframe(df)

    #Fetch unique users:
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show Analysis w.r.t.", user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        st.title('Top Statistics')
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)

        with col4:
            st.header("Links Shared")
            st.title(num_links)

        #Monthly Timeline
        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color="yellow")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Daily Timeline
        st.title('Daily Timeline')
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Week activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)
        # with col1:
        #     st.header('Most busy day')
        #     busy_day = helper.week_activity_map(selected_user,df)
        #     fig,ax = plt.subplots()
        #     ax.bar(busy_day['day_name'], busy_day['count'],color='black')
        #     plt.xticks(rotation='vertical')
        #     st.pyplot(fig)

        #Month Activity map:
        # with col2:
        #     st.header('Most busy Month')
        #     busy_month = helper.month_activity_map(selected_user, df)
        #     fig, ax = plt.subplots()
        #     ax.bar(busy_month['index'], busy_month['month'], color='purple')
        #     plt.xticks(rotation='vertical')
        #     st.pyplot(fig)

        #Activity heat map
        st.title('Weekly Activity Map')
        activity_heatmap = helper.activity_heat_map(selected_user,df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(activity_heatmap)
        st.pyplot(fig)

        #Finding the busiest users in the group (group level)
        if selected_user == "Overall":
            st.title("Most Busy Users")
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color="red")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        #WordCloud
        st.title('Wordcloud')
        df_wc = helper.word_cloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #Most common words
        most_common_df = helper.most_common_words(selected_user,df)

        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Most Common Words')
        st.pyplot(fig)

        #emoji Analysis
        emoji_df = helper.emoji_analysis(selected_user, df)
        st.title('Emoji Analysis')

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(10), labels=emoji_df[0].head(10), autopct="%0.2f")
            st.pyplot(fig)
