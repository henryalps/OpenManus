import React from 'react';

function ChatDisplay({ messages }) {
  return (
    <div style={{
      border: '1px solid #ccc',
      borderRadius: '8px',
      padding: '20px',
      minHeight: '400px',
      maxHeight: '600px',
      overflowY: 'auto',
      backgroundColor: '#f9f9f9',
      marginBottom: '20px'
    }}>
      {messages.length === 0 ? (
        <div style={{ textAlign: 'center', color: '#999', padding: '40px' }}>
          No messages yet. Start a conversation!
        </div>
      ) : (
        messages.map((message, index) => (
          <div
            key={index}
            style={{
              marginBottom: '15px',
              padding: '10px',
              borderRadius: '8px',
              backgroundColor: message.sender === 'user' ? '#e3f2fd' : '#fff',
              border: message.sender === 'user' ? '1px solid #2196f3' : '1px solid #ddd',
            }}
          >
            <strong style={{ color: message.sender === 'user' ? '#1976d2' : '#388e3c' }}>
              {message.sender === 'user' ? 'You' : 'OpenManus'}:
            </strong>
            <div style={{ marginTop: '5px', whiteSpace: 'pre-wrap' }}>
              {message.text}
            </div>
          </div>
        ))
      )}
    </div>
  );
}

export default ChatDisplay;