import matplotlib.pyplot as plt
import streamlit as st
import preprocessor, helper

st.sidebar.title("WhatsApp Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    st.dataframe(df)

# fetch unique user
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)
    if st.sidebar.button("Show Analysis"):

        # stats Area
        num_messages,words,num_media_messages,links = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
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
            st.header("Shared links")
            st.title(links)

        # Monthly time line


        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

       # daily time line

        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'],color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity Map
        st.title("Activity Map")
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.weekly_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.monthly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)







        # finding busiest person the group(overall)

    if selected_user == 'Overall':
        st.title('Most Busy user')
        x, new_df = helper.most_busy_users(df)
        fig, ax = plt.subplots()

        col1,col2 = st.columns(2)

        with col1:
            ax.bar(x.index, x.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.dataframe(new_df)

        #




