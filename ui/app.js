document.addEventListener('DOMContentLoaded', () => {
    // --- SPA Routing Logic ---
    const navItems = document.querySelectorAll('.nav-item');
    const viewSections = document.querySelectorAll('.view-section');
    const placeholderTitle = document.getElementById('placeholder-title');

    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Remove active from all nav items
            navItems.forEach(nav => nav.classList.remove('active'));
            // Add active to clicked item
            item.classList.add('active');

            // Hide all sections
            viewSections.forEach(section => section.style.display = 'none');

            // Show target section
            const targetId = item.getAttribute('data-target');
            const targetSection = document.getElementById(targetId);
            
            if (targetSection) {
                targetSection.style.display = 'block';
                // If it's the placeholder, update the title
                if (targetId === 'view-placeholder') {
                    placeholderTitle.textContent = item.textContent.trim();
                }
            }
        });
    });

    // --- Slide Over Modal Logic ---
    const openBtn = document.getElementById('openChatBtn');
    const closeBtn = document.getElementById('closeChatBtn');
    const overlay = document.getElementById('chatOverlay');
    const slideOver = document.getElementById('chatSlideOver');

    function openChat() {
        overlay.classList.add('active');
        slideOver.classList.add('active');
        document.getElementById('message-input').focus();
    }

    function closeChat() {
        overlay.classList.remove('active');
        slideOver.classList.remove('active');
    }

    openBtn.addEventListener('click', openChat);
    closeBtn.addEventListener('click', closeChat);
    overlay.addEventListener('click', closeChat);

    // --- Chat Logic ---
    const input = document.getElementById('message-input');
    const sendBtn = document.getElementById('send-btn');
    const chatHistory = document.getElementById('chat-history');
    
    // Insights elements
    const resDecision = document.getElementById('res-decision');
    const reasonBox = document.getElementById('reason-box');
    const resReason = document.getElementById('res-reason');
    const resIntent = document.getElementById('res-intent');
    const resConfidenceText = document.getElementById('res-confidence-text');
    const resGrounded = document.getElementById('res-grounded');

    function appendMessage(text, type) {
        const div = document.createElement('div');
        div.className = `message ${type}`;
        
        const sender = document.createElement('span');
        sender.className = 'sender';
        sender.textContent = type === 'customer' ? 'Customer' : 'Sarathi';
        
        const content = document.createElement('div');
        content.textContent = text;
        
        div.appendChild(sender);
        div.appendChild(content);
        chatHistory.appendChild(div);
        
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    async function processMessage() {
        const msg = input.value.trim();
        if (!msg) return;

        // Reset UI
        input.value = '';
        input.disabled = true;
        sendBtn.disabled = true;
        sendBtn.innerHTML = '<i class="ph ph-spinner-gap"></i>';
        
        appendMessage(msg, 'customer');

        try {
            const response = await fetch('http://localhost:8000/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: msg })
            });

            if (!response.ok) {
                throw new Error('API Error');
            }

            const data = await response.json();
            
            // Update Chat
            if (data.decision === 'AUTO_HANDLE') {
                appendMessage(data.generated_reply, 'agent');
            } else {
                appendMessage(`[ESCALATED] Reason: ${data.escalation_reason}`, 'agent');
            }

            // Update Insights
            resDecision.textContent = data.decision;
            resDecision.style.color = data.decision === 'AUTO_HANDLE' ? 'var(--green)' : 'var(--red)';
            
            if (data.decision === 'ESCALATE') {
                reasonBox.style.display = 'block';
                resReason.textContent = data.escalation_reason;
            } else {
                reasonBox.style.display = 'none';
            }

            resIntent.textContent = data.intent;
            const confPercent = Math.round(data.intent_confidence * 100);
            resConfidenceText.textContent = `${confPercent}%`;
            
            resGrounded.textContent = data.is_grounded ? "PASSED" : "FAILED";
            resGrounded.style.color = data.is_grounded ? "var(--green)" : "var(--red)";

        } catch (error) {
            console.error(error);
            appendMessage(`Error: ${error.message}. Backend might be down.`, 'agent');
        } finally {
            input.disabled = false;
            sendBtn.disabled = false;
            sendBtn.innerHTML = '<i class="ph ph-paper-plane-right"></i> Send';
            input.focus();
        }
    }

    sendBtn.addEventListener('click', processMessage);
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            processMessage();
        }
    });
});
