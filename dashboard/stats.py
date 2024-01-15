import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import json

page_config = st.set_page_config(
    page_title="Sözcük App Dashboard",
    page_icon="📊",
    layout="centered",
)

db_creds = json.load(open("db_creds.json", "r"))

engine = create_engine(
    f"mysql+mysqlconnector://{db_creds['USER']}:{db_creds['PASSWORD']}@{db_creds['HOST']}:{db_creds['PORT']}/{db_creds['NAME']}",
    echo=False,
)

query_competitors = "SELECT * FROM Competitors"
query_visitors = "SELECT * FROM Visitors"
query_words = "SELECT * FROM Words"


@st.cache_data
def get_data(query):
    return pd.read_sql(query, engine)


st.title("Sözcük App Dashboard")

st.header("Competitors")
st.info("Only the competitors with the username provided are shown.")
st.subheader("KPIs")

competitors = get_data(query_competitors)

competitors_1_ts, competitors_2_ts, competitors_3_ts = st.columns(3)

# All-time competitor count
with competitors_1_ts:
    st.metric(label="All-time Competitor Count", value=competitors.shape[0])

# Compare with last month
this_month_competior_count = competitors[
    competitors["dateCreated"] > datetime.now() - timedelta(days=30)
].shape[0]
last_month_competior_count = competitors[
    (competitors["dateCreated"] > datetime.now() - timedelta(days=60))
    & (competitors["dateCreated"] < datetime.now() - timedelta(days=30))
].shape[0]

with competitors_2_ts:
    st.metric(
        label="Monthly Competitor Count",
        value=this_month_competior_count,
        delta=f"{this_month_competior_count - last_month_competior_count} vs last month",
    )

# Compare with last week
this_week_competior_count = competitors[
    competitors["dateCreated"] > datetime.now() - timedelta(days=7)
].shape[0]
last_week_competior_count = competitors[
    (competitors["dateCreated"] > datetime.now() - timedelta(days=14))
    & (competitors["dateCreated"] < datetime.now() - timedelta(days=7))
].shape[0]

with competitors_3_ts:
    st.metric(
        label="Weekly Competitor Count",
        value=this_week_competior_count,
        delta=f"{this_week_competior_count - last_week_competior_count} vs last week",
    )

competitors_1_sc, competitors_2_sc, competitors_3_sc = st.columns(3)

# Average score
with competitors_1_sc:
    st.metric(
        label="Average Score",
        value=int(competitors["score"].mean()),
    )

# Average score this month
this_month_score = int(
    competitors[competitors["dateCreated"] > datetime.now() - timedelta(days=30)][
        "score"
    ].mean()
)

with competitors_2_sc:
    st.metric(
        label="Average Score This Month",
        value=this_month_score,
    )

# Average score this week
this_week_score = int(
    competitors[competitors["dateCreated"] > datetime.now() - timedelta(days=7)][
        "score"
    ].mean()
) if this_week_competior_count > 0 else 0

with competitors_3_sc:
    st.metric(
        label="Average Score This Week",
        value=this_week_score,
    )

competitors_1_fan, competitors_2_fan, competitors_3_fan = st.columns(3)

# Biggest fan (depends on the occurrence of the username
biggest_fan = competitors["name"].value_counts().index[0]

with competitors_1_fan:
    st.metric(
        label="🥇 Biggest Fan",
        value=biggest_fan,
        delta=f"{competitors['name'].value_counts()[0]} times",
        delta_color="off",
    )

# Second biggest fan
second_biggest_fan = competitors["name"].value_counts().index[1]

with competitors_2_fan:
    st.metric(
        label="🥈 Second Biggest Fan",
        value=second_biggest_fan,
        delta=f"{competitors['name'].value_counts()[1]} times",
        delta_color="off",
    )

# Third biggest fan
third_biggest_fan = competitors["name"].value_counts().index[2]

with competitors_3_fan:
    st.metric(
        label="🥉 Third Biggest Fan",
        value=third_biggest_fan,
        delta=f"{competitors['name'].value_counts()[2]} times",
        delta_color="off",
    )

st.subheader("Competitor Count Time-Series")

competitors["dateCreated"] = pd.to_datetime(competitors["dateCreated"])
competitors = competitors.set_index("dateCreated")

competitors = competitors.resample("D").count()

st.bar_chart(competitors["id"])


st.header("Visitors")

visitors = get_data(query_visitors)

st.subheader("KPIs")

