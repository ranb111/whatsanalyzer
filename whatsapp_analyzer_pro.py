import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import re
import zipfile
import io
from datetime import datetime, timedelta
import emoji
import numpy as np

# Page configuration
st.set_page_config(
    page_title="WhatsApp Analyzer Pro",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .section-header {
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem 1.5rem;
        border-radius: 8px;
        color: white;
        margin: 1.5rem 0 1rem 0;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin: 0.5rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1rem;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Language selection
language = st.sidebar.radio("Language / שפה", ("עברית", "English"), horizontal=True)
is_hebrew = language == "עברית"

# Labels
if is_hebrew:
    page_title = "📱 מנתח WhatsApp Pro"
    upload_label = "העלה קובץ WhatsApp (.txt או .zip)"
    processing_label = "מעבד קובץ..."
    no_file_label = "אנא העלה קובץ WhatsApp"
    total_messages = "סה״כ הודעות"
    participants = "משתתפים"
    active_days = "ימים פעילים"
    messages_per_day = "הודעות ליום"
    most_active_user = "המשתמש הפעיל ביותר"
    daily_average = "ממוצע יומי"
    active_participants = "משתתפים פעילים"
    leaderboard_title = "🏆 דירוג המובילים"
    messages_leaderboard = "הכי הרבה הודעות"
    weekly_breakdown = "פילוח לפי ימים בשבוע"
    monthly_breakdown = "פילוח לפי ימים בחודש"
    hourly_breakdown = "פילוח לפי שעות"
    interesting_facts = "עובדות מעניינות"
    longest_messages = "ההודעות הארוכות ביותר"
    most_haha = "הכי הרבה חחח"
    most_emojis = "הכי הרבה אימוג'י"
    most_media = "הכי הרבה מדיה"
    date_range = "טווח תאריכים"
    last_60_days = "60 ימים אחרונים"
    all_time = "כל התקופה"
    custom_range = "טווח מותאם אישית"
    personal_analysis = "ניתוח אישי"
    select_user = "בחר משתמש לניתוח"
    user_messages = "הודעות"
    user_emojis = "אימוג'י"
    user_media = "מדיה"
    user_percentage = "אחוז הודעות"
    fun_facts = "עובדות מצחיקות"
    top_chatter = "הכי מדבר"
    the_digger = "החופר"
    emoji_king = "מלך האימוג'י"
    the_ghost = "הרוח"
    morning_champion = "אלוף הבוקר טוב"
    sticker_addict = "מכור הסטיקרים"
    explanation_top_chatter = "מי שלח הכי הרבה הודעות בקבוצה"
    explanation_digger = "מי שלח את ההודעה הכי ארוכה (הכי הרבה תווים)"
    explanation_emoji_king = "מי השתמש הכי הרבה באימוג'י"
    explanation_ghost = "מי שלח הכי פחות הודעות (הכי שקט)"
    explanation_morning_champion = "מי אמר הכי הרבה 'בוקר טוב' או 'good morning'"
    explanation_sticker_addict = "מי שלח הכי הרבה מדיה (תמונות, וידאו, סטיקרים)"
else:
    page_title = "📱 WhatsApp Analyzer Pro"
    upload_label = "Upload WhatsApp file (.txt or .zip)"
    processing_label = "Processing file..."
    no_file_label = "Please upload a WhatsApp file"
    total_messages = "Total Messages"
    participants = "Participants"
    active_days = "Active Days"
    messages_per_day = "Messages per Day"
    most_active_user = "Most Active User"
    daily_average = "Daily Average"
    active_participants = "Active Participants"
    leaderboard_title = "🏆 Leaderboards"
    messages_leaderboard = "Most Messages"
    weekly_breakdown = "Weekly Breakdown"
    monthly_breakdown = "Monthly Breakdown"
    hourly_breakdown = "Hourly Breakdown"
    interesting_facts = "Interesting Facts"
    longest_messages = "Longest Messages"
    most_haha = "Most Haha"
    most_emojis = "Most Emojis"
    most_media = "Most Media"
    date_range = "Date Range"
    last_60_days = "Last 60 Days"
    all_time = "All Time"
    custom_range = "Custom Range"
    personal_analysis = "Personal Analysis"
    select_user = "Select user for analysis"
    user_messages = "Messages"
    user_emojis = "Emojis"
    user_media = "Media"
    user_percentage = "Message Percentage"
    fun_facts = "Fun Facts"
    top_chatter = "Top Chatter"
    the_digger = "The Digger"
    emoji_king = "Emoji King/Queen"
    the_ghost = "The Ghost"
    morning_champion = "Good Morning Champion"
    sticker_addict = "Sticker Addict"
    explanation_top_chatter = "Who sent the most messages in the group"
    explanation_digger = "Who sent the longest message (most characters)"
    explanation_emoji_king = "Who used the most emojis"
    explanation_ghost = "Who sent the least messages (quietest)"
    explanation_morning_champion = "Who said 'good morning' the most"
    explanation_sticker_addict = "Who sent the most media (photos, videos, stickers)"

# Main title
st.markdown(f'<div class="main-header"><h1>{page_title}</h1></div>', unsafe_allow_html=True)

def extract_txt_from_zip(zip_bytes):
    """Extract txt file from zip with error handling"""
    try:
        with zipfile.ZipFile(io.BytesIO(zip_bytes), 'r') as zip_file:
            for file_name in zip_file.namelist():
                if file_name.endswith('.txt'):
                    return zip_file.read(file_name).decode('utf-8')
        return None
    except Exception as e:
        st.error(f"Error reading zip file: {e}")
        return None

def parse_whatsapp_content(content):
    """Parse WhatsApp chat content with multiple format support"""
    messages = []
    
    # Multiple regex patterns for different WhatsApp formats
    patterns = [
        # Standard format: 29/07/2025, 20:30 - User: Message
        r'(\d{1,2}/\d{1,2}/\d{2,4}),?\s+(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AP]M)?)\s*-\s*([^:]+):\s*(.+)',
        # Bracket format: [29/07/2025, 20:30] User: Message
        r'\[(\d{1,2}/\d{1,2}/\d{2,4}),?\s+(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AP]M)?)\]\s*([^:]+):\s*(.+)',
        # No comma format: 29/07/2025 20:30 - User: Message
        r'(\d{1,2}/\d{1,2}/\d{2,4})\s+(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AP]M)?)\s*-\s*([^:]+):\s*(.+)',
        # ISO format: 2025-07-29 20:30 - User: Message
        r'(\d{4}-\d{1,2}-\d{1,2})\s+(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AP]M)?)\s*-\s*([^:]+):\s*(.+)',
        # Alternative format: 29.07.2025 20:30 - User: Message
        r'(\d{1,2}\.\d{1,2}\.\d{2,4})\s+(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AP]M)?)\s*-\s*([^:]+):\s*(.+)'
    ]
    
    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        for pattern in patterns:
            match = re.match(pattern, line)
            if match:
                date_str, time_str, sender, message = match.groups()
                
                # Parse date
                try:
                    if '/' in date_str:
                        # Check if it's MM/DD/YY format (like 11/20/16)
                        parts = date_str.split('/')
                        if len(parts) == 3:
                            if len(parts[2]) == 2:  # YY format
                                # Convert YY to YYYY
                                parts[2] = '20' + parts[2]
                                date_str = '/'.join(parts)
                            
                            # Try MM/DD/YYYY first (American format)
                            try:
                                date_obj = datetime.strptime(date_str, '%m/%d/%Y')
                            except:
                                # Try DD/MM/YYYY (European format)
                                date_obj = datetime.strptime(date_str, '%d/%m/%Y')
                    elif '-' in date_str:
                        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    elif '.' in date_str:
                        date_obj = datetime.strptime(date_str, '%d.%m.%Y')
                    else:
                        continue
                except:
                    continue
                
                # Parse time
                try:
                    if 'AM' in time_str or 'PM' in time_str:
                        time_obj = datetime.strptime(time_str, '%I:%M:%S %p').time()
                    else:
                        time_obj = datetime.strptime(time_str, '%H:%M').time()
                except:
                    try:
                        time_obj = datetime.strptime(time_str, '%H:%M:%S').time()
                    except:
                        continue
                
                # Combine date and time
                datetime_obj = datetime.combine(date_obj.date(), time_obj)
                
                messages.append({
                    'datetime': datetime_obj,
                    'sender': sender.strip(),
                    'message': message.strip()
                })
                break
    
    # Debug: Show first few lines if no messages found
    if not messages:
        st.warning("לא נמצאו הודעות. בואו נבדוק את הפורמט של הקובץ:")
        st.code(content[:500])
    
    return pd.DataFrame(messages)

def create_leaderboards(df):
    """Create comprehensive leaderboards"""
    leaderboards = {}
    
    # 1. Most messages
    user_message_counts = df['sender'].value_counts()
    leaderboards['most_messages'] = user_message_counts
    
    # 2. Most emojis
    all_emojis = []
    for message in df['message']:
        all_emojis.extend(emoji.emoji_list(message))
    emoji_counts = Counter([e['emoji'] for e in all_emojis])
    leaderboards['most_emojis'] = emoji_counts.most_common(10)
    
    # 3. Longest messages
    df['message_length'] = df['message'].str.len()
    longest_messages = df.nlargest(10, 'message_length')[['sender', 'message', 'message_length', 'datetime']]
    leaderboards['longest_messages'] = longest_messages
    
    # 4. Most media messages
    media_messages = df[df['message'].str.contains(r'<.*?>', na=False)]
    media_counts = media_messages['sender'].value_counts()
    leaderboards['most_media'] = media_counts
    
    # 5. Most "haha" messages
    haha_messages = df[df['message'].str.contains(r'חחח|haha|ההה|lol', case=False, na=False)]
    haha_counts = haha_messages['sender'].value_counts()
    leaderboards['most_haha'] = haha_counts
    
    return leaderboards

def create_time_breakdowns(df):
    """Create time-based breakdowns"""
    breakdowns = {}
    
    # 1. Weekly breakdown (days of week)
    df['weekday'] = df['datetime'].dt.day_name()
    weekday_counts = df['weekday'].value_counts()
    breakdowns['weekly'] = weekday_counts
    
    # 2. Monthly breakdown (days of month)
    df['day_of_month'] = df['datetime'].dt.day
    day_counts = df['day_of_month'].value_counts().sort_index()
    breakdowns['monthly'] = day_counts
    
    # 3. Hourly breakdown
    df['hour'] = df['datetime'].dt.hour
    hour_counts = df['hour'].value_counts().sort_index()
    breakdowns['hourly'] = hour_counts
    
    return breakdowns

def get_interesting_facts(df, leaderboards):
    """Generate interesting facts and insights"""
    facts = []
    
    if not df.empty:
        total_messages = len(df)
        total_users = df['sender'].nunique()
        
        # Most active user percentage
        most_active = leaderboards['most_messages'].index[0]
        most_active_count = leaderboards['most_messages'].iloc[0]
        most_active_percentage = (most_active_count / total_messages) * 100
        
        facts.append(f"👑 {most_active} מהווה {most_active_percentage:.1f}% מההודעות בקבוצה" if is_hebrew else f"👑 {most_active} represents {most_active_percentage:.1f}% of all messages")
        
        # Most active hour
        most_active_hour = df['datetime'].dt.hour.value_counts().index[0]
        facts.append(f"🕐 השעה הפעילה ביותר: {most_active_hour}:00" if is_hebrew else f"🕐 Most active hour: {most_active_hour}:00")
        
        # Most active day
        most_active_day = df['datetime'].dt.day_name().value_counts().index[0]
        facts.append(f"📅 היום הפעיל ביותר: {most_active_day}" if is_hebrew else f"📅 Most active day: {most_active_day}")
        
        # Average messages per day
        avg_per_day = total_messages / df['datetime'].dt.date.nunique()
        facts.append(f"📊 ממוצע יומי: {avg_per_day:.1f} הודעות" if is_hebrew else f"📊 Daily average: {avg_per_day:.1f} messages")
        
        # Most emoji user
        if leaderboards['most_emojis']:
            top_emoji = leaderboards['most_emojis'][0][0]
            facts.append(f"😄 האימוג'י הפופולרי ביותר: {top_emoji}" if is_hebrew else f"😄 Most popular emoji: {top_emoji}")
    
    return facts

def create_fun_facts(df, leaderboards):
    """Create fun and humorous insights"""
    facts = []
    
    if df.empty:
        return facts
    
    # Top chatter
    top_chatter = leaderboards['most_messages'].index[0]
    if is_hebrew:
        facts.append(f"🏆 {top_chatter}: {leaderboards['most_messages'].iloc[0]} הודעות - {explanation_top_chatter}")
    else:
        facts.append(f"🏆 {top_chatter}: {leaderboards['most_messages'].iloc[0]} messages - {explanation_top_chatter}")
    
    # The digger (longest message)
    if not leaderboards['longest_messages'].empty:
        digger = leaderboards['longest_messages'].iloc[0]
        if is_hebrew:
            facts.append(f"📚 {digger['sender']}: {digger['message_length']} תווים - {explanation_digger}")
        else:
            facts.append(f"📚 {digger['sender']}: {digger['message_length']} characters - {explanation_digger}")
    
    # Emoji king/queen
    emoji_counts = {}
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    
    for sender in df['sender'].unique():
        user_messages = df[df['sender'] == sender]['message'].str.cat(sep=' ')
        emoji_counts[sender] = len(emoji_pattern.findall(user_messages))
    
    if emoji_counts:
        emoji_king = max(emoji_counts, key=emoji_counts.get)
        if is_hebrew:
            facts.append(f"👑 {emoji_king}: {emoji_counts[emoji_king]} אימוג'י - {explanation_emoji_king}")
        else:
            facts.append(f"👑 {emoji_king}: {emoji_counts[emoji_king]} emojis - {explanation_emoji_king}")
    
    # The ghost (least active)
    ghost = leaderboards['most_messages'].index[-1]
    if is_hebrew:
        facts.append(f"👻 {ghost}: {leaderboards['most_messages'].iloc[-1]} הודעות - {explanation_ghost}")
    else:
        facts.append(f"👻 {ghost}: {leaderboards['most_messages'].iloc[-1]} messages - {explanation_ghost}")
    
    # Good morning champion
    morning_keywords = ['בוקר טוב', 'good morning', 'בוקר', 'morning']
    morning_counts = {}
    for sender in df['sender'].unique():
        user_messages = df[df['sender'] == sender]['message'].str.lower()
        morning_counts[sender] = sum(1 for msg in user_messages if any(keyword in msg for keyword in morning_keywords))
    
    if morning_counts and max(morning_counts.values()) > 0:
        morning_champion = max(morning_counts, key=morning_counts.get)
        if is_hebrew:
            facts.append(f"🌅 {morning_champion}: {morning_counts[morning_champion]} פעמים - {explanation_morning_champion}")
        else:
            facts.append(f"🌅 {morning_champion}: {morning_counts[morning_champion]} times - {explanation_morning_champion}")
    
    # Sticker addict
    sticker_keywords = ['<Media omitted>', 'sticker']
    sticker_counts = {}
    for sender in df['sender'].unique():
        user_messages = df[df['sender'] == sender]['message'].str.lower()
        sticker_counts[sender] = sum(1 for msg in user_messages if any(keyword in msg for keyword in sticker_keywords))
    
    if sticker_counts and max(sticker_counts.values()) > 0:
        sticker_addict = max(sticker_counts, key=sticker_counts.get)
        if is_hebrew:
            facts.append(f"🎯 {sticker_addict}: {sticker_counts[sticker_addict]} מדיה - {explanation_sticker_addict}")
        else:
            facts.append(f"🎯 {sticker_addict}: {sticker_counts[sticker_addict]} media - {explanation_sticker_addict}")
    
    return facts

# Instructions for exporting WhatsApp chat
st.markdown("## 📋 " + ("איך לייצא צ'אט מווטסאפ" if is_hebrew else "How to Export WhatsApp Chat"))
st.markdown("""
### **שלבים לייצוא:**
1. **פתח את ווטסאפ** במחשב או בטלפון
2. **היכנס לקבוצה** שברצונך לנתח
3. **לחץ על שם הקבוצה** בראש הצ'אט
4. **בחר 'ייצוא צ'אט'** (Export Chat)
5. **בחר 'ללא מדיה'** (Without Media) - זה מהיר יותר
6. **שמור את הקובץ** במחשב

### **סוגי קבצים נתמכים:**
- **קובץ .txt** - ייצוא רגיל
- **קובץ .zip** - ייצוא עם מדיה (נדרש חילוץ)

### **הערות:**
- הקובץ צריך להיות בפורמט ווטסאפ סטנדרטי
- מומלץ לייצא 'ללא מדיה' לביצועים טובים יותר
- הקובץ יכול להיות גדול - זה בסדר
""")

# File upload
uploaded_file = st.file_uploader(upload_label, type=['txt', 'zip'])

if uploaded_file:
    with st.spinner(processing_label):
        if uploaded_file.name.endswith(".zip"):
            content = extract_txt_from_zip(uploaded_file.read())
            if not content:
                st.error("לא ניתן לקרוא קובץ מהארכיון" if is_hebrew else "Cannot read file from archive")
                st.stop()
        else:
            content = uploaded_file.read().decode('utf-8')
        
        # Parse content
        df = parse_whatsapp_content(content)
        
        if df.empty:
            st.error("לא נמצאו הודעות בקובץ" if is_hebrew else "No messages found in file")
            st.stop()
        
        # Date range filter
        st.markdown(f'<div class="section-header">📅 {date_range}</div>', unsafe_allow_html=True)
        
        date_option = st.selectbox(
            "בחר טווח תאריכים" if is_hebrew else "Select date range",
            [last_60_days, all_time, custom_range],
            index=0
        )
        
        if date_option == last_60_days:
            latest_date = df['datetime'].max()
            sixty_days_ago = latest_date - timedelta(days=60)
            df_filtered = df[df['datetime'] >= sixty_days_ago]
        elif date_option == custom_range:
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("תאריך התחלה" if is_hebrew else "Start date", value=df['datetime'].min().date())
            with col2:
                end_date = st.date_input("תאריך סיום" if is_hebrew else "End date", value=df['datetime'].max().date())
            df_filtered = df[(df['datetime'].dt.date >= start_date) & (df['datetime'].dt.date <= end_date)]
        else:
            df_filtered = df
        
        if df_filtered.empty:
            st.warning("אין נתונים בטווח התאריכים שנבחר" if is_hebrew else "No data in selected date range")
            df_filtered = df
        
        # User filter
        st.markdown("### " + ("סינון משתמשים" if is_hebrew else "User Filter"))
        all_users = df_filtered['sender'].unique()
        selected_users = st.multiselect(
            "בחר משתמשים" if is_hebrew else "Select users",
            options=all_users,
            default=all_users,
            help="בחר משתמשים לניתוח. אם לא נבחר אף אחד, יוצגו כל המשתמשים." if is_hebrew else "Select users for analysis. If none selected, all users will be shown."
        )
        
        # Filter by selected users
        if selected_users:
            df_filtered = df_filtered[df_filtered['sender'].isin(selected_users)]
        
        # Create leaderboards and breakdowns
        leaderboards = create_leaderboards(df_filtered)
        breakdowns = create_time_breakdowns(df_filtered)
        facts = get_interesting_facts(df_filtered, leaderboards)
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(total_messages, f"{len(df_filtered):,}")
        
        with col2:
            st.metric(participants, df_filtered['sender'].nunique())
        
        with col3:
            st.metric(active_days, df_filtered['datetime'].dt.date.nunique())
        
        with col4:
            avg_per_day = len(df_filtered) / df_filtered['datetime'].dt.date.nunique()
            st.metric(messages_per_day, f"{avg_per_day:.1f}")
        
        # Interesting facts
        st.markdown(f'<div class="section-header">💡 {interesting_facts}</div>', unsafe_allow_html=True)
        for fact in facts:
            st.info(fact)
        

        
        # Personal Analysis
        st.markdown(f'<div class="section-header">👤 {personal_analysis}</div>', unsafe_allow_html=True)
        
        users = df_filtered['sender'].unique()
        selected_user = st.selectbox(select_user, options=users)
        
        if selected_user:
            user_data = df_filtered[df_filtered['sender'] == selected_user]
            
            # User stats
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(user_messages, len(user_data))
            
            with col2:
                # Count emojis using regex pattern
                emoji_pattern = re.compile("["
                    u"\U0001F600-\U0001F64F"  # emoticons
                    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                    u"\U0001F680-\U0001F6FF"  # transport & map symbols
                    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                    u"\U00002702-\U000027B0"
                    u"\U000024C2-\U0001F251"
                    "]+", flags=re.UNICODE)
                emoji_count = len(emoji_pattern.findall(' '.join(user_data['message'])))
                st.metric(user_emojis, emoji_count)
            
            with col3:
                media_count = sum(1 for msg in user_data['message'] if '<Media omitted>' in str(msg))
                st.metric(user_media, media_count)
            
            # User percentage of total activity
            user_percentage_of_total = (len(user_data) / len(df_filtered)) * 100
            st.info(f"משתמש זה מהווה {user_percentage_of_total:.1f}% מהפעילות הכללית בקבוצה" if is_hebrew else f"This user represents {user_percentage_of_total:.1f}% of total group activity")
            
            # Additional user stats
            col1, col2 = st.columns(2)
            
            with col1:
                # Average message length (characters)
                avg_chars = user_data['message'].str.len().mean()
                st.metric("אורך ממוצע (תווים)" if is_hebrew else "Avg Length (chars)", f"{avg_chars:.1f}")
                
                # Average message length (words)
                avg_words = user_data['message'].str.split().str.len().mean()
                st.metric("אורך ממוצע (מילים)" if is_hebrew else "Avg Length (words)", f"{avg_words:.1f}")
            
            with col2:
                # Removed emoji metric due to display issues
                pass
            
            # Top 5 words
            st.markdown("#### " + ("חמש המילים הנפוצות ביותר" if is_hebrew else "Top 5 Words"))
            all_words = []
            for msg in user_data['message']:
                # Remove emojis and special characters, split into words
                clean_msg = re.sub(r'[^\w\s]', '', str(msg))
                words = clean_msg.split()
                # Filter out "media", "omitted" and short words
                filtered_words = [word.lower() for word in words if len(word) > 2 and word.lower() not in ['media', 'omitted']]
                all_words.extend(filtered_words)
            
            if all_words:
                word_counts = Counter(all_words)
                top_words = word_counts.most_common(5)
                
                # Display as a small horizontal bar chart
                fig_top_words = px.bar(
                    x=[count for word, count in top_words],
                    y=[word for word, count in top_words],
                    orientation='h',
                    labels={'x': 'כמות' if is_hebrew else 'Count', 'y': 'מילה' if is_hebrew else 'Word'},
                    color_discrete_sequence=['#667eea']
                )
                fig_top_words.update_layout(height=250, showlegend=False)
                fig_top_words.update_traces(
                    texttemplate='%{x}',
                    textposition='outside'
                )
                st.plotly_chart(fig_top_words, use_container_width=True)
            else:
                st.info("אין מספיק מילים לניתוח" if is_hebrew else "Not enough words for analysis")
        
        # Fun Facts
        st.markdown(f'<div class="section-header">🎭 {fun_facts}</div>', unsafe_allow_html=True)
        fun_facts_list = create_fun_facts(df_filtered, leaderboards)
        
        for fact in fun_facts_list:
            st.markdown(f'<div class="metric-card">{fact}</div>', unsafe_allow_html=True)
        
        # Leaderboards
        st.markdown(f'<div class="section-header">{leaderboard_title}</div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📱 " + messages_leaderboard,
            "😄 " + most_emojis,
            "📝 " + longest_messages,
            "🖼️ " + most_media,
            "😆 " + most_haha
        ])
        
        with tab1:
            most_messages_df = leaderboards['most_messages'].reset_index()
            most_messages_df.columns = ['משתמש' if is_hebrew else 'User', 'הודעות' if is_hebrew else 'Messages']
            most_messages_df['אחוז' if is_hebrew else 'Percentage'] = (most_messages_df['הודעות' if is_hebrew else 'Messages'] / most_messages_df['הודעות' if is_hebrew else 'Messages'].sum() * 100).round(1)
            st.dataframe(most_messages_df, use_container_width=True)
        
        with tab2:
            emoji_df = pd.DataFrame(leaderboards['most_emojis'], columns=['אימוגי' if is_hebrew else 'Emoji', 'כמות' if is_hebrew else 'Count'])
            st.dataframe(emoji_df, use_container_width=True)
        
        with tab3:
            longest_df = leaderboards['longest_messages'][['sender', 'message', 'message_length']].copy()
            longest_df.columns = ['משתמש' if is_hebrew else 'User', 'הודעה' if is_hebrew else 'Message', 'אורך' if is_hebrew else 'Length']
            st.dataframe(longest_df, use_container_width=True)
        
        with tab4:
            media_df = leaderboards['most_media'].reset_index()
            media_df.columns = ['משתמש' if is_hebrew else 'User', 'כמות' if is_hebrew else 'Count']
            st.dataframe(media_df, use_container_width=True)
        
        with tab5:
            haha_df = leaderboards['most_haha'].reset_index()
            haha_df.columns = ['משתמש' if is_hebrew else 'User', 'כמות' if is_hebrew else 'Count']
            st.dataframe(haha_df, use_container_width=True)
        
        # Time breakdowns
        st.markdown(f'<div class="section-header">📊 פילוח לפי זמן</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Weekly breakdown
            weekly_data = breakdowns['weekly']
            fig_weekly = px.bar(
                x=weekly_data.index,
                y=weekly_data.values,
                title=weekly_breakdown,
                labels={'x': 'יום' if is_hebrew else 'Day', 'y': 'הודעות' if is_hebrew else 'Messages'},
                color_discrete_sequence=['#667eea']
            )
            # Add value labels on bars
            fig_weekly.update_traces(
                texttemplate='%{y}',
                textposition='outside'
            )
            fig_weekly.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig_weekly, use_container_width=True)
            
            # Monthly breakdown
            monthly_data = breakdowns['monthly']
            fig_monthly = px.bar(
                x=monthly_data.index,
                y=monthly_data.values,
                title=monthly_breakdown,
                labels={'x': 'יום בחודש' if is_hebrew else 'Day of Month', 'y': 'הודעות' if is_hebrew else 'Messages'},
                color_discrete_sequence=['#f093fb']
            )
            # Add value labels on bars
            fig_monthly.update_traces(
                texttemplate='%{y}',
                textposition='outside'
            )
            fig_monthly.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig_monthly, use_container_width=True)
        
        with col2:
            # Hourly breakdown
            hourly_data = breakdowns['hourly']
            fig_hourly = px.bar(
                x=hourly_data.index,
                y=hourly_data.values,
                title=hourly_breakdown,
                labels={'x': 'שעה' if is_hebrew else 'Hour', 'y': 'הודעות' if is_hebrew else 'Messages'},
                color_discrete_sequence=['#f5576c']
            )
            # Add value labels on bars
            fig_hourly.update_traces(
                texttemplate='%{y}',
                textposition='outside'
            )
            fig_hourly.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig_hourly, use_container_width=True)
            
            # Daily activity over time
            daily_data = df_filtered.groupby(df_filtered['datetime'].dt.date).size()
            fig_daily = px.line(
                x=daily_data.index,
                y=daily_data.values,
                title="פעילות יומית" if is_hebrew else "Daily Activity",
                labels={'x': 'תאריך' if is_hebrew else 'Date', 'y': 'הודעות' if is_hebrew else 'Messages'}
            )
            fig_daily.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig_daily, use_container_width=True)

        # Weekly change percentage chart (last 60 days)
        st.markdown(f'<div class="section-header">📈 אחוז שינוי שבועי (60 ימים אחרונים)</div>', unsafe_allow_html=True)
        
        # Get last 60 days data
        latest_date = df_filtered['datetime'].max()
        sixty_days_ago = latest_date - timedelta(days=60)
        last_sixty_days_data = df_filtered[df_filtered['datetime'] >= sixty_days_ago]
        
        if not last_sixty_days_data.empty:
            # Group by week and calculate percentage change
            weekly_counts = last_sixty_days_data.groupby(last_sixty_days_data['datetime'].dt.isocalendar().week).size()
            
            if len(weekly_counts) > 1:
                # Calculate percentage change
                weekly_changes = []
                week_labels = []
                
                for i in range(1, len(weekly_counts)):
                    current_week = weekly_counts.index[i]
                    prev_week = weekly_counts.index[i-1]
                    
                    current_count = weekly_counts.iloc[i]
                    prev_count = weekly_counts.iloc[i-1]
                    
                    if prev_count > 0:
                        change_percent = ((current_count - prev_count) / prev_count) * 100
                    else:
                        change_percent = 0
                    
                    # Limit extreme values to prevent chart cutoff
                    if change_percent > 500:
                        change_percent = 500
                    elif change_percent < -500:
                        change_percent = -500
                    
                    weekly_changes.append(change_percent)
                    
                    # Create date range label for the week
                    week_start = last_sixty_days_data[last_sixty_days_data['datetime'].dt.isocalendar().week == current_week]['datetime'].min()
                    week_end = last_sixty_days_data[last_sixty_days_data['datetime'].dt.isocalendar().week == current_week]['datetime'].max()
                    
                    if week_start and week_end:
                        start_str = week_start.strftime('%d/%m')
                        end_str = week_end.strftime('%d/%m')
                        week_labels.append(f"{start_str}-{end_str}")
                    else:
                        week_labels.append(f"שבוע {current_week}" if is_hebrew else f"Week {current_week}")
                
                if weekly_changes:
                    # Get the actual message counts for each week
                    week_counts = []
                    for i in range(1, len(weekly_counts)):
                        current_week = weekly_counts.index[i]
                        current_count = weekly_counts.iloc[i]
                        week_counts.append(current_count)
                    
                    # Create single chart with bars and line overlay
                    import plotly.graph_objects as go
                    
                    fig_combined = go.Figure()
                    
                    # Add bars for message counts
                    fig_combined.add_trace(
                        go.Bar(
                            x=week_labels,
                            y=week_counts,
                            name="הודעות" if is_hebrew else "Messages",
                            marker_color='#667eea',
                            text=week_counts,
                            textposition='outside',
                            yaxis='y'
                        )
                    )
                    
                    # Add line for percentage changes on secondary y-axis
                    fig_combined.add_trace(
                        go.Scatter(
                            x=week_labels,
                            y=weekly_changes,
                            name="אחוז שינוי" if is_hebrew else "Change %",
                            mode='lines+markers',
                            line=dict(color='#f093fb', width=3),
                            marker=dict(size=8),
                            text=[f"{p:.1f}%" for p in weekly_changes],
                            textposition='top center',
                            yaxis='y2'
                        )
                    )
                    
                    fig_combined.update_layout(
                        height=400,
                        title="הודעות ואחוז שינוי שבועי" if is_hebrew else "Weekly Messages and Change Percentage",
                        xaxis_title="תאריכים" if is_hebrew else "Dates",
                        yaxis=dict(
                            title="הודעות" if is_hebrew else "Messages",
                            side='left',
                            showgrid=True
                        ),
                        yaxis2=dict(
                            title="אחוז שינוי" if is_hebrew else "Change %",
                            side='right',
                            overlaying='y',
                            showgrid=False
                        ),
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        )
                    )
                    
                    st.plotly_chart(fig_combined, use_container_width=True)
                else:
                    st.info("אין מספיק נתונים לחישוב שינויים שבועיים" if is_hebrew else "Not enough data for weekly changes")
            else:
                st.info("אין מספיק שבועות לניתוח" if is_hebrew else "Not enough weeks for analysis")
        else:
            st.info("אין נתונים ב-60 הימים האחרונים" if is_hebrew else "No data in last 60 days")
        


else:
    st.info(no_file_label) 