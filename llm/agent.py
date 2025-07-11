import re
from database.db_manager import save_reminder

# If user says "Remind me to pray at 8:00 AM"
if "remind me to" in message_lower:
    match = re.search(r'remind me to (.+?) at (\d{1,2}:\d{2}\s*[ap]m)', message_lower)
    if match:
        task = match.group(1).strip().capitalize()
        time = match.group(2).upper()
        save_reminder(user_id, task, time)
        return ChatResponse(response=f"✅ Got it! I’ll remind you to **{task}** at **{time}** every day.", session_id=session_id)
    else:
        return ChatResponse(response="❌ Sorry, I couldn’t understand the time format. Try saying: 'Remind me to pray at 8:00 AM'", session_id=session_id)
