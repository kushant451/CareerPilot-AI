"""Global CSS injected once per app run."""
import streamlit as st

def load_css():
    st.markdown("""
<style>
#MainMenu, footer, header {display:none !important}
.block-container {padding:1.5rem 2rem !important; max-width:1100px}
.stApp {background:#FFF6F0}
section[data-testid="stSidebar"] {background:#FFFFFF; border-right:1px solid #F0DDD0; box-shadow:2px 0 12px rgba(232,137,106,.06)}

.ai-card {background:#FFFFFF; border:1px solid #F3E1D3; border-radius:16px; padding:20px; margin-bottom:16px; box-shadow:0 2px 10px rgba(232,137,106,.08)}
.ai-card-flat {background:#FDEAE0; border:1px solid #F3E1D3; border-radius:12px; padding:16px; margin-bottom:12px}

.b-green  {background:rgba(16,185,129,.12);  color:#10B981; padding:3px 10px; border-radius:999px; font-size:13px; font-weight:500; display:inline-block}
.b-red    {background:rgba(239,68,68,.12);   color:#EF4444; padding:3px 10px; border-radius:999px; font-size:13px; font-weight:500; display:inline-block}
.b-yellow {background:rgba(245,158,11,.12);  color:#F59E0B; padding:3px 10px; border-radius:999px; font-size:13px; font-weight:500; display:inline-block}
.b-accent {background:rgba(232,137,106,.15);  color:#E8896A; padding:3px 10px; border-radius:999px; font-size:13px; font-weight:500; display:inline-block}
.b-cyan   {background:rgba(6,182,212,.12);   color:#06B6D4; padding:3px 10px; border-radius:999px; font-size:13px; font-weight:500; display:inline-block}

.tag {display:inline-block; background:rgba(232,137,106,.15); color:#E8896A; padding:4px 12px;
      border-radius:999px; font-size:13.5px; margin:3px; border:1px solid rgba(232,137,106,.2)}

.prog-bar    {height:6px; border-radius:3px; background:#FDEAE0; overflow:hidden; margin:4px 0}
.prog-fill   {height:100%; border-radius:3px; background:#E8896A}
.p-green     {background:#10B981}
.p-yellow    {background:#F59E0B}
.p-red       {background:#EF4444}

.waveform {display:flex; align-items:center; gap:3px; height:32px; margin:10px 0}
.waveform span {width:3px; border-radius:2px; background:#E8896A; animation:wv 1.2s ease-in-out infinite}
.waveform span:nth-child(2){animation-delay:.1s} .waveform span:nth-child(3){animation-delay:.2s}
.waveform span:nth-child(4){animation-delay:.3s} .waveform span:nth-child(5){animation-delay:.4s}
.waveform span:nth-child(6){animation-delay:.5s} .waveform span:nth-child(7){animation-delay:.6s}
.waveform span:nth-child(8){animation-delay:.7s} .waveform span:nth-child(9){animation-delay:.3s}
.waveform span:nth-child(10){animation-delay:.15s} .waveform span:nth-child(11){animation-delay:.55s}
.waveform span:nth-child(12){animation-delay:.25s}
@keyframes wv {0%,100%{height:10%} 50%{height:100%}}

.stButton>button {
    border:none !important; border-radius:8px !important; font-weight:500 !important
}
button[kind="primary"], button[kind="primaryFormSubmit"] {
    background:#E8896A !important; color:#fff !important;
}
button[kind="primary"]:hover {background:#F0A184 !important}
button[kind="secondary"] {
    background:transparent !important; color:#6B5248 !important;
    text-align:left !important; justify-content:flex-start !important;
    padding-left:14px !important; font-weight:500 !important;
}
button[kind="secondary"]:hover {background:#FDEAE0 !important; color:#3A2E2A !important}
section[data-testid="stSidebar"] button[kind="primary"] {
    box-shadow:0 2px 8px rgba(232,137,106,.35) !important;
}
.stTextArea>div>textarea {
    background:#FDEAE0 !important; border:1px solid #E8C7AE !important;
    color:#3A2E2A !important; border-radius:8px !important
}
.stSelectbox>div>div {
    background:#FDEAE0 !important; border:1px solid #E8C7AE !important; color:#3A2E2A !important
}
.stFileUploader>div {background:#FDEAE0 !important; border:1px solid #E8C7AE !important; border-radius:8px !important}
label {color:#9C7A6B !important; font-size:13.5px !important}
.stDownloadButton>button {
    background:#FDEAE0 !important; border:1px solid #E8C7AE !important;
    color:#3A2E2A !important; border-radius:8px !important
}
.stAlert {border-radius:8px !important}
div[data-testid="stDecoration"] {display:none}
.stDeployButton {display:none}
[data-testid="stMarkdownContainer"]:empty {display:none !important}
[data-testid="element-container"]:empty {display:none !important}
.ai-card:empty {display:none !important}
</style>
""", unsafe_allow_html=True)
