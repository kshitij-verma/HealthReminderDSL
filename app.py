import streamlit as st
from textx import metamodel_from_file
from plyer import notification
from datetime import datetime, timedelta

# Page config
st.set_page_config(page_title="HealthReminder DSL", page_icon="🏥")

st.title("🏥 HealthReminder DSL Interpreter")
st.markdown("""
Write your DSL code below and hit **Run Interpreter**. 
The system will validate your logic and trigger Windows notifications.
""")

# Sidebar for simulation settings
st.sidebar.header("Simulation Settings")
test_mins = st.sidebar.slider("Minutes since last medication:", 0, 120, 30)

# Default DSL code for the text area
default_code = """medication Aspirin
medication Ibuprofen

conflict Aspirin with Ibuprofen message "Safety Alert: Mixing NSAIDs!"

reminder "Posture" {
    every: 30 min
    message: "Sit up straight!"
}"""

dsl_code = st.text_area("Your DSL Script:", default_code, height=300)

if st.button("🚀 Run Interpreter"):
    try:
        # Load Meta-model
        meta_model = metamodel_from_file('health.tx')
        model = meta_model.model_from_str(dsl_code)
        
        st.success("✅ Syntax Correct! Running logic...")

        # 1. Simulate State
        for med in model.medications:
            med.last_taken = datetime.now() - timedelta(minutes=test_mins)
        
        # 2. Check Conflicts
        st.subheader("Safety Check")
        conflict_found = False
        for c in model.conflicts:
            if hasattr(c.medA, 'last_taken') and hasattr(c.medB, 'last_taken'):
                st.error(f"🚨 CONFLICT: {c.medA.name} + {c.medB.name}")
                st.info(f"Message: {c.message}")
                notification.notify(title="DSL Conflict", message=c.message)
                conflict_found = True
        
        if not conflict_found:
            st.write("No safety conflicts detected.")

        # 3. Check Reminders
        st.subheader("Active Reminders")
        for r in model.reminders:
            st.write(f"🔔 Checking: **{r.name}**")
            # For the demo, we'll just trigger them
            notification.notify(title=f"DSL: {r.name}", message=r.message)
            
    except Exception as e:
        st.error(f"❌ Error: {e}")