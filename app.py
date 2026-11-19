import streamlit as st
import swisseph as swe
from datetime import datetime
import os

# ============ 1. CONFIG & REVENUE SETTINGS ============
st.set_page_config(page_title="JyotishAI - Free Kundli", page_icon="🪐", layout="wide")

# --- YOUR REVENUE KEYS (Fill later, app works without them) ---
# Get Free Groq Key from console.groq.com
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")
# Get AdSense Publisher ID after approval - e.g. ca-pub-123456
ADSENSE_ID = "ca-pub-XXXXXXXXXXXXXX"  # Replace after AdSense approval
# Your UPI for Paid PDF - e.g. yourname@okhdfc
UPI_ID = "jyotishai@upi"

# ============ 2. LANGUAGE SYSTEM - EN / HI / BN ============
LANG = st.sidebar.selectbox("Language / भाषा / ভাষা", ["English", "हिंदी", "বাংলা"])

T = {
"English": {"title":"🪐 JyotishAI - Vedic + Western + KP + Numerology","sub":"Free For Everyone | For Guidance Only","name":"Your Name","dob":"Date of Birth","tob":"Time of Birth","place":"Birth Place","btn":"Generate Complete Kundli","vedic":"1. VEDIC (Lahiri)","western":"2. WESTERN (Tropical)","kp":"3. KP SYSTEM","num":"4. NUMEROLOGY","ask":"Ask JyotishAI - Career, Marriage, Money, Health","free_q":"You have 3 Free Questions Today","premium":"🔓 Unlock Unlimited Chat + 20 Page PDF Report - Rs 99","pdf":"📄 Download Detailed PDF Report (Rs 199)","disclaimer":"Disclaimer: For guidance & entertainment only. Not medical/legal advice."},
"हिंदी": {"title":"🪐 ज्योतिषAI - वैदिक + पश्चिमी + केपी + अंकशास्त्र","sub":"सबके लिए मुफ्त | केवल मार्गदर्शन के लिए","name":"आपका नाम","dob":"जन्म तिथि","tob":"जन्म समय","place":"जन्म स्थान","btn":"पूरी कुंडली बनाएं","vedic":"1. वैदिक (लाहिरी)","western":"2. पश्चिमी (ट्रॉपिकल)","kp":"3. केपी सिस्टम","num":"4. अंकशास्त्र","ask":"ज्योतिषAI से पूछें - करियर, विवाह, पैसा, स्वास्थ्य","free_q":"आज आपके पास 3 मुफ्त प्रश्न हैं","premium":"🔓 अनलिमिटेड चैट + 20 पेज PDF रिपोर्ट - Rs 99","pdf":"📄 विस्तृत PDF रिपोर्ट डाउनलोड करें (Rs 199)","disclaimer":"अस्वीकरण: केवल मार्गदर्शन के लिए। चिकित्सा / कानूनी सलाह नहीं।"},
"বাংলা": {"title":"🪐 জ্যোতিষAI - বৈদিক + পাশ্চাত্য + কেপি + সংখ্যাতত্ত্ব","sub":"সবার জন্য বিনামূল্যে | শুধুমাত্র নির্দেশনার জন্য","name":"আপনার নাম","dob":"জন্ম তারিখ","tob":"জন্ম সময়","place":"জন্মস্থান","btn":"সম্পূর্ণ কুণ্ডলী তৈরি করুন","vedic":"1. বৈদিক (লাহিড়ী)","western":"2. পাশ্চাত্য (ট্রপিক্যাল)","kp":"3. কেপি সিস্টেম","num":"4. সংখ্যাতত্ত্ব","ask":"জ্যোতিষAI কে জিজ্ঞাসা করুন - ক্যারিয়ার, বিবাহ, টাকা, স্বাস্থ্য","free_q":"আজ আপনার 3টি বিনামূল্যে প্রশ্ন আছে","premium":"🔓 আনলিমিটেড চ্যাট + 20 পৃষ্ঠার PDF রিপোর্ট - Rs 99","pdf":"📄 বিস্তারিত PDF রিপোর্ট ডাউনলোড করুন (Rs 199)","disclaimer":"দাবিত্যাগ: শুধুমাত্র নির্দেশনা ও বিনোদনের জন্য। চিকিৎসা / আইনি পরামর্শ নয়।"}
}[LANG]

# ============ 3. AD SLOT (Revenue) ============
# This box shows after AdSense approval. Before approval, it shows Affiliate link.
st.markdown(f"""<div style='background:#FFF3CD;padding:10px;text-align:center;border-radius:10px'>📢 Advertisement - Your AdSense Banner Will Appear Here | <a href='https://amzn.to/3xxxx'>Buy Original Rudraksha (Affiliate)</a></div>""", unsafe_allow_html=True)

st.title(T["title"])
st.caption(T["sub"] + " | " + T["disclaimer"])

# ============ 4. INPUT ============
c1,c2,c3 = st.columns(3)
with c1:
    name = st.text_input(T["name"], "Pradip")
    dob = st.date_input(T["dob"], datetime(1990,1,1))
with c2:
    tob = st.time_input(T["tob"], datetime.now().time())
    place = st.text_input(T["place"], "Kolkata, India")
