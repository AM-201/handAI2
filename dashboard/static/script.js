// Dashboard State Update Functions

function updateGestureInfo() {
    fetch('/api/gesture')
        .then(response => response.json())
        .then(data => {
            document.getElementById('currentGesture').textContent = data.current_gesture || 'None';
            document.getElementById('lastGestureTime').textContent = data.last_gesture_time || '--:--:--';
            document.getElementById('frameCount').textContent = data.frame_count;
        })
        .catch(error => console.error('Error fetching gesture info:', error));
}

function updateMQTTInfo() {
    fetch('/api/mqtt')
        .then(response => response.json())
        .then(data => {
            // Update ESP32 status
            const esp32StatusEl = document.getElementById('esp32Status');
            if (data.esp32_status && data.esp32_status !== 'Disconnected') {
                esp32StatusEl.textContent = 'Connected';
                esp32StatusEl.className = 'value status-connected';
            } else {
                esp32StatusEl.textContent = 'Disconnected';
                esp32StatusEl.className = 'value status-disconnected';
            }

            // Update LED states
            updateLEDStates(data.led_states);

            // Update MQTT log
            updateMQTTLog(data.messages_sent);
        })
        .catch(error => console.error('Error fetching MQTT info:', error));
}

function updateLEDStates(ledStates) {
    const ledMap = {
        'G': 'ledG',
        'R': 'ledR',
        'W': 'ledW'
    };

    for (const [color, elementId] of Object.entries(ledMap)) {
        const ledEl = document.getElementById(elementId);
        if (ledStates[color]) {
            ledEl.classList.remove('led-off');
            ledEl.classList.add(`led-on-${color.toLowerCase()}`);
        } else {
            ledEl.classList.remove(`led-on-${color.toLowerCase()}`);
            ledEl.classList.add('led-off');
        }
    }
}

function updateMQTTLog(messages) {
    const logEl = document.getElementById('mqttLog');
    
    if (messages.length === 0) {
        logEl.innerHTML = '<p class="log-entry">No messages yet...</p>';
        return;
    }

    let logHTML = '';
    messages.slice().reverse().forEach(msg => {
        logHTML += `<p class="log-entry">
            <span class="timestamp">[${msg.timestamp}]</span>
            <span class="gesture">${msg.gesture}</span>
            → <span class="message">${msg.mqtt_message}</span>
        </p>`;
    });

    logEl.innerHTML = logHTML;
}

function updateSerialLog() {
    fetch('/api/serial')
        .then(response => response.json())
        .then(data => {
            const logEl = document.getElementById('serialLog');
            
            if (data.logs.length === 0) {
                logEl.innerHTML = '<p class="log-entry">No serial data yet...</p>';
                return;
            }

            let logHTML = '';
            data.logs.slice().reverse().forEach(log => {
                logHTML += `<p class="log-entry">${escapeHtml(log)}</p>`;
            });

            logEl.innerHTML = logHTML;
            // Auto-scroll to bottom
            logEl.scrollTop = logEl.scrollHeight;
        })
        .catch(error => console.error('Error fetching serial logs:', error));
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Initialize dashboard and set up auto-refresh
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard loaded. Starting updates...');

    // Initial update
    updateGestureInfo();
    updateMQTTInfo();
    updateSerialLog();

    // Set up periodic updates (every 1 second)
    setInterval(updateGestureInfo, 1000);
    setInterval(updateMQTTInfo, 1000);
    setInterval(updateSerialLog, 1000);

    console.log('Dashboard updates started.');
});
