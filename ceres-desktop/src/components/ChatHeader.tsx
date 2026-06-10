import React from 'react';
import { Bot, RefreshCw, Mic, MicOff, Type, Volume2 } from 'lucide-react';
import { InputMode } from '../types';

interface ChatHeaderProps {
  isProcessing: boolean;
  isListening: boolean;
  inputMode: InputMode;
  onRefresh: () => void;
  onToggleListening: () => void;
  onToggleInputMode: () => void;
}

export const ChatHeader: React.FC<ChatHeaderProps> = ({
  isProcessing,
  isListening,
  inputMode,
  onRefresh,
  onToggleListening,
  onToggleInputMode,
}) => {
  const getStatusText = () => {
    if (isProcessing) return '🔄 Processing command...';
    if (isListening) return '🎤 Listening for voice...';
    return 'AI Computer Control';
  };

  return (
    <div className="bg-gray-900 p-3 flex items-center gap-3 shadow-md border-b border-gray-700">
      <div className="w-9 h-9 bg-gray-800 rounded-xl flex items-center justify-center border border-gray-700 shadow-sm">
        <Bot className="w-5 h-5 text-gray-300" />
      </div>
      
      <div className="flex-1 flex items-center justify-between">
        <div className="flex flex-col">
          <h3 className="text-gray-100 font-semibold text-sm tracking-wide">Ceres</h3>
          <p className="text-gray-400 text-[11px]">{getStatusText()}</p>
        </div>
        
        <div className="flex gap-1">
          {/* Input Mode Toggle */}
          <button
            onClick={onToggleInputMode}
            className="px-2 py-1 text-xs rounded-md border bg-gray-800 text-gray-300 border-gray-700 hover:bg-gray-700 hover:text-white flex items-center gap-1 transition-all duration-200"
            disabled={isProcessing}
            title={`Switch to ${inputMode === 'text' ? 'voice' : 'text'} mode`}
          >
            {inputMode === 'text' ? (
              <>
                <Volume2 className="w-3 h-3" />
                Voice
              </>
            ) : (
              <>
                <Type className="w-3 h-3" />
                Text
              </>
            )}
          </button>

          {/* Voice Toggle (only shown in voice mode) */}
          {inputMode === 'voice' && (
            <button
              onClick={onToggleListening}
              className={`px-2 py-1 text-xs rounded-md border flex items-center gap-1 transition-all duration-200 ${
                isListening
                  ? 'bg-red-600 text-white border-red-500 animate-pulse'
                  : 'bg-gray-800 text-gray-300 border-gray-700 hover:bg-gray-700 hover:text-white'
              }`}
              disabled={isProcessing}
              title={isListening ? 'Stop listening' : 'Start listening'}
            >
              {isListening ? (
                <>
                  <MicOff className="w-3 h-3" />
                  Stop
                </>
              ) : (
                <>
                  <Mic className="w-3 h-3" />
                  Listen
                </>
              )}
            </button>
          )}

          {/* Refresh Button */}
          <button
            onClick={onRefresh}
            className="px-2 py-1 text-xs rounded-md border bg-gray-800 text-gray-300 border-gray-700 hover:bg-gray-700 hover:text-white flex items-center gap-1 transition-all duration-200"
            disabled={isProcessing}
            title="Refresh chat"
          >
            <RefreshCw className="w-3 h-3" />
            Refresh
          </button>
        </div>
      </div>
    </div>
  );
};