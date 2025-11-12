import { useState } from "react";

export default function App() {
  const [msg, setMsg] = useState("");

  async function send() {
    await fetch("/api/discord/send", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg || "Привет из фронта!" }),
    });
    alert("Сообщение отправлено!");
  }

  return (
    <div style={{ padding: 40, fontFamily: "sans-serif" }}>
      <h1>🎧 Discord Bot Panel</h1>
      <input
        value={msg}
        onChange={(e) => setMsg(e.target.value)}
        placeholder="Введите сообщение..."
        style={{ padding: "8px", marginRight: "8px" }}
      />
      <button onClick={send} style={{ padding: "8px 12px" }}>
        Отправить
      </button>
    </div>
  );
}
