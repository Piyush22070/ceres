import React, { useState } from 'react';
import { useMessages } from '../hooks/useMessages';
import { useSpeechRecognition } from '../hooks/useSpeechReconisation';
import { ChatHeader } from './ChatHeader';
import { MessageList } from './MessageList';
import { ChatInput } from './ChatInput';
import { InputMode } from '../types';

export const CeresChatBot: React.FC = () => {
  const [isProcessing, setIsProcessing] = useState(false);
  const [inputMode, setInputMode] = useState<InputMode>('text');
  
  const { messages, addMessage, clearMessages, runCommand } = useMessages();

  const handleVoiceResult = async (transcript: string) => {
    addMessage(transcript, 'user');
    setIsProcessing(true);
    try {
      await runCommand(transcript);
    } finally {
      setIsProcessing(false);
    }
  };

  const { isListening, toggleListening } = useSpeechRecognition({
    onResult: handleVoiceResult,
    onStatusMessage: (message) => addMessage(message, 'status'),
  });

  const handleTextSubmit = async (message: string) => {
    addMessage(message, 'user');
    setIsProcessing(true);
    try {
      await runCommand(message);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleRefresh = () => {
    if (!isProcessing) {
      clearMessages();
      if (isListening) {
        toggleListening();
      }
    }
  };

  const handleToggleInputMode = () => {
    if (!isProcessing) {
      setInputMode(prev => prev === 'text' ? 'voice' : 'text');
      if (isListening) {
        toggleListening();
      }
    }
  };

  return (
    <div className="mt-0 w-[360px] h-[460px] bg-white shadow-2xl flex flex-col overflow-hidden border border-gray-200">
      <ChatHeader
        isProcessing={isProcessing}
        isListening={isListening}
        inputMode={inputMode}
        onRefresh={handleRefresh}
        onToggleListening={toggleListening}
        onToggleInputMode={handleToggleInputMode}
      />

      <MessageList messages={messages} isProcessing={isProcessing} />

      <ChatInput
        inputMode={inputMode}
        isProcessing={isProcessing}
        isListening={isListening}
        onSubmit={handleTextSubmit}
        onToggleListening={toggleListening}
      />
    </div>
  );
};