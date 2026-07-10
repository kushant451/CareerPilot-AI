"""Small reusable presentation helpers shared across pages (SVG rings, badges, score math)."""
import streamlit as st

def svg_ring(value, max_val, size=100, color="#E8896A", sub=""):
    pct   = (value / max_val) if max_val else 0
    r     = size * 0.42
    circ  = 2 * 3.14159 * r
    dash  = pct * circ
    cx = cy = size / 2
    fs = size * 0.22
    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#F0DDD0" stroke-width="{size*.08}"/>
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}"
              stroke-width="{size*.08}" stroke-dasharray="{dash:.1f} {circ:.1f}"
              stroke-linecap="round" transform="rotate(-90 {cx} {cy})"/>
      <text x="{cx}" y="{cy-.04*size}" text-anchor="middle" dominant-baseline="central"
            fill="{color}" font-size="{fs}" font-weight="700"
            font-family="Segoe UI,sans-serif">{value}</text>
      <text x="{cx}" y="{cy+size*.2}" text-anchor="middle" fill="#9C7A6B"
            font-size="{size*.1}" font-family="Segoe UI,sans-serif">{sub}</text>
    </svg>"""


def avg_score():
    evals  = st.session_state.get("evaluations", {})
    scores = [v["score"] for v in evals.values()
              if isinstance(v, dict) and "score" in v]
    return round(sum(scores) / len(scores), 1) if scores else 0.0


def diff_badge(difficulty):
    cls = {"Easy":"b-green","Medium":"b-yellow","Hard":"b-red"}.get(difficulty,"b-accent")
    return f'<span class="{cls}">{difficulty}</span>'
