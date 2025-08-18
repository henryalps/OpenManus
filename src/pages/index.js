import ChatInput from '../components/ChatInput';
import ChatDisplay from '../components/ChatDisplay';
import React, { useState, useEffect } from 'react';
import {
  Box,
  Flex,
  VStack,
  Heading,
  useColorMode,
  Button,
  Spacer,
} from '@chakra-ui/react';

function HomePage() {
  const [messages, setMessages] = useState([]);
  const { colorMode, toggleColorMode } = useColorMode();

  // A more realistic message handling
  const handleSendMessage = async (inputValue) => {
    if (!inputValue.trim()) return;

    const userMessage = { role: 'user', content: inputValue };
    setMessages((prevMessages) => [...prevMessages, userMessage]);

    try {
      const response = await fetch('http://localhost:8000/api/chat/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ messages: [...messages, userMessage] }),
      });

      if (!response.body) return;
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let aiMessageContent = '';

      // Add a new empty AI message to the state
      setMessages((prevMessages) => [...prevMessages, { role: 'assistant', content: '' }]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const eventLines = chunk.split('\n\n').filter(line => line.startsWith('data:'));

        for (const line of eventLines) {
          try {
            const jsonStr = line.substring(5);
            const eventData = JSON.parse(jsonStr);
            if (eventData.content) {
              aiMessageContent += eventData.content;
              setMessages((prevMessages) => {
                const newMessages = [...prevMessages];
                newMessages[newMessages.length - 1].content = aiMessageContent;
                return newMessages;
              });
            }
          } catch (e) {
            console.error('Failed to parse stream chunk:', line, e);
          }
        }
      }
    } catch (error) {
      console.error('Failed to send message:', error);
      const errorMessage = { role: 'assistant', content: 'Sorry, I had trouble connecting to the server.' };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    }
  };

  return (
    <Flex height="100vh" width="100vw" direction="column" align="center" justify="center">
      <Box width="100%" p={4}>
        <Flex>
          <Heading size="lg">Enhanced AutoGPT</Heading>
          <Spacer />
          <Button onClick={toggleColorMode}>
            Toggle {colorMode === 'light' ? 'Dark' : 'Light'}
          </Button>
        </Flex>
      </Box>
      <VStack
        flex="1"
        width={{ base: '100%', md: '80%', lg: '60%' }}
        p={4}
        spacing={4}
        align="stretch"
        overflowY="auto"
      >
        <ChatDisplay messages={messages} />
      </VStack>
      <Box width={{ base: '100%', md: '80%', lg: '60%' }} p={4}>
        <ChatInput onSendMessage={handleSendMessage} />
      </Box>
    </Flex>
  );
}

export default HomePage;