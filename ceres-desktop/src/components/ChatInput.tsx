import React, { useState } from 'react';
import { Send, Mic, MicOff } from 'lucide-react';
import { InputMode } from '../types';

interface ChatInputProps {
  inputMode: InputMode;
  isProcessing: boolean;
  isListening: boolean;
  onSubmit: (message: string) => Promise<void>;
  onToggleListening: () => void;
}

export const ChatInput: React.FC<ChatInputProps> = ({
  inputMode,
  isProcessing,
  isListening,
  onSubmit,
  onToggleListening,
}) => {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isProcessing) return;

    const userMessage = inputValue.trim();
    setInputValue('');
    await onSubmit(userMessage);
  };

  const getPlaceholder = () => {
    if (isProcessing) return 'Processing your command...';
    if (inputMode === 'voice') {
      return isListening ? 'Listening for your command...' : 'Click the mic to speak your command...';
    }
    return 'Tell me what to automate (e.g., "open calculator")...';
  };

  if (inputMode === 'voice') {
    return (
      <div className="p-4 bg-gray-900 border-t border-gray-700">
        <div className="flex gap-2 items-center justify-center">
          <button
            onClick={onToggleListening}
            disabled={isProcessing}
            className={`flex-1 p-4 rounded-lg flex items-center justify-center gap-2 text-sm font-medium transition-all duration-200 ${
              isListening
                ? 'bg-red-600 text-white hover:bg-red-700 animate-pulse focus:ring-red-500'
                : 'bg-gray-700 text-gray-200 hover:bg-gray-600 focus:ring-blue-500'
            } disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-900`}
          >
            {isListening ? (
              <>
                <MicOff className="w-5 h-5" />
                Stop Listening
              </>
            ) : (
              <>
                <Mic className="w-5 h-5" />
                {isProcessing ? 'Processing...' : 'Start Voice Command'}
              </>
            )}
          </button>
        </div>
        <p className="text-center text-xs text-gray-400 mt-2">
          {getPlaceholder()}
        </p>
      </div>
    );
  }

  return (
    <div className="p-4 bg-gray-900 border-t border-gray-700">
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder={getPlaceholder()}
          className="flex-1 px-3 py-2 bg-gray-800 border border-gray-600 text-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder:text-gray-500 text-sm transition-all duration-200"
          disabled={isProcessing}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSubmit(e as unknown as React.FormEvent);
            }
          }}
        />
        <button
          type="submit"
          disabled={!inputValue.trim() || isProcessing}
          className="p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-gray-900 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center justify-center min-w-[40px]"
        >
          {isProcessing ? (
            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          ) : (
            <Send className="w-4 h-4" />
          )}
        </button>
      </form>
    </div>
  );
};