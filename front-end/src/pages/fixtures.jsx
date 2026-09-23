import { useEffect, useState } from "react";
import "../styles/fixtures.css";
import "../styles/form.css";


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

        fetch(`http://127.0.0.1:8000/matches/fixtures/?${params}`)
            .then(async (res) => {
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

    const groupByMatchday = (matches) => {
        return matches.reduce((groups, m) => {
            const day = m.matchday;
            if (!groups[day]) {
                groups[day] = [];
            }
            groups[day].push(m);
            return groups;
        }, {});
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
                    {  /*   <p>Team</p> */}
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




                <button onClick={searchMatches}>
                    Cerca
                </button>

            </div>


            <div className="fixtures-list">
                {Object.entries(groupByMatchday(matches))
                    .sort(([dayA], [dayB]) => Number(dayA) - Number(dayB))
                    .map(([day, dayMatches]) => (
                        <div key={day} className="matchday-group">
                            <h3 className="matchday-title">Giornata {day}</h3>

                            {dayMatches.map((m) => (
                                <p key={m.id} className="fixture-row">
                                    <span className="fixture-team">{m.home_team}</span>
                                    <span className="fixture-score">
                                        {m.home_goals} - {m.away_goals}
                                    </span>
                                    <span className="fixture-team">{m.away_team}</span>
                                </p>
                            ))}
                        </div>
                    ))}
            </div>


        </div>
    );
}

export default App;