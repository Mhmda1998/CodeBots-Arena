import { Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import Editor from './pages/Editor';
import Leaderboard from './pages/Leaderboard';
import Battle from './pages/Battle';

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white">
      <nav className="border-b border-purple-500/30 p-4 flex gap-6">
        <Link to="/" className="text-2xl font-bold">🤖 CodeBots Arena</Link>
        <Link to="/editor" className="hover:text-purple-300">Editor</Link>
        <Link to="/leaderboard" className="hover:text-purple-300">Leaderboard</Link>
        <Link to="/battle" className="hover:text-purple-300">Battle</Link>
      </nav>
      <main className="container mx-auto p-6">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/editor" element={<Editor />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/battle" element={<Battle />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
