document.addEventListener('DOMContentLoaded', function() {
    const pendingRequestsList = document.getElementById('pending-requests-list');
    const knowledgeList = document.getElementById('knowledge-list');
    const responseModal = document.getElementById('response-modal');
    const requestDetails = document.getElementById('request-details');
    const responseText = document.getElementById('response-text');
    const submitResponse = document.getElementById('submit-response');
    const cancelResponse = document.getElementById('cancel-response');
    
    let currentRequestId = null;
    
    // Fetch and display data
    function loadData() {
        fetch('/api/help-requests/?status=pending')
            .then(response => response.json())
            .then(requests => {
                pendingRequestsList.innerHTML = '';
                requests.forEach(request => {
                    const requestCard = document.createElement('div');
                    requestCard.className = 'request-card pending';
                    requestCard.innerHTML = `
                        <h3>Request #${request.id}</h3>
                        <p><strong>From:</strong> ${request.customer_phone}</p>
                        <p><strong>Question:</strong> ${request.question}</p>
                        <p><strong>Received:</strong> ${new Date(request.created_at).toLocaleString()}</p>
                        <button class="respond-btn" data-id="${request.id}">Respond</button>
                    `;
                    pendingRequestsList.appendChild(requestCard);
                });
                
                // Add event listeners to respond buttons
                document.querySelectorAll('.respond-btn').forEach(btn => {
                    btn.addEventListener('click', function() {
                        currentRequestId = this.getAttribute('data-id');
                        const request = requests.find(r => r.id == currentRequestId);
                        requestDetails.innerHTML = `
                            <p><strong>Customer:</strong> ${request.customer_phone}</p>
                            <p><strong>Question:</strong> ${request.question}</p>
                        `;
                        responseModal.style.display = 'flex';
                    });
                });
            });
            
        fetch('/api/knowledge/')
            .then(response => response.json())
            .then(knowledge => {
                knowledgeList.innerHTML = '';
                knowledge.forEach(item => {
                    const knowledgeCard = document.createElement('div');
                    knowledgeCard.className = 'knowledge-card';
                    knowledgeCard.innerHTML = `
                        <h3>${item.question}</h3>
                        <p>${item.answer}</p>
                    `;
                    knowledgeList.appendChild(knowledgeCard);
                });
            });
    }
    
    // Handle response submission
    submitResponse.addEventListener('click', function() {
        if (!currentRequestId || !responseText.value.trim()) return;
        
        fetch(`/api/help-requests/${currentRequestId}/resolve`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                answer: responseText.value.trim(),
                add_to_knowledge: true
            })
        })
        .then(response => {
            if (response.ok) {
                responseModal.style.display = 'none';
                responseText.value = '';
                loadData(); // Refresh the lists
            }
        });
    });
    
    // Handle modal cancellation
    cancelResponse.addEventListener('click', function() {
        responseModal.style.display = 'none';
        responseText.value = '';
    });
    
    // Initial load
    loadData();
    
    // Refresh every 30 seconds
    setInterval(loadData, 30000);
});