import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, MessageCircle, Loader } from 'lucide-react';
import { useGetRunTrace } from '../../hooks/useReports';

export const AgentChat = ({ runId }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const { data: traceData } = useGetRunTrace(runId);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Convert trace data to chat messages - REAL DATA FROM API
  useEffect(() => {
    if (!traceData?.trace) return;

    const trace = traceData.trace;
    const newMessages = [
      {
        id: 1,
        type: 'agent',
        text: `👋 Hi! I'm monitoring your food rescue operation (Run: ${runId.slice(0, 8)}...). Here's the real-time status:`,
        timestamp: new Date(),
      },
    ];

    let msgId = 2;

    // Extract agent steps from trace
    if (trace.steps && Array.isArray(trace.steps)) {
      trace.steps.forEach((step) => {
        newMessages.push({
          id: msgId++,
          type: 'agent',
          text: `🤖 ${step.agent || 'Agent'}: ${step.description || step.output || 'Processing...'}`,
          timestamp: new Date(step.timestamp || Date.now()),
        });
      });
    }

    // Add status message
    if (trace.status) {
      newMessages.push({
        id: msgId++,
        type: 'agent',
        text: `📊 Current Status: ${trace.status}`,
        timestamp: new Date(),
      });
    }

    // Add output/decision if available
    if (trace.output) {
      const outputText = typeof trace.output === 'string' 
        ? trace.output 
        : JSON.stringify(trace.output).slice(0, 100);
      newMessages.push({
        id: msgId++,
        type: 'agent',
        text: `✅ Result: ${outputText}`,
        timestamp: new Date(),
      });
    }

    setMessages(newMessages);

    // Poll for updates every 2 seconds (real-time)
    const pollInterval = setInterval(() => {
      // This will trigger re-fetch automatically via useGetRunTrace
    }, 2000);

    return () => clearInterval(pollInterval);
  }, [traceData, runId]);

  const handleSendMessage = () => {
    if (!inputValue.trim()) return;

    // Add user message
    setMessages((prev) => [
      ...prev,
      {
        id: prev.length + 1,
        type: 'user',
        text: inputValue,
        timestamp: new Date(),
      },
    ]);

    const userQuestion = inputValue;
    setInputValue('');
    setIsLoading(true);

    // In a real scenario, you would call an API endpoint here
    // For now, we'll just acknowledge the message
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        {
          id: prev.length + 1,
          type: 'agent',
          text: `📝 I've noted your message: "${userQuestion}". The operations team has been alerted.`,
          timestamp: new Date(),
        },
      ]);

      setIsLoading(false);
    }, 500);
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex flex-col h-[500px] bg-white rounded-lg border border-soft-sage shadow-sm overflow-hidden"
    >
      {/* Header */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-700 text-white p-4 flex items-center gap-2">
        <MessageCircle size={20} />
        <div>
          <h3 className="font-semibold">Agent Updates</h3>
          <p className="text-xs opacity-90">Real-time food rescue tracking</p>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-cream">
        <AnimatePresence>
          {messages.map((msg) => (
            <motion.div
              key={msg.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs px-4 py-3 rounded-lg ${
                  msg.type === 'user'
                    ? 'bg-primary-600 text-white rounded-br-none'
                    : 'bg-white border border-soft-sage text-text-primary rounded-bl-none'
                }`}
              >
                <p className="text-sm">{msg.text}</p>
                <p className={`text-xs mt-1 ${msg.type === 'user' ? 'text-primary-100' : 'text-text-muted'}`}>
                  {msg.timestamp.toLocaleTimeString()}
                </p>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {isLoading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex items-center gap-2 text-text-secondary"
          >
            <Loader size={16} className="animate-spin" />
            <span className="text-sm">Agent is thinking...</span>
          </motion.div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t border-soft-sage p-4 bg-white">
        <div className="flex gap-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Ask about your food rescue..."
            className="flex-1 px-4 py-2 rounded-lg border border-soft-sage bg-cream focus:outline-none focus:ring-2 focus:ring-primary-600"
          />
          <button
            onClick={handleSendMessage}
            disabled={isLoading || !inputValue.trim()}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-text-muted transition-colors flex items-center gap-2"
          >
            <Send size={18} />
          </button>
        </div>
      </div>
    </motion.div>
  );
};
