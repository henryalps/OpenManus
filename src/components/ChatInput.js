import React, { useState } from 'react';
import { HStack, Input, IconButton } from '@chakra-ui/react';
import { FaPaperPlane } from 'react-icons/fa';

function ChatInput({ onSendMessage }) {
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim()) {
      onSendMessage(inputValue);
      setInputValue('');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <HStack>
        <Input
          value={inputValue}
          onChange={handleInputChange}
          placeholder="Ask me anything..."
          variant="filled"
        />
        <IconButton
          colorScheme="blue"
          aria-label="Send message"
          icon={<FaPaperPlane />}
          type="submit"
          _hover={{ bg: 'blue.600' }}
        />
      </HStack>
    </form>
  );
}

export default ChatInput;