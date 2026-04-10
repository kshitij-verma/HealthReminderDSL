import os
from datetime import datetime, timedelta
from textx import metamodel_from_file
from plyer import notification  # Handles the OS popup

def run_dsl():
    if not os.path.exists('health.tx'):
        print("❌ Error: 'health.tx' not found!")
        return

    try:
        meta_model = metamodel_from_file('health.tx')
        
        example_script = """
        medication Aspirin
        medication VitaminC

        reminder "Vitamin C" {
            every: 720 min
            after: Aspirin
            message: "Safe to take Vitamin C now."
        }

        reminder "Posture Check" {
            every: 10 min
            message: "Sit up straight and roll your shoulders!"
        }

        reminder "Hydration" {
            every: 60 min
            message: "Drink a full glass of water."
        }

        reminder "Stretch Break" {
            every: 60 min
            message: "Stand up and reach for the ceiling for 30 seconds."
        }
        """

        model = meta_model.model_from_str(example_script)

        # 1. STATE SIMULATION
        # To test the 'Success' popup!
        # learn pytest 
        # pyproject.toml (learn toml the standard way for python config)
        # UV tool for project management, for virtual environment (local environment that has all envornoments installed)
        # webapp for input by the user
        # color code for the user (vs code plugin)
        test_minutes = 30 
        for med in model.medications:
            if med.name == "Aspirin":
                med.last_taken = datetime.now() - timedelta(minutes=test_minutes)
                print(f"🕒 System Memory: {med.name} taken {test_minutes} mins ago.")

        # 2. THE CHECK LOOP & NOTIFICATION TRIGGER
        for r in model.reminders:
            print(f"\n--- Checking: {r.name} ---")
            
            dep_med = getattr(r, 'dependency', None)
            
            if dep_med and hasattr(dep_med, 'last_taken'):
                time_passed = datetime.now() - dep_med.last_taken
                minutes_passed = time_passed.total_seconds() / 60
                
                if minutes_passed < 60:
                    print(f"🚫 BLOCKED: Wait 60m after {dep_med.name}.")
                else:
                    print(f"✅ CLEAR: Requirements met.")
                    # --- TRIGGER WINDOWS NOTIFICATION ---
                    notification.notify(
                        title=f"Health Reminder: {r.name}",
                        message=r.message,
                        app_name="HealthReminderDSL",
                        timeout=10
                    )
            else:
                # No dependency? Just send the notification immediately
                print(f"✅ CLEAR: No dependencies.")
                notification.notify(
                    title=f"Health Reminder: {r.name}",
                    message=r.message,
                    app_name="HealthReminderDSL",
                    timeout=10
                )

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_dsl()