// File: src/hooks/useMessages.ts

import { useState, useCallback, useRef } from 'react';
import { Message } from '../types';

export const useMessages = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      // --- CORRECTED LINE ---
      text: "Hi! I'm Ceres, your AI assistant — I can open apps, send emails, search the web, control your system, and more. Try me!",
      type: 'bot',
      timestamp: new Date(),
    },
  ]);

  const wsRef = useRef<WebSocket | null>(null);

  const addMessage = useCallback((text: string, type: 'user' | 'bot' | 'status') => {
    const newMessage: Message = {
      id: Date.now().toString() + Math.random().toString(),
      text,
      type,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, newMessage]);
  }, []);

  const clearMessages = useCallback(() => {
    setMessages([
      {
        id: '1',
        text: "Hi! I'm Ceres, your AI assistant — I can open apps, send emails, search the web, control your system, and more. Try me!",
        type: 'bot',
        timestamp: new Date(),
      },
    ]);
  }, []);

  const connectSocket = useCallback(() => {
    if (wsRef.current && wsRef.current.readyState < 2) return;

    wsRef.current = new WebSocket("ws://localhost:8000/ws/execute");

    wsRef.current.onopen = () => {
      console.log("✅ WebSocket connected");
    };

    wsRef.current.onclose = () => {
      console.log("❌ WebSocket disconnected");
      wsRef.current = null;
    };

    wsRef.current.onerror = (err) => {
      console.error("WebSocket error:", err);
      addMessage("❌ Connection error - unable to process your request.", "bot");
    };

    wsRef.current.onmessage = (event) => {
      let text = event.data;

      if (text === "###DONE###") {
        return; // End of response
      }

      if (text.startsWith("🔍 Parsing command:")) {
        text = "🔍 Parsing command...";
      } else if (text.includes("AppleScript executed successfully")) {
        text = "✅ Task completed successfully!";
      }

      if (text.trim()) {
        addMessage(text, "bot");
      }
    };
  }, [addMessage]);

  const runCommand = useCallback(
    (userMessage: string) => {
      connectSocket();

      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
        wsRef.current.send(userMessage);
      } else {
        setTimeout(() => {
          if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
            wsRef.current.send(userMessage);
          } else {
            addMessage("❌ Failed to send command - WebSocket not ready.", "bot");
          }
        }, 500);
      }
    },
    [addMessage, connectSocket]
  );

  return {
    messages,
    addMessage,
    clearMessages,
    runCommand,
  };
};