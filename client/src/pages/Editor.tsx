import Editor from '@monaco-editor/react';
import { useState } from 'react';

const TEMPLATE = `from codebots import Bot, State

class MyBot(Bot):
    name = "MyBot"
    color = "#FF6B35"
    author = "me"

    def on_turn(self, state: State) -> str:
        if state.enemy_distance <= 1:
            return "attack"
        if state.my_health < 30:
            return "heal"
        return "move_forward"
`;

export default function EditorPage() {
  const [code, setCode] = useState(TEMPLATE);
  const [status, setStatus] = useState('');

  const submit = async () => {
    setStatus('Submitting...');
    const res = await fetch('/api/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        bot_id: 'mybot_' + Date.now(),
        name: 'MyBot',
        author: 'guest',
        code,
      }),
    });
    const data = await res.json();
    setStatus(res.ok ? `✅ Submitted: ${data.bot_id}` : `❌ ${data.detail}`);
  };

  return (
    <div>
      <h2 className="text-3xl font-bold mb-4">Code Your Bot</h2>
      <Editor
        height="60vh"
        defaultLanguage="python"
        theme="vs-dark"
        value={code}
        onChange={(v) => setCode(v || '')}
        options={{ minimap: { enabled: false }, fontSize: 14 }}
      />
      <button
        onClick={submit}
        className="mt-4 bg-purple-600 hover:bg-purple-700 px-6 py-3 rounded-lg font-semibold"
      >
        Submit Bot
      </button>
      {status && <p className="mt-4 text-purple-200">{status}</p>}
    </div>
  );
}
