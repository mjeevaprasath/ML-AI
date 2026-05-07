# IMPORT YOUR BIG ML CODE FILE
# example: import your full assistant logic file

# from ml_main import execute_command, execute_smart_command, ask_ai

WEB_MODE = True

def run_ml_command(command):

    command = command.lower()

    # 🔥 STEP 1: LOCAL COMMAND
    if "time" in command:
        import datetime
        return datetime.datetime.now().strftime("%I:%M %p")

    if "hello" in command:
        return "Hello Sir, ML is active"

    # 🔥 STEP 2: AI RESPONSE PLACEHOLDER
    return f"ML received: {command}"