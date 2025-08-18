import React, { useEffect, useRef } from 'react';
import {
  VStack,
  Box,
  Flex,
  Avatar,
  Text,
  useColorModeValue,
} from '@chakra-ui/react';
import { FaUser, FaRobot } from 'react-icons/fa';
import { motion } from 'framer-motion';

const MotionFlex = motion(Flex);

function ChatDisplay({ messages }) {
  const endOfMessagesRef = useRef(null);
  const bgColor = useColorModeValue('gray.100', 'gray.700');
  const userBgColor = useColorModeValue('blue.500', 'blue.300');
  const aiBgColor = useColorModeValue('gray.200', 'gray.600');
  const userColor = 'white';
  const aiColor = useColorModeValue('black', 'white');

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const messageVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 },
  };

  return (
    <VStack
      flex="1"
      width="100%"
      spacing={4}
      p={4}
      bg={bgColor}
      borderRadius="lg"
      overflowY="auto"
    >
      {messages.map((message, index) => (
        <MotionFlex
          key={index}
          w="100%"
          justify={message.role === 'user' ? 'flex-end' : 'flex-start'}
          initial="hidden"
          animate="visible"
          variants={messageVariants}
          transition={{ duration: 0.3, delay: index * 0.1 }}
        >
          {message.role !== 'user' && <Avatar as={FaRobot} mr={3} />}
          <Box
            bg={message.role === 'user' ? userBgColor : aiBgColor}
            color={message.role === 'user' ? userColor : aiColor}
            px={4}
            py={2}
            borderRadius="lg"
            maxWidth="70%"
          >
            <Text>{message.content}</Text>
          </Box>
          {message.role === 'user' && <Avatar as={FaUser} ml={3} />}
        </MotionFlex>
      ))}
      <div ref={endOfMessagesRef} />
    </VStack>
  );
}

export default ChatDisplay;