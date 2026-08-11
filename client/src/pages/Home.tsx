export default function Home() {
  return (
    <div className="text-center py-20">
      <h1 className="text-6xl font-bold mb-6">🤖⚔️ CodeBots Arena</h1>
      <p className="text-2xl text-purple-200 mb-8">
        Write your bot. Watch it fight. Climb the global leaderboard.
      </p>
      <div className="flex gap-4 justify-center">
        <a href="/editor" className="bg-purple-600 hover:bg-purple-700 px-8 py-4 rounded-lg text-lg font-semibold">
          Start Coding
        </a>
        <a href="/leaderboard" className="border border-purple-400 hover:bg-purple-400/10 px-8 py-4 rounded-lg text-lg font-semibold">
          View Leaderboard
        </a>
      </div>
    </div>
  );
}
