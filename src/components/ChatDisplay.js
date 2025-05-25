import React from "react";

function ChatDisplay({ messages }) {
  return (
    <div>
      {messages.map((message, index) => (
        <div key={index}>
          <strong>{message.sender}:</strong> {message.text}
        </div>
      ))}
    </div>
  );
}

export default ChatDisplay;
