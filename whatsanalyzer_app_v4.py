
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re
import zipfile
from datetime import datetime, date

# Set page config
st.set_page_config(page_title="WhatsAnalyzer", layout="wide")

# Language toggle
language = st.sidebar.radio("🌐 בחר שפה / Choose language", ("עברית", "English"))
is_hebrew = language == "עברית"

# Labels
title = "📊 ניתוח שיחת וואטסאפ" if is_hebrew else "📊 WhatsApp Chat Analysis"
upload_text = "📁 העלה קובץ WhatsApp (.txt או .zip)" if is_hebrew else "📁 Upload WhatsApp Export File (.txt or .zip)"
overview_header = "סקירה כללית" if is_hebrew else "Overview"
user_analysis_header = "פילוח אישי" if is_hebrew else "Individual Analysis"
messages_per_day_label = "הודעות לפי יום" if is_hebrew else "Messages per Day"
messages_by_hour_label = "הודעות לפי שעה" if is_hebrew else "Messages by Hour"
messages_by_day_label = "הודעות לפי יום בשבוע" if is_hebrew else "Messages by Day of Week"
messages_over_time_label = "שינויים בפעילות לפי משתתף" if is_hebrew else "User Activity Over Time"
date_range_label = "בחר טווח תאריכים" if is_hebrew else "Select Date Range"

st.title(title)
uploaded_file = st.file_uploader(upload_text, type=["txt", "zip"])

def extract_txt_from_zip(zip_bytes):
    with zipfile.ZipFile(zip_bytes) as z:
        for name in z.namelist():
            if name.endswith(".txt"):
                return z.read(name).decode("utf-8")
    return None

if uploaded_file:
    if uploaded_file.name.endswith(".zip"):
        content = extract_txt_from_zip(uploaded_file)
        if not content:
            st.error("לא נמצא קובץ טקסט בתוך ה-ZIP" if is_hebrew else "No .txt file found inside the ZIP")
            st.stop()
    else:
        content = uploaded_file.read().decode("utf-8")

    pattern = r"(\d{1,2}/\d{1,2}/\d{2,4}), (\d{2}:\d{2}) - ([^:]+): (.+)"
    matches = re.findall(pattern, content)

    data = []
    for date_str, time, sender, message in matches:
        try:
            dt = datetime.strptime(f"{date_str} {time}", "%d/%m/%Y %H:%M")
            data.append([dt, sender, message])
        except ValueError:
            continue

    df = pd.DataFrame(data, columns=["datetime", "sender", "message"])
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    df = df.dropna(subset=["datetime"])
    df["date"] = df["datetime"].dt.date
    df["hour"] = df["datetime"].dt.hour
    df["weekday"] = df["datetime"].dt.day_name()

    # Show available date range
    min_date = df["date"].min()
    max_date = df["date"].max()

    if pd.isna(min_date) or pd.isna(max_date):
        st.warning("לא נמצאו תאריכים תקינים בקובץ." if is_hebrew else "No valid dates found in file.")
        st.stop()

    if isinstance(min_date, pd.Timestamp):
        min_date = min_date.date()
    if isinstance(max_date, pd.Timestamp):
        max_date = max_date.date()

    st.sidebar.markdown("### " + date_range_label)
    selected_range = st.sidebar.date_input(
        date_range_label,
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if isinstance(selected_range, tuple):
        df = df[(df["date"] >= selected_range[0]) & (df["date"] <= selected_range[1])]

    # Overview
    st.subheader(overview_header)
    col1, col2, col3 = st.columns(3)
    col1.metric("📅 תאריכים שונים" if is_hebrew else "📅 Unique Dates", df["date"].nunique())
    col2.metric("👥 משתתפים" if is_hebrew else "👥 Participants", df["sender"].nunique())
    col3.metric("💬 סה״כ הודעות" if is_hebrew else "💬 Total Messages", len(df))

    # Aggregates
    daily_activity = df.groupby("date").size()
    hourly_activity = df.groupby("hour").size()
    weekday_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    weekday_activity = df.groupby("weekday").size().reindex(weekday_order)
    sender_time = df.groupby([df["datetime"].dt.date, "sender"]).size().unstack(fill_value=0)

    st.markdown("### " + messages_per_day_label)
    st.line_chart(daily_activity)

    st.markdown("### " + messages_by_hour_label)
    st.bar_chart(hourly_activity)

    st.markdown("### " + messages_by_day_label)
    st.bar_chart(weekday_activity)

    st.markdown("### " + messages_over_time_label)
    st.line_chart(sender_time)

    # Individual user analysis
    st.subheader(user_analysis_header)
    selected_user = st.selectbox("בחר משתמש" if is_hebrew else "Select User", df["sender"].unique())
    user_df = df[df["sender"] == selected_user]
    user_daily = user_df.groupby("date").size()
    user_hourly = user_df.groupby("hour").size()
    user_weekday = user_df.groupby("weekday").size().reindex(weekday_order)

    st.markdown(f"#### {selected_user} – " + (messages_per_day_label if is_hebrew else "Messages per Day"))
    st.line_chart(user_daily)

    st.markdown(f"#### {selected_user} – " + (messages_by_hour_label if is_hebrew else "Messages by Hour"))
    st.bar_chart(user_hourly)

    st.markdown(f"#### {selected_user} – " + (messages_by_day_label if is_hebrew else "Messages by Day of Week"))
    st.bar_chart(user_weekday)
else:
    st.info("נא להעלות קובץ WhatsApp בפורמט .txt או .zip" if is_hebrew else "Please upload a WhatsApp .txt or .zip export file.")
