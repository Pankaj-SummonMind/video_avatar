// UI Helper Functions

// Initialize UI components
function initUI() {
    // Add event listeners
    const messageInput = document.getElementById('messageInput');
    if (messageInput) {
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    }
    
    // Load initial avatars
    loadAvatars();
    
    // Update status periodically
    setInterval(() => {
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: 'ping' }));
        }
    }, 30000);
}

// Show/hide loading spinner
function showLoading(show) {
    let spinner = document.getElementById('loadingSpinner');
    if (!spinner) {
        spinner = document.createElement('div');
        spinner.id = 'loadingSpinner';
        spinner.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        spinner.style.position = 'fixed';
        spinner.style.top = '50%';
        spinner.style.left = '50%';
        spinner.style.transform = 'translate(-50%, -50%)';
        spinner.style.background = 'rgba(0,0,0,0.8)';
        spinner.style.color = 'white';
        spinner.style.padding = '20px';
        spinner.style.borderRadius = '10px';
        spinner.style.zIndex = '1000';
        spinner.style.display = 'flex';
        spinner.style.alignItems = 'center';
        spinner.style.gap = '10px';
        document.body.appendChild(spinner);
    }
    spinner.style.display = show ? 'flex' : 'none';
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'info-circle'}"></i>
        ${message}
    `;
    notification.style.position = 'fixed';
    notification.style.bottom = '20px';
    notification.style.right = '20px';
    notification.style.background = type === 'success' ? '#4CAF50' : '#2196F3';
    notification.style.color = 'white';
    notification.style.padding = '15px 20px';
    notification.style.borderRadius = '5px';
    notification.style.zIndex = '999';
    notification.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Add message to chat
function addChatMessage(sender, text, type) {
    const messagesDiv = document.getElementById('chatMessages');
    if (!messagesDiv) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    messageDiv.innerHTML = `
        <div class="message-content">${text}</div>
        <div class="message-time">${time}</div>
    `;
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Update connection status
function updateStatus(status, isConnected) {
    const statusText = document.getElementById('statusText');
    const statusDot = document.getElementById('statusDot');
    if (statusText) statusText.textContent = status;
    if (statusDot) {
        statusDot.className = `status-dot ${isConnected ? 'connected' : 'disconnected'}`;
    }
}

// Update avatar status
function updateAvatarStatus(status, color) {
    const statusEl = document.getElementById('avatarStatus');
    if (statusEl) {
        statusEl.innerHTML = `<i class="fas fa-circle" style="color: ${color};"></i> ${status}`;
    }
}

// Log debug messages
function logDebug(message) {
    const debugEl = document.getElementById('debugInfo');
    if (debugEl) {
        const timestamp = new Date().toLocaleTimeString();
        debugEl.textContent += `[${timestamp}] ${message}\n`;
        debugEl.scrollTop = debugEl.scrollHeight;
    }
    console.log(message);
}

// Export functions globally
window.initUI = initUI;
window.showLoading = showLoading;
window.showNotification = showNotification;
window.addChatMessage = addChatMessage;
window.updateStatus = updateStatus;
window.updateAvatarStatus = updateAvatarStatus;
window.logDebug = logDebug;