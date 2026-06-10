// File: src/hooks/useSpeechReconisation.ts

import { useState, useRef, useEffect, useCallback } from 'react';
import { SpeechRecognition, SpeechRecognitionEvent } from '../types';

interface UseSpeechRecognitionProps {
  onResult: (transcript: string) => Promise<void>;
  onStatusMessage: (message: string) => void;
}

export const useSpeechRecognition = ({ onResult, onStatusMessage }: UseSpeechRecognitionProps) => {
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef<SpeechRecognition | null>(null);

  const initRecognition = useCallback(() => {
    const SR = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition;
    if (!SR) {
      onStatusMessage('🎤 Speech Recognition not supported in this browser.');
      return null;
    }

    const recognition = new SR() as SpeechRecognition;
    // --- CORRECTED LINE ---
    recognition.lang = 'en-US'; 
    recognition.interimResults = false;
    recognition.continuous = false;

    recognition.onstart = () => {
      setIsListening(true);
      onStatusMessage('🎤 Listening...');
    };

    recognition.onresult = async (event: SpeechRecognitionEvent) => {
      const transcript = event.results[0]?.[0]?.transcript?.trim() || '';
      if (transcript) {
        await onResult(transcript);
      }
    };

    recognition.onerror = (event: any) => {
      if (event.error === 'no-speech') {
        onStatusMessage('🎤 No speech was detected. Please try again.');
      } else {
        onStatusMessage(`🎤 Speech recognition error: ${event.error}`);
      }
      setIsListening(false);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    return recognition;
  }, [onResult, onStatusMessage]);

  const toggleListening = useCallback(async () => {
    if (isListening) {
      recognitionRef.current?.stop();
      return;
    }
    
    // You might want to add a permission check here
    const recognition = initRecognition();
    if (recognition) {
      recognitionRef.current = recognition;
      recognition.start();
    }
  }, [isListening, initRecognition]);

  useEffect(() => {
    const recognition = recognitionRef.current;
    return () => {
      recognition?.stop();
    };
  }, []);

  return {
    isListening,
    toggleListening,
  };
};