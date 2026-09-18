import { useState, useRef, useEffect } from "react";
import "./Chatbot.css";

function App({ matches }) {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]); // [{ role: "user" | "assistant", text: string }]
  const [chatLoading, setChatLoading] = useState(false);
  const messagesEndRef = useRef(null);


  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }, [messages]);

  useEffect(() => {
    setMessages([]);
    setQuestion("");
  }, [matches]);

  const askChat = () => {
    if (question.trim() === "") return;

    const userMessage = { role: "user", text: question };
    setMessages((prev) => [...prev, userMessage]);
    setQuestion("");
    setChatLoading(true);

    fetch("http://127.0.0.1:8000/chat/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question: userMessage.text,
        matches,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        setMessages((prev) => [...prev, { role: "assistant", text: data.response }]);
      })
      .catch(() => {
        setMessages((prev) => [
          ...prev,
          { role: "assistant", text: "Errore nella richiesta." },
        ]);
      })
      .finally(() => setChatLoading(false));
  };

  return (
    <div className="chatbox">
      <div className="chat-container">
        <div className="chat-messages">
          {messages.map((msg, i) => (
            <div key={i} className={`chat-bubble ${msg.role}`}>
              <p>{msg.text}</p>
            </div>
          ))}
          {chatLoading && (
            <div className="chat-bubble assistant loading">
              <p>...</p>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="chat-input">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask to AI"
            onKeyDown={(e) => e.key === "Enter" && askChat()}
          />
          <button onClick={askChat} disabled={chatLoading}>
            {chatLoading ? "..." : "➤"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;