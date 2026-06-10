import React, { useEffect, useRef } from 'react';
import { CheckCircle, XCircle, Info } from 'lucide-react';
import { Message } from '../types';

interface MessageListProps {
  messages: Message[];
  isProcessing: boolean;
}

export const MessageList: React.FC<MessageListProps> = ({ messages, isProcessing }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const getMessageIcon = (message: Message) => {
    // Adjusted icon colors for better contrast on dark backgrounds
    if (message.type === 'status') {
      return <Info className="w-3 h-3 text-blue-400" />;
    }
    
    if (message.type === 'bot') {
      if (message.text.includes('') || message.text.includes('successfully')) {
        return <CheckCircle className="w-3 h-3 text-green-400" />;
      }
      if (message.text.includes('') || message.text.includes('Error')) {
        return <XCircle className="w-3 h-3 text-red-400" />;
      }
    }
    
    return null;
  };
  
  return (
    <div className="flex-1 p-4 overflow-y-auto bg-gray-800 space-y-3">
      {messages.map((message) => (
        <div
          key={message.id}
          className={`flex ${
            message.type === 'user' ? 'justify-end' : 'justify-start'
          } animate-fadeIn`}
        >
          <div
            className={`max-w-[80%] p-2 rounded-lg text-sm ${
              message.type === 'user'
                ? 'bg-blue-500 text-white rounded-br-sm'
                : message.type === 'status'
                ? 'bg-blue-950 text-blue-300 border border-blue-800 rounded-lg text-xs flex items-center gap-2'
                : message.text.includes('✅')
                ? 'bg-green-950 text-green-300 rounded-bl-sm shadow-sm border border-green-800 flex items-center gap-2'
                : message.text.includes('❌')
                ? 'bg-red-950 text-red-300 rounded-bl-sm shadow-sm border border-red-800 flex items-center gap-2'
                : 'bg-gray-700 text-gray-200 rounded-bl-sm shadow-sm border border-gray-600 flex items-center gap-2'
            }`}
          >
            {getMessageIcon(message)}
            <span className="flex-1">{message.text}</span>
          </div>
        </div>
      ))}

      {isProcessing && (
        <div className="flex justify-start">
          <div className="bg-gray-700 p-3 rounded-lg rounded-bl-sm shadow-sm border border-gray-600 flex items-center gap-2">
            <div className="flex gap-1">
              <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
              <div
                className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"
                style={{ animationDelay: '0.1s' }}
              ></div>
              <div
                className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"
                style={{ animationDelay: '0.2s' }}
              ></div>
            </div>
            <span className="text-gray-300 text-xs">Ceres is working...</span>
          </div>
        </div>
      )}
      <div ref={messagesEndRef} />
    </div>
  );
};