# All-time visitor count
visitors_1, visitors_2, visitors_3 = st.columns(3)

with visitors_1:
    st.metric(label="All-time Visitor Count", value=visitors.shape[0])

# Compare with last month
this_month_visitor_count = visitors[
    visitors["dateCreated"] > datetime.now() - timedelta(days=30)
].shape[0]
last_month_visitor_count = visitors[
    (visitors["dateCreated"] > datetime.now() - timedelta(days=60))
    & (visitors["dateCreated"] < datetime.now() - timedelta(days=30))
].shape[0]

with visitors_2:
    st.metric(
        label="Monthly Visitor Count",
        value=this_month_visitor_count,
        delta=f"{this_month_visitor_count - last_month_visitor_count} vs last month",
    )

# Compare with last week
this_week_visitor_count = visitors[
    visitors["dateCreated"] > datetime.now() - timedelta(days=7)
].shape[0]
last_week_visitor_count = visitors[
    (visitors["dateCreated"] > datetime.now() - timedelta(days=14))
    & (visitors["dateCreated"] < datetime.now() - timedelta(days=7))
].shape[0]

with visitors_3:
    st.metric(
        label="Weekly Visitor Count",
        value=this_week_visitor_count,
        delta=f"{this_week_visitor_count - last_week_visitor_count} vs last week",
    )

visitors_1_top, visitors_2_top, visitors_3_top = st.columns(3)

# Top visitor (ip)
with visitors_1_top:
    top_visitor = visitors["ip"].value_counts().index[0]
    st.metric(
        label="🥇 Top Visitor",
        value=top_visitor,
        delta=f"{visitors['ip'].value_counts()[0]} times",
        delta_color="off",
    )

# Second top visitor (ip)
with visitors_2_top:
    second_top_visitor = visitors["ip"].value_counts().index[1]
    st.metric(
        label="🥈 Second Top Visitor",
        value=second_top_visitor,
        delta=f"{visitors['ip'].value_counts()[1]} times",
        delta_color="off",
    )

# Third top visitor (ip)
with visitors_3_top:
    third_top_visitor = visitors["ip"].value_counts().index[2]
    st.metric(
        label="🥉 Third Top Visitor",
        value=third_top_visitor,
        delta=f"{visitors['ip'].value_counts()[2]} times",
        delta_color="off",
    )

st.subheader("Visitor Count Time-Series")

visitors["dateCreated"] = pd.to_datetime(visitors["dateCreated"])
visitors = visitors.set_index("dateCreated")

visitors = visitors.resample("D").count()

st.bar_chart(visitors["id"])


st.header("Words")

words = get_data(query_words)

# Remaning days before word bank is empty (biggest releaseDate - today)
remaining_days = (words["releaseDate"].max() - datetime.now()).days

st.warning(f"{round(remaining_days/365, 2)} years left before the word bank is empty.")

words_1, words_2, words_3 = st.columns(3)

# Total word count
with words_1:
    st.metric(label="Total Word Count", value=words.shape[0])

# Remaining word count (where releaseDate is bigger than today)
with words_2:
    st.metric(
        label="Remaining Word Count",
        value=words[words["releaseDate"] > datetime.now()].shape[0],
    )

with words_3:
    st.metric(
        label="Remaining Days",
        value=remaining_days,
    )

word_list_1, word_list_2 = st.columns(2)

today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
tomorrow = today + timedelta(days=1)

# Today's words and definitions
todays_words = words[words["releaseDate"] == today]

with word_list_1:
    st.subheader("Today's Words")
    for index, row in todays_words.iterrows():
        st.write(f"{row['word']} - {row['definition']}")

# Tomorrow's words and definitions
tomorrows_words = words[words["releaseDate"] == tomorrow]

with word_list_2:
    st.subheader("Tomorrow's Words")
    for index, row in tomorrows_words.iterrows():
        st.write(f"{row['word']} - {row['definition']}")

st.subheader("Words by Release Date")
st.markdown("Select a date to see the words released on that day.")

selected_date = st.date_input("Release date", datetime.now())
# Converting to datetime
selected_date = datetime.combine(selected_date, datetime.min.time())
selected_date = selected_date.replace(hour=0, minute=0, second=0, microsecond=0)

selected_words = words[words["releaseDate"] == selected_date]

if selected_words.shape[0] != 0:
    for index, row in selected_words.iterrows():
        st.write(f"{row['word']} - {row['definition']}")

else:
    st.error("Release date is out of range.")