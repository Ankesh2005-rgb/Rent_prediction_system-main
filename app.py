# app.py

import os
import joblib
import gradio as gr

# ==========================================================
# Load the trained model
# ==========================================================
try:
    deployed_lr = joblib.load("my_first_ml_model.pkl")
except Exception as e:
    print(f"Warning: Model not found or error loading. {e}")
    deployed_lr = None

# ==========================================================
# Prediction Function with Error Handling
# ==========================================================
def predict_rent(size_of_prop):

    def card(title, sub, tag, css_class, meta=""):
        meta_html = f'<div class="result-meta">{meta}</div>' if meta else ""
        return f"""
        <div class="result-card {css_class}">
            <div class="corner corner-tl"></div>
            <div class="corner corner-tr"></div>
            <div class="corner corner-bl"></div>
            <div class="corner corner-br"></div>
            <div class="result-tag">{tag}</div>
            <div class="result-title">{title}</div>
            <div class="result-sub">{sub}</div>
            {meta_html}
        </div>
        """

    # 1. Empty input check
    if size_of_prop is None or str(size_of_prop).strip() == "":
        return card("Enter a size to continue", "The size field is empty.", "INPUT REQUIRED", "error-card")

    # 2. Type casting
    try:
        size_of_prop = float(size_of_prop)
    except (ValueError, TypeError):
        return card("Not a valid number", "Enter the size using digits only.", "INPUT ERROR", "error-card")

    # 3. Range validation
    if size_of_prop <= 0:
        return card("Size must be positive", "Property size must be greater than 0.", "INPUT ERROR", "error-card")

    if size_of_prop > 100000:
        return card("Size looks too large", "Double-check the value you entered.", "INPUT ERROR", "error-card")

    # 4. Model check
    if deployed_lr is None:
        return card("Model unavailable", "The .pkl model file could not be loaded.", "SYSTEM ERROR", "error-card")

    # 5. Prediction
    try:
        prediction = deployed_lr.predict([[size_of_prop]])
        rent_value = prediction[0]

        return f"""
        <div class="result-card rent-card">
            <div class="corner corner-tl"></div>
            <div class="corner corner-tr"></div>
            <div class="corner corner-bl"></div>
            <div class="corner corner-br"></div>
            <div class="result-tag">ESTIMATE — MODEL v1</div>
            <div class="rent-figure">₹{rent_value:,.0f}<span class="rent-unit">/mo</span></div>
            <div class="rent-divider"></div>
            <div class="result-meta">{size_of_prop:,.0f} sq&nbsp;ft &nbsp;·&nbsp; ₹{(rent_value/size_of_prop):.2f} per sq&nbsp;ft</div>
        </div>
        """
    except Exception as e:
        return card("Prediction failed", str(e), "SYSTEM ERROR", "error-card")


def reset_form():
    return [None, PLACEHOLDER_RESULT]


# ==========================================================
# Copy
# ==========================================================
PLACEHOLDER_RESULT = """
<div class="result-card idle-card">
    <div class="corner corner-tl"></div>
    <div class="corner corner-tr"></div>
    <div class="corner corner-bl"></div>
    <div class="corner corner-br"></div>
    <div class="result-tag">READY</div>
    <div class="result-title">No estimate yet</div>
    <div class="result-sub">Enter a floor area and run the estimate.</div>
</div>
"""

# ==========================================================
# Custom Styling — architectural / drafting-table inspired
# Type: Fraunces (display) + Inter (body/UI) + IBM Plex Mono (data)
# Palette: paper #F6F4EF · ink #1C2B39 · blueprint #2F5D82 ·
#          brass #A8752C · mist #E4E0D6 · rose #B54B4B
# Signature: drafting corner-bracket marks framing the result panel,
#            like dimension marks on a floor plan.
# ==========================================================
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,560;9..144,680&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root {
    --paper: #F6F4EF;
    --ink: #1C2B39;
    --ink-soft: #55677A;
    --blueprint: #2F5D82;
    --brass: #A8752C;
    --mist: #E4E0D6;
    --rose: #B54B4B;
}

.gradio-container {
    max-width: 720px !important;
    margin: auto !important;
    font-family: 'Inter', sans-serif !important;
    background:
        linear-gradient(var(--paper), var(--paper)),
        repeating-linear-gradient(0deg, rgba(47,93,130,0.05) 0 1px, transparent 1px 28px),
        repeating-linear-gradient(90deg, rgba(47,93,130,0.05) 0 1px, transparent 1px 28px);
    background-blend-mode: normal;
}

body, .dark .gradio-container { color: var(--ink) !important; }

/* ---------- Header ---------- */
#header-banner {
    padding: 34px 8px 18px 8px;
    text-align: left;
    border-bottom: 1px solid var(--mist);
    margin-bottom: 22px;
}
#header-banner .eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--blueprint);
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
}
#header-banner .eyebrow .rule {
    flex: 0 0 34px;
    height: 1px;
    background: var(--brass);
}
#header-banner h1 {
    font-family: 'Fraunces', serif;
    font-weight: 560;
    font-size: 2.3rem;
    letter-spacing: -0.01em;
    color: var(--ink);
    margin: 0 0 8px 0;
    line-height: 1.08;
}
#header-banner p {
    font-size: 0.98rem;
    color: var(--ink-soft);
    max-width: 46ch;
    margin: 0;
}

/* ---------- Section labels ---------- */
.section-title {
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 500 !important;
    font-size: 0.74rem !important;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--blueprint) !important;
    margin-bottom: 2px !important;
}

.gr-group, .gradio-container .form {
    background: #FFFFFE !important;
    border: 1px solid var(--mist) !important;
    border-radius: 4px !important;
    box-shadow: none !important;
}