with c3:
    lat = st.number_input("Latitude", value=22.57)
    lon = st.number_input("Longitude", value=88.36)
    tz = st.number_input("Timezone (5.5 = India)", value=5.5)

# ============ 5. CALCULATION ENGINE ============
if st.button(T["btn"], type="primary"):
    dt = datetime.combine(dob, tob)
    jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60 - tz)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    ayan = swe.get_ayanamsa_ut(jd)
    signs = ["Mesha","Vrishabha","Mithuna","Karka","Simha","Kanya","Tula","Vrischika","Dhanu","Makara","Kumbha","Meena"]
    nak = ["Ashwini","Bharani","Krittika","Rohini","Mrigashira","Ardra","Punarvasu","Pushya","Ashlesha","Magha","Purva Phalguni","Uttara Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha","Jyeshtha","Mula","Purva Ashadha","Uttara Ashadha","Shravana","Dhanishta","Shatabhisha","Purva Bhadrapada","Uttara Bhadrapada","Revati"]
    def pos(d): return f"{signs[int(d//30)]} {int(d%30)}° {int((d%1)*60)}' | {nak[int(d//13.3333)]}"
    
    planets={}
    for p,pn in [(swe.SUN,"Sun"),(swe.MOON,"Moon"),(swe.MARS,"Mars"),(swe.MERCURY,"Mercury"),(swe.JUPITER,"Jupiter"),(swe.VENUS,"Venus"),(swe.SATURN,"Saturn"),(swe.MEAN_NODE,"Rahu")]:
        xx,_ = swe.calc_ut(jd, p); planets[pn]=(xx[0]-ayan)%360
    planets["Ketu"]=(planets["Rahu"]+180)%360
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P')
    lagna=(ascmc[0]-ayan)%360
    st.session_state['chart']=f"Lagna: {pos(lagna)}, Moon: {pos(planets['Moon'])}, Sun: {pos(planets['Sun'])}, Saturn: {pos(planets['Saturn'])}, Jupiter: {pos(planets['Jupiter'])}, Rahu: {pos(planets['Rahu'])}"
    st.session_state['lagna']=lagna; st.session_state['planets']=planets

    st.subheader(T["vedic"])
    st.write(f"**Lagna:** {pos(lagna)}")
    for k,v in planets.items(): st.write(f"**{k}:** {pos(v)}")
    st.write("**Dasha System:** Vimshottari - Based on Moon Nakshatra. **Sade Sati:** Check Saturn transit over Moon sign.")
    
    st.subheader(T["western"])
    st.write(f"**Sun:** {signs[int((planets['Sun']+ayan)//30)%12]} | **Moon:** {signs[int((planets['Moon']+ayan)//30)%12]} | **Rising:** {signs[int((lagna+ayan)//30)%12]}")
    
    st.subheader(T["kp"])
    swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)
    st.write(f"KP Ayanamsa: {swe.get_ayanamsa_ut(jd):.2f}° | Rule: Cuspal Sub-Lord decides result. 10th CSL in 2,6,10,11 = Job")
    
    st.subheader(T["num"])
    d,m,y=dob.day,dob.month,dob.year
    def red(n):
        while n>9: n=sum(map(int,str(n)))
        return n
    mulank=red(d); bhagyank=red(d+m+y)
    st.write(f"**Mulank:** {mulank} | **Bhagyank:** {bhagyank} | **Personal Year:** {red(d+m+2026)} | **Lucky Colour:** {['Red','Orange','Yellow','Green','Blue'][mulank%5]}")
    st.success("✅ Kundli Generated. Now ask below.")

# ============ 6. AI CHAT + REVENUE GATE ============
st.subheader("💬 " + T["ask"])
st.info(T["free_q"])
if 'qcount' not in st.session_state: st.session_state.qcount=0

q = st.text_input("Your Question", key="qbox")
if st.button("Ask"):
    if st.session_state.qcount >= 3:
        st.warning(T["premium"])
        st.markdown(f"**Pay Rs 99 via UPI:** `{UPI_ID}` - Send screenshot on WhatsApp to unlock. Or Buy PDF below.")
        st.button(T["pdf"])
    elif 'chart' not in st.session_state:
        st.error("Please generate Kundli first.")
    else:
        st.session_state.qcount+=1
        # --- AI PROMPT (Works with Groq Free API) ---
        system_prompt = f"""You are JyotishAI, expert in Vedic, Western, KP, Numerology. Language: {LANG}. Use ONLY this chart: {st.session_state['chart']}. Never invent planets. Structure: 1) What chart shows, 2) Answer to: {q}, 3) 3 Practical Remedies: Mantra, Daan/Behaviour, Best Muhurat Date. Never predict death/divorce. Add: For guidance only."""
        st.info(f"System Prompt Ready for AI: {system_prompt[:200]}... Connect Groq API Key in Secrets to get live answer.")
        # To go live: import groq client and call here.
        st.write("**Sample Logic:** Your Moon sign + Saturn position shows current Sade Sati / Dasha effect. Remedy will be shown based on that.")

# ============ 7. BOTTOM AD (Revenue) ============
st.markdown(f"""<div style='background:#E8F5E9;padding:10px;text-align:center;border-radius:10px'>📢 Advertisement Slot 2 - AdSense / Affiliate | {T['disclaimer']}</div>""", unsafe_allow_html=True)
