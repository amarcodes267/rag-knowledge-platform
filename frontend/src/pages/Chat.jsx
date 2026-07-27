import React, { useState, useRef, useEffect } from 'react';
import { sendMessage, getSessionId, clearChat, getChatStatus } from '../services/chatService';
import '../styles/Chat.css';

function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [systemStatus, setSystemStatus] = useState(null);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    getChatStatus().then(function (data) {
      setSystemStatus(data.status);
    }).catch(function () {
      setSystemStatus({ ollama_running: false, model_available: false });
    });
  }, []);

  useEffect(function () {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  function getTime() {
    return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }

  async function handleSend() {
    var text = input.trim();
    if (!text || isLoading) return;
    setError(null);
    var userMsg = { id: Date.now(), type: 'user', text: text, time: getTime() };
    setMessages(function (prev) { return prev.concat([userMsg]); });
    setInput('');
    setIsLoading(true);
    try {
      var sid = getSessionId();
      var result = await sendMessage(text, sid);
      if (result.success) {
        var aiMsg = {
          id: Date.now() + 1,
          type: 'ai',
          text: result.answer,
          time: getTime(),
          sources: result.sources || []
        };
        setMessages(function (prev) { return prev.concat([aiMsg]); });
      } else {
        var errMsg = {
          id: Date.now() + 1,
          type: 'error',
          text: result.error || 'Failed to get response',
          time: getTime()
        };
        setMessages(function (prev) { return prev.concat([errMsg]); });
      }
    } catch (err) {
      var errMsg2 = {
        id: Date.now() + 1,
        type: 'error',
        text: err.message || 'Connection error',
        time: getTime()
      };
      setMessages(function (prev) { return prev.concat([errMsg2]); });
    } finally {
      setIsLoading(false);
      if (inputRef.current) inputRef.current.focus();
    }
  }

  function handleKey(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  async function handleClear() {
    try {
      await clearChat();
      setMessages([]);
      setError(null);
    } catch (err) {
      setError('Failed to clear chat');
    }
  }

  const isOnline = systemStatus && systemStatus.ollama_running;
  const isEmpty = messages.length === 0;

  function renderSources(srcArray) {
    if (!srcArray || srcArray.length === 0) return null;
    return React.createElement('div', { className: 'message__sources' },
      React.createElement('span', { className: 'message__sources-label' }, 'Sources:'),
      React.createElement('div', { className: 'message__sources-list' },
        srcArray.map(function(src, idx) {
          return React.createElement('span', { key: idx, className: 'message__source-badge', title: 'Score: ' + ((src.score || 0) * 100).toFixed(1) + '%' },
            src.filename,
            src.chunk_index !== undefined ? React.createElement('span', { className: 'message__source-chunk' }, 'Chunk #' + (src.chunk_index + 1)) : null
          );
        })
      )
    );
  }

  function renderTypingIndicator() {
    return React.createElement('div', { className: 'message message--ai' },
      React.createElement('div', { className: 'message__avatar' }, 'AI'),
      React.createElement('div', { className: 'message__content' },
        React.createElement('div', { className: 'typing-indicator' },
          React.createElement('span', { className: 'typing-indicator__dot', key: 1 }),
          React.createElement('span', { className: 'typing-indicator__dot', key: 2 }),
          React.createElement('span', { className: 'typing-indicator__dot', key: 3 })
        )
      )
    );
  }

  return React.createElement('div', { className: 'chat-page' },
    React.createElement('section', { className: 'section' },
      React.createElement('div', { className: 'container' },
        React.createElement('div', { className: 'page-header' },
          React.createElement('h1', { className: 'page-title' }, 'AI Chat'),
          React.createElement('p', { className: 'page-subtitle' }, 'Ask questions about your uploaded documents. The AI assistant searches your documents to provide accurate answers.')
        ),
        React.createElement('div', { className: 'chat-page__content' },
          React.createElement('div', { className: 'chat-window' },
            React.createElement('div', { className: 'chat-window__header' },
              React.createElement('div', { className: 'chat-window__header-icon' },
                React.createElement('svg', { width: '20', height: '20', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: '2' },
                  React.createElement('path', { d: 'M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z' })
                )
              ),
              React.createElement('div', { className: 'chat-window__header-info' },
                React.createElement('h2', { className: 'chat-window__header-title' }, 'Knowledge Assistant'),
                React.createElement('p', { className: 'chat-window__header-status ' + (isOnline ? 'chat-window__header-status--online' : 'chat-window__header-status--offline') },
                  isOnline ? 'Online' : 'Offline'
                )
              ),
              React.createElement('button', { className: 'chat-window__clear-btn', onClick: handleClear, disabled: isLoading || isEmpty, title: 'Clear chat' },
                React.createElement('svg', { width: '16', height: '16', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: '2' },
                  React.createElement('polyline', { points: '3 6 5 6 21 6' }),
                  React.createElement('path', { d: 'M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2' })
                )
              )
            ),
            React.createElement('div', { className: 'chat-window__messages' },
              isEmpty ? React.createElement('div', { className: 'chat-window__empty' },
                React.createElement('div', { className: 'chat-window__empty-icon' },
                  React.createElement('svg', { width: '48', height: '48', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: '1.5' },
                    React.createElement('path', { d: 'M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z' })
                  )
                ),
                React.createElement('p', { className: 'chat-window__empty-text' }, 'Start a conversation by typing a message below.'),
                React.createElement('p', { className: 'chat-window__empty-hint' }, 'Upload documents first, then ask questions about them.')
              ) : messages.map(function(msg) {
                return React.createElement('div', { key: msg.id, className: 'message message--' + msg.type },
                  React.createElement('div', { className: 'message__avatar' },
                    msg.type === 'user' ? 'U' : msg.type === 'error' ? '!' : 'AI'
                  ),
                  React.createElement('div', { className: 'message__content' },
                    React.createElement('p', null, msg.text),
                    msg.type === 'ai' ? renderSources(msg.sources) : null,
                    React.createElement('span', { className: 'message__time' }, msg.time)
                  )
                );
              }).concat(isLoading ? [renderTypingIndicator()] : []),
              React.createElement('div', { ref: messagesEndRef })
            ),
            error ? React.createElement('div', { className: 'chat-window__error-bar' },
              React.createElement('svg', { width: '14', height: '14', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: '2' },
                React.createElement('circle', { cx: '12', cy: '12', r: '10' }),
                React.createElement('line', { x1: '12', y1: '8', x2: '12', y2: '12' }),
                React.createElement('line', { x1: '12', y1: '16', x2: '12.01', y2: '16' })
              ),
              React.createElement('span', null, error)
            ) : null,
            React.createElement('div', { className: 'chat-window__input' },
              React.createElement('input', { ref: inputRef, type: 'text', className: 'chat-window__input-field', placeholder: isOnline ? 'Type your message...' : 'AI service unavailable...', value: input, onChange: function(e) { setInput(e.target.value); }, onKeyDown: handleKey, disabled: isLoading || !isOnline }),
              React.createElement('button', { className: 'chat-window__send-btn', onClick: handleSend, disabled: !input.trim() || isLoading || !isOnline, 'aria-label': 'Send' },
                isLoading ? React.createElement('div', { className: 'chat-window__send-spinner' }) : React.createElement('svg', { width: '20', height: '20', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: '2' },
                  React.createElement('line', { x1: '22', y1: '2', x2: '11', y2: '13' }),
                  React.createElement('polygon', { points: '22 2 15 22 11 13 2 9 22 2' })
                )
              )
            )
          )
        )
      )
    )
  );
}

export default Chat;
