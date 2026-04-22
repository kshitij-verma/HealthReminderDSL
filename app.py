import streamlit as st
from code_editor import code_editor
from textx import metamodel_from_file
from plyer import notification
from datetime import datetime, timedelta

# Page config
st.set_page_config(page_title="HealthReminder DSL", page_icon="🏥", layout="wide")

st.title("🏥 HealthReminder DSL Interpreter")
st.markdown("""
Write your DSL code below. The **Conflict** logic is now dynamic based on the 'within' time you define.
""")

# Sidebar settings
st.sidebar.header("⚙️ Simulation Settings")
test_mins = st.sidebar.slider("Minutes since last medication:", 0, 120, 30)
st.sidebar.info(f"Simulating: Medications taken {test_mins} mins ago.")

# --- DYNAMIC EXAMPLE SCRIPT ---
# We now define the safety window (60 min) directly in the DSL code.
default_code = """medication Aspirin
medication VitaminC

conflict Aspirin with VitaminC within 60 min message "Precaution: Space these out to avoid stomach irritation."

reminder "Morning Aspirin" {
    every: 1440 min
    message: "Take your heart-health Aspirin dose."
}

reminder "Hydration Guard" {
    every: 60 min
    after: Aspirin
    message: "Drink water (Aspirin was taken recently)."
}"""

# Editor Config
buttons = [{"name": "Run", "feather": "Play", "primary": True, "alwaysOn": True, "commands": ["submit"]}]

st.subheader("📝 DSL Editor")
response = code_editor(
    default_code, 
    lang="python", 
    theme="github_dark", 
    buttons=buttons, 
    height=[15, 30], 
    key="dsl_dynamic_v2"
)

dsl_code = response.get('text', "")
run_clicked = st.button("🚀 Execute Global Sync") or (response.get('type') == "submit")

if run_clicked:
    if not dsl_code or len(dsl_code.strip()) < 5:
        st.warning("Please enter your DSL code above.")
    else:
        try:
            # Load Meta-model and generate Model
            meta_model = metamodel_from_file('health.tx')
            model = meta_model.model_from_str(dsl_code)
            st.success("✅ DSL Logic Validated!")

            # 1. Simulate State
            # We assign a 'last_taken' timestamp to all medications in the model
            for med in model.medications:
                med.last_taken = datetime.now() - timedelta(minutes=test_mins)
            
            # 2. DYNAMIC CONFLICT CHECK
            st.divider()
            st.subheader("🛡️ Safety Check")
            conflict_found = False
            
            for c in model.conflicts:
                # DYNAMIC LOGIC: We compare the simulation slider (test_mins)
                # against the specific time defined in the DSL script (c.time)
                if test_mins < c.time:
                    st.error(f"🚨 CONFLICT: {c.medA.name} + {c.medB.name}")
                    st.info(f"**Condition:** Less than {c.time} minutes elapsed.")
                    st.warning(f"**Rule Message:** {c.message}")
                    notification.notify(title="DSL Conflict", message=c.message)
                    conflict_found = True
            
            if not conflict_found:
                st.success(f"✅ State Safe: Time elapsed ({test_mins}m) exceeds all defined safety windows.")

            # 3. Check Reminders
            st.divider()
            st.subheader("🔔 Active Reminders")
            for r in model.reminders:
                st.write(f"Verifying: **{r.name}**")
                st.toast(f"Notification triggered: {r.name}")
                notification.notify(title=f"Health Reminder: {r.name}", message=r.message)
                
        except Exception as e:
            st.error(f"❌ Parser Error: {e}")
