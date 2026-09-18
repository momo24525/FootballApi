import { useEffect, useState } from "react";
import "./h2hTable.css";


function App() {
  const [matches, setMatches] = useState([]);
  const [error, setError] = useState("");
  const [notFound, setNotFound] = useState("");
  const [teams, setTeams] = useState([]);
  const [seasons, setSeasons] = useState([]);

  const [team1, setTeam1] = useState("");
  const [team2, setTeam2] = useState("");
  const [limit, setLimit] = useState("");
  const [season, setSeason] = useState("");
  const [matchday, setMatchday] = useState("")



  // Carica squadre e stagioni dal DB
  useEffect(() => {
    fetch("http://127.0.0.1:8000/teams/")
      .then((res) => res.json())
      .then((data) => setTeams(data));

    fetch("http://127.0.0.1:8000/seasons/")
      .then((res) => res.json())
      .then((data) => setSeasons(data));
  }, []);


  const searchMatches = () => {

    if (team1 === "" || team2 === "") {
      setError("Seleziona entrambe le squadre per confrontarle.");
      return;
    }

    setError("");
    setNotFound("");


    const filters = { team1, team2, matchday, year: season };

    const params = new URLSearchParams(
      Object.entries(filters).filter(([, value]) => value !== "")
    );

    fetch(`http://127.0.0.1:8000/matches/headtohead/?${params}`)
      .then(async (res) => {
        if (!res.ok) {
          const errBody = await res.json().catch(() => null);
          throw new Error(errBody?.detail || "Errore durante la ricerca");
        }
        return res.json();
      })
      .then((data) => setMatches(data))
      .catch((err) => {
        setMatches([]); // svuota la lista precedente
        setNotFound(err.message);
        return
      });

  };

    const getDotClass = (isWinner, isDraw) => {
        if (isDraw) return "dot-draw";
        return isWinner ? "dot-win" : "dot-lose";
    };

  return (
    <div className="container">

    { /* <h1 className="title">Partite</h1>  */}

        {error && (
            <p className="error-message">
                <span className="error-icon">!</span>
                {error}
            </p>
        )}

      {notFound && (
        <p className="notfound-message">
          <span className="error-icon">!</span>
          {notFound}
        </p>
      )}


      <div className="forms">

        <select
          value={team1}
          onChange={(e) => setTeam1(e.target.value)}
        >
          <option value="">Team 1</option>

          {[...teams].sort((a, b) => a.name.localeCompare(b.name)).map((team) => (
            <option key={team.id} value={team.name}>
              {team.name}
            </option>
          ))}
        </select>

        <select
            value={team2}
            onChange={(e) => setTeam2(e.target.value)}
        >
            <option value="">Team 2</option>

            {[...teams].sort((a, b) => a.name.localeCompare(b.name)).map((team) => (
                <option key={team.id} value={team.name}>
                    {team.name}
                </option>
            ))}
        </select>


        <select
          value={season}
          onChange={(e) => setSeason(e.target.value)}
        >
          <option value="">Tutte le stagioni</option>

          {[...seasons]
            .sort((a, b) => b.year - a.year).map((seasonValue) => (
            <option key={seasonValue.id} value={seasonValue.year}>
              {seasonValue.year}-{seasonValue.year + 1}
            </option>
          ))}
        </select>


        <select
          value={matchday}
          onChange={(e) => setMatchday(e.target.value)}
        >
          <option value="">Tutti i turni</option>

          {Array.from({ length: 38 }, (_, i) => i + 1).map((number) => (
            <option key={number} value={number}>
              {number}
            </option>
          ))}
        </select>


        <button onClick={searchMatches}>
          Cerca
        </button>


      </div>

          
          
      

      <div className="table">
        <table className="maintable">
          <thead>
            <tr>
              <th>Casa</th>
              <th>Risultato</th>
              <th>Trasferta</th>
              <th>Giornata</th>
              <th>Stagione</th>
            </tr>
          </thead>

          <tbody>
            {matches.map((m) => {
                const isDraw = m.home_goals === m.away_goals;
                const homeWins = m.home_goals > m.away_goals;

                return (
                    <tr key={m.id}>
                        <td>
                            <span className={`status-dot ${getDotClass(homeWins, isDraw)}`}></span>
                            {m.home_team}
                        </td>
                        <td className="score">
                            {m.home_goals} - {m.away_goals}
                        </td>
                        <td>
                            <span className={`status-dot ${getDotClass(!homeWins, isDraw)}`}></span>
                            {m.away_team}
                        </td>
                        <td className="mdse">{m.matchday}</td>
                        <td className="mdse">
                            {m.season} - {m.season + 1}
                        </td>
                    </tr>
                );
            })}
          </tbody>
        </table>
      </div>

    </div>
  );
}

export default App;