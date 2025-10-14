import ChatInput from '../components/ChatInput';
import ChatDisplay from '../components/ChatDisplay';
import React, { useState } from 'react';

function HomePage() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (newMessage) => {
    // Add user message to chat
    const userMsg = { sender: 'user', text: newMessage };
    setMessages(prev => [...prev, userMsg]);
    setIsLoading(true);

    try {
      // Build the conversation history for the API
      const conversationHistory = [...messages, userMsg].map(msg => ({
        role: msg.sender === 'user' ? 'user' : 'assistant',
        content: msg.text
      }));

      // Send to backend API
      const response = await fetch('http://localhost:8000/api/chat/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: conversationHistory
        }),
      });

      if (!response.ok) {
        // Try to get error details from response
        let errorMsg = `Backend returned error (status ${response.status})`;
        try {
          const errorText = await response.text();
          if (errorText) {
            const errorData = JSON.parse(errorText);
            errorMsg = errorData.detail || errorMsg;
          }
        } catch (e) {
          // Could not parse error response
        }
        throw new Error(errorMsg);
      }

      // Read the SSE stream
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let aiResponse = '';
      let hasError = false;
      let errorMessage = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              let content = data.content || '';

              // If content is a stringified object, try to extract the actual message
              if (content.startsWith('{') || content.startsWith("{'")) {
                try {
                  // Handle Python dict format with single quotes
                  const pythonDictMatch = content.match(/HumanMessage\(content='([^']+)'/);
                  if (pythonDictMatch) {
                    content = pythonDictMatch[1];
                  }
                } catch (e) {
                  // If parsing fails, use the content as-is
                  console.log('Could not parse nested content, using raw:', content);
                }
              }

              aiResponse += content;
            } catch (e) {
              console.error('Error parsing SSE data:', e);
              // Check if the stream contains an error
              if (line.includes('error') || line.includes('Error') || line.includes('Exception')) {
                hasError = true;
                errorMessage = line;
              }
            }
          }
        }
      }

      // Check if we got an error in the stream
      if (hasError || (!aiResponse && errorMessage)) {
        throw new Error('Backend error processing your request. The system may need API keys configured. Check console for details.');
      }

      // Add AI response to chat
      setMessages(prev => [...prev, { sender: 'ai', text: aiResponse || 'No response received from AI. Please check if API keys are configured.' }]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Provide helpful error messages
      let userMessage = error.message;

      if (error.message.includes('Failed to fetch') || error.message.includes('network')) {
        userMessage = '❌ Cannot connect to backend server.\n\nPlease check:\n1. Is the backend running? (docker ps)\n2. Is it accessible at http://localhost:8000?';
      } else if (error.message.includes('Backend error')) {
        userMessage = '❌ Backend encountered an error.\n\nLikely causes:\n1. No API keys configured - Create a .env file with your LLM API keys\n2. Missing dependencies - Check docker logs\n\nTo configure API keys, create a .env file in the project root with:\nBASIC_API_KEY=your-api-key-here\nBASIC_BASE_URL=https://api.openai.com/v1\nBASIC_MODEL=gpt-3.5-turbo';
      }

      setMessages(prev => [...prev, {
        sender: 'ai',
        text: userMessage
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <h1 style={{ textAlign: 'center' }}>Welcome to OpenManus!</h1>
      <ChatDisplay messages={messages} />
      {isLoading && <div style={{ textAlign: 'center', padding: '10px' }}>AI is thinking...</div>}
      <ChatInput onSendMessage={handleSendMessage} />
    </div>
  );
}

export default HomePage;