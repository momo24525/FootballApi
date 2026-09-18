import { useEffect, useState } from "react";
import "./MainTable.css";
import Chatbot from "../components/Chatbot";


function App() {
  const [matches, setMatches] = useState([]);

  const [teams, setTeams] = useState([]);
  const [seasons, setSeasons] = useState([]);
  const [notFound, setNotFound] = useState("");

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
    
    setNotFound("");

    fetch(`http://127.0.0.1:8000/matches/?${params}`)
      .then(async(res) => {
        if (!res.ok) {
          const errBody = await res.json().catch(() => null);
          throw new Error(errBody?.detail || "Errore durante la ricerca");
        }
        return res.json();
      })
      .then((data) => setMatches(data))
      .catch((err) => {
        setMatches([]);
        setNotFound(err.message);
      });

  };




  return (
    <div className="container">

      { /* <h1 className="title">Partite</h1>  */}

      {notFound && (
        <p className="notfound-message">
          <span className="error-icon">!</span>
          {notFound}
        </p>
      )}

      <div className="forms">

    { /*   <div className="filter"> */}
          <div>
     {  /*   <p>Team</p> */ }
          <select
            value={team}
            onChange={(e) => setTeam(e.target.value)}
          >
            <option value="">Tutte le squadre</option>

            {[...teams]
              .sort((a, b) => a.name.localeCompare(b.name))
              .map((team) => (
                <option key={team.id} value={team.name}>
                  {team.name}
                </option>
              ))}
          </select>
        </div>

        { /*   <div className="filter"> */}
        <div>
          {/* <p>Season</p> */}
          <select
            value={season}
            onChange={(e) => setSeason(e.target.value)}
          >
            <option value="">Tutte le stagioni</option>

            {[...seasons]
              .sort((a, b) => b.year - a.year)
              .map((seasonValue) => (
                <option key={seasonValue.id} value={seasonValue.year}>
                  {seasonValue.year}-{seasonValue.year + 1}
                </option>
              ))}
          </select>
        </div>

        { /*   <div className="filter"> */}
        <div>
          {/* <p>Matchday</p> */}
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
        </div>

        { /*   <div className="filter"> */}
        <div>
          {/* <p>Limit</p> */}
          <input
            type="number"
            value={limit}
            onChange={(e) => setLimit(e.target.value)}
            placeholder="Limite risultati"
          />
        </div>

           
        <button onClick={searchMatches}>
          Cerca
        </button>

      </div>

      {matches.length > 0 && <Chatbot matches={matches} />}


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