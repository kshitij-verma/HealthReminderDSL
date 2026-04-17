import os
from datetime import datetime, timedelta
from textx import metamodel_from_file
from plyer import notification

def run_dsl():
    if not os.path.exists('health.tx'):
        print("❌ Error: 'health.tx' not found!")
        return

    try:
        meta_model = metamodel_from_file('health.tx')
        
        # FULL SCRIPT: Restored with all your original reminders and the new conflict
        example_script = """
        medication Aspirin
        medication Ibuprofen
        medication VitaminC

        conflict Aspirin with Ibuprofen message "Safety Alert: Avoid mixing different NSAID medications!"

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
        # learn pytest 
        # pyproject.toml (learn toml the standard way for python config)
        # UV tool for project management, for virtual environment
        # webapp for input by the user
        # color code for the user (vs code plugin)
        
        test_minutes = 30 
        for med in model.medications:
            # We simulate taking both Aspirin and Ibuprofen to trigger the new conflict logic
            if med.name in ["Aspirin", "Ibuprofen"]:
                med.last_taken = datetime.now() - timedelta(minutes=test_minutes)
                print(f"🕒 System Memory: {med.name} taken {test_minutes} mins ago.")

        # 2. THE CONFLICT CHECKER (The "Relational Logic" Upgrade)
        print("\n--- Checking Medication Conflicts ---")
        for c in model.conflicts:
            # Check if both medications in the conflict pair have a recorded time
            if hasattr(c.medA, 'last_taken') and hasattr(c.medB, 'last_taken'):
                print(f"🚨 CONFLICT DETECTED: {c.medA.name} + {c.medB.name}")
                notification.notify(
                    title="⚠️ MEDICATION CONFLICT",
                    message=c.message,
                    app_name="HealthReminderDSL",
                    timeout=15
                )

        # 3. THE CHECK LOOP & NOTIFICATION TRIGGER
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
                    notification.notify(
                        title=f"Health Reminder: {r.name}",
                        message=r.message,
                        app_name="HealthReminderDSL",
                        timeout=10
                    )
            else:
                # No dependency (Posture, Hydration, Stretch)? Just send it!
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