import sys
import os
from twilio.rest import Client

# Force Python to recognize the current directory folders correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ABSOLUTE PLACEHOLDERS: Do not put your real keys here!
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "YOUR_TWILIO_ACCOUNT_SID_HERE")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "YOUR_TWILIO_AUTH_TOKEN_HERE")

# The WhatsApp sandbox number provided by Twilio
FROM_WHATSAPP_NUMBER = "whatsapp:+14155238886"

# Enter YOUR personal WhatsApp phone number with Ghana code (e.g., whatsapp:+233240000000)
TO_WHATSAPP_NUMBER = "whatsapp:+233549117215"

def send_whatsapp_ticket(ticket_text: str):
    """Transmits the daily structured prediction slip straight to your WhatsApp."""
    if "YOUR_TWILIO" in TWILIO_ACCOUNT_SID or "233240000000" in TO_WHATSAPP_NUMBER:
        print("⚠️ WhatsApp notification skipped: Twilio credentials or phone number not configured.")
        return False
        
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message_body = f"🎾 *DAILY SPORTYBET TICKET* 🎾\n\n{ticket_text}"
        
        message = client.messages.create(
            body=message_body,
            from_=FROM_WHATSAPP_NUMBER,
            to=TO_WHATSAPP_NUMBER
        )
        print(f"📱 WhatsApp notification dispatched successfully! SID: {message.sid}")
        return True
    except Exception as e:
        print(f"❌ Failed to dispatch WhatsApp notification: {e}")
        return False

if __name__ == "__main__":
    test_slip = "Leg 1: Test Match (Odds: 1.50)\n📈 Total Odds: 1.50x"
    send_whatsapp_ticket(test_slip)
