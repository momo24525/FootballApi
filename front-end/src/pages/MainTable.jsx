import { useEffect, useState } from "react";
import "./MainTable.css";


function App() {
  const [matches, setMatches] = useState([]);

  const [teams, setTeams] = useState([]);
  const [seasons, setSeasons] = useState([]);

  const [team, setTeam] = useState("");
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

 /* const searchMatches = () => {
    const params = new URLSearchParams({
    });

    if (team !== "") {
      params.append("team", team);
    }
    
    if (matchday !== "") {
      params.append("matchday", matchday);
    }

    if (limit !== "") {
      params.append("limit", limit);
    }

    if (season !== "") {
      params.append("year", season);
    }

    fetch(`http://127.0.0.1:8000/matches/?${params}`)
      .then((res) => res.json())
      .then((data) => setMatches(data));
  };  versione fatta da me troppo da junior :<*/

  const searchMatches = () => {
    const filters = { team, matchday, limit, year: season };

    const params = new URLSearchParams(
      Object.entries(filters).filter(([, value]) => value !== "")
    );

    fetch(`http://127.0.0.1:8000/matches/?${params}`)
      .then((res) => res.json())
      .then((data) => setMatches(data));

  };

  return (
    <div className="container">

      <h1>Partite</h1>

      <div className="forms">

        <select
          value={team}
          onChange={(e) => setTeam(e.target.value)}
        >
          <option value="">Tutte le squadre</option>

          {teams.map((team) => (
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

          {seasons.map((seasonValue) => (
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


        <input
          type="number"
          value={limit}
          onChange={(e) => setLimit(e.target.value)}
          placeholder="Limite risultati"
        />


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
            {matches.map((m) => (
              <tr key={m.id}>
                <td>{m.home_team}</td>
                <td className="score">
                  {m.home_goals} - {m.away_goals}
                </td>
                <td>{m.away_team}</td>
                <td className="mdse">{m.matchday}</td>
                <td className="mdse">
                  {m.season} - {m.season + 1}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

    </div>
  );
}

export default App;