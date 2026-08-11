import { useEffect, useState } from 'react';

interface Entry {
  rank: number;
  name: string;
  author: string;
  rating: number;
  rank_label: string;
  wins: number;
  losses: number;
  matches: number;
}

export default function Leaderboard() {
  const [entries, setEntries] = useState<Entry[]>([]);

  useEffect(() => {
    fetch('/api/leaderboard')
      .then((r) => r.json())
      .then(setEntries)
      .catch(() => setEntries([]));
  }, []);

  return (
    <div>
      <h2 className="text-3xl font-bold mb-6">🏆 Global Leaderboard</h2>
      <table className="w-full text-left">
        <thead className="border-b border-purple-500/30">
          <tr>
            <th className="py-2">#</th>
            <th>Bot</th>
            <th>Author</th>
            <th>Rating</th>
            <th>Tier</th>
            <th>W/L</th>
          </tr>
        </thead>
        <tbody>
          {entries.map((e) => (
            <tr key={e.rank} className="border-b border-purple-500/10 hover:bg-purple-500/10">
              <td className="py-2">{e.rank}</td>
              <td className="font-semibold">{e.name}</td>
              <td className="text-purple-200">{e.author}</td>
              <td>{e.rating}</td>
              <td><span className="px-2 py-1 rounded bg-purple-700/40 text-xs">{e.rank_label}</span></td>
              <td>{e.wins}/{e.losses}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
