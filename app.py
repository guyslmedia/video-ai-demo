
# אפליקציה פשוטה לעריכת וידאו עם AI ב-Streamlit
# שימוש: מעלים וידאו, האפליקציה מחלצת אודיו, מתמללת ומראה טקסט

import streamlit as st
import moviepy.editor as mp
import speech_recognition as sr
import os
import tempfile

st.title("🔥 עורך וידאו אוטומטי מבוסס AI")

# שלב 1: העלאת קובץ וידאו
uploaded_file = st.file_uploader("העלה סרטון (MP4)", type=["mp4"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(uploaded_file.read())
        video_path = temp_video.name

    st.video(video_path)
    st.write("\n🔄 מעבד... זה יכול לקחת קצת זמן...")

    # שלב 2: חילוץ אודיו מהוידאו
    video = mp.VideoFileClip(video_path)
    audio_path = video_path.replace(".mp4", ".wav")
    video.audio.write_audiofile(audio_path)

    # שלב 3: זיהוי קולי
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="he-IL")
            st.success("🎙️ תמלול מזוהה:")
            st.text_area("תוצאה:", text, height=200)
        except sr.UnknownValueError:
            st.error("לא ניתן לזהות דיבור בקובץ")
        except sr.RequestError:
            st.error("שגיאה בשירות זיהוי הדיבור")

    # ניקוי קבצים זמניים
    os.remove(audio_path)
    os.remove(video_path)