label span, .gradio-container label {
    font-family: 'Inter', sans-serif !important;
    color: var(--ink) !important;
    font-weight: 500 !important;
}

input, textarea {
    font-family: 'IBM Plex Mono', monospace !important;
    border-radius: 3px !important;
}

/* ---------- Buttons ---------- */
#predict-btn {
    background: var(--brass) !important;
    border: 1px solid var(--brass) !important;
    color: #FFF9F0 !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em;
    border-radius: 3px !important;
}
#predict-btn:hover { background: #93641f !important; }

#reset-btn {
    background: transparent !important;
    border: 1px solid var(--mist) !important;
    color: var(--ink-soft) !important;
    border-radius: 3px !important;
}
#reset-btn:hover { border-color: var(--blueprint) !important; color: var(--blueprint) !important; }

/* ---------- Result panel ---------- */
#result-box { min-height: 180px; display: flex; align-items: center; justify-content: center; padding: 6px 0; }

.result-card {
    position: relative;
    width: 100%;
    padding: 30px 26px;
    text-align: center;
    background: #FFFFFE;
    border: 1px solid var(--mist);
    border-radius: 4px;
    animation: fade-in 0.35s ease;
}
@keyframes fade-in { from { opacity: 0; transform: translateY(4px);} to { opacity: 1; transform: translateY(0);} }

.corner { position: absolute; width: 14px; height: 14px; border: 2px solid var(--brass); opacity: 0.85; }
.corner-tl { top: -1px; left: -1px; border-right: none; border-bottom: none; }
.corner-tr { top: -1px; right: -1px; border-left: none; border-bottom: none; }
.corner-bl { bottom: -1px; left: -1px; border-right: none; border-top: none; }
.corner-br { bottom: -1px; right: -1px; border-left: none; border-top: none; }

.result-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--blueprint);
    margin-bottom: 12px;
}

.rent-figure {
    font-family: 'Fraunces', serif;
    font-weight: 680;
    font-size: 3rem;
    color: var(--ink);
    line-height: 1;
}
.rent-unit {
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    color: var(--ink-soft);
    font-weight: 500;
    margin-left: 4px;
}
.rent-divider {
    width: 40px;
    height: 2px;
    background: var(--brass);
    margin: 16px auto;
}

.idle-card .result-tag { color: var(--ink-soft); }
.idle-card .corner { border-color: var(--mist); }
.idle-card .result-title { font-family: 'Fraunces', serif; font-size: 1.3rem; color: var(--ink-soft); margin-bottom: 4px; }
.idle-card .result-sub { color: var(--ink-soft); font-size: 0.92rem; }

.error-card .corner { border-color: var(--rose); }
.error-card .result-tag { color: var(--rose); }
.error-card .result-title { font-family: 'Fraunces', serif; font-size: 1.3rem; color: var(--ink); margin-bottom: 4px; }
.error-card .result-sub { color: var(--ink-soft); font-size: 0.92rem; }

.result-meta {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    color: var(--ink-soft);
}

/* ---------- Footer ---------- */
.footer-block {
    border-top: 1px solid var(--mist);
    margin-top: 26px;
    padding-top: 18px;
}
.footer-block table { font-family: 'IBM Plex Mono', monospace !important; font-size: 0.85rem !important; }
"""

# ==========================================================
# Interface Setup
# ==========================================================
theme = gr.themes.Soft(
    primary_hue="orange",
    secondary_hue="blue",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Inter"), "sans-serif"],
    font_mono=[gr.themes.GoogleFont("IBM Plex Mono"), "monospace"],
)

with gr.Blocks(theme=theme, css=CUSTOM_CSS, title="Property Rent Predictor") as interface:

    gr.HTML(
        """
        <div id="header-banner">
            <div class="eyebrow"><span class="rule"></span>MODEL-BASED ESTIMATE</div>
            <h1>Property Rent Predictor</h1>
            <p>Enter the floor area of a property and get an instant rent
            estimate from a trained Linear Regression model.</p>
        </div>
        """
    )

    with gr.Group():
        gr.Markdown("FLOOR AREA", elem_classes="section-title")
        size_of_prop = gr.Number(
            label="Size of property (sq. ft.)",
            minimum=0,
            info="Total built-up area of the property",
        )
        with gr.Row():
            clear_btn = gr.Button("Reset", variant="secondary", elem_id="reset-btn")
            predict_btn = gr.Button("Estimate rent →", variant="primary", elem_id="predict-btn")

    output_box = gr.HTML(value=PLACEHOLDER_RESULT, elem_id="result-box")

    predict_btn.click(fn=predict_rent, inputs=size_of_prop, outputs=output_box)
    clear_btn.click(fn=reset_form, inputs=None, outputs=[size_of_prop, output_box])

    gr.Examples(
        examples=[[500], [850], [1200], [2000]],
        inputs=size_of_prop,
        label="Sample sizes (sq. ft.)",
    )

    gr.HTML(
        """
        <div class="footer-block">
        <table style="width:100%; border-collapse:collapse;">
        <tr><td style="padding:3px 0; color:#55677A;">Model</td><td style="padding:3px 0;">Linear Regression · scikit-learn</td></tr>
        <tr><td style="padding:3px 0; color:#55677A;">Interface</td><td style="padding:3px 0;">Gradio</td></tr>
        <tr><td style="padding:3px 0; color:#55677A;">Deployment</td><td style="padding:3px 0;">Render</td></tr>
        </table>
        </div>
        """
    )

# ==========================================================
# Launch
# ==========================================================
if __name__ == "__main__":
    interface.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
    )
