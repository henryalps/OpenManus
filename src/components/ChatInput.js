import React, { useState } from 'react';

function ChatInput({ onSendMessage }) {
  const [inputValue, setInputValue] = useState('');

  const handleSend = () => {
    if (inputValue.trim()) {
      onSendMessage(inputValue);
      setInputValue('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };

  return (
    <div style={{ padding: '20px', borderTop: '1px solid #ccc' }}>
      <input
        type="text"
        placeholder="Type your message..."
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyPress={handleKeyPress}
        style={{ width: '80%', padding: '10px', fontSize: '16px' }}
      />
      <button
        onClick={handleSend}
        style={{ width: '18%', padding: '10px', fontSize: '16px', marginLeft: '2%' }}
      >
        Send
      </button>
    </div>
  );
}

export default ChatInput;