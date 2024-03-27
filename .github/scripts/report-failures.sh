WEBHOOK_URL="$WEBHOOK_URL"
WORKFLOW_URL="$WORKFLOW_URL"

send_message_to_discord() {
    local message="$1"
    # Use curl to send a POST request to the webhook URL
    curl -X POST -H "Content-Type: application/json" -d "{\"content\":\"$message\"}" "$WEBHOOK_URL"
}

send_message_to_discord "test failed! $WORKFLOW_URL"
