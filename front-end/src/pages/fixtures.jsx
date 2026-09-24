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
    const [matchday, setMatchday] = useState("");  
    const [matchdays, setMatchdays] = useState([]);




    // Carica squadre e stagioni dal DB
    useEffect(() => {
        fetch("http://127.0.0.1:8000/teams/?year=2026")
            .then((res) => res.json())
            .then((data) => setTeams(data));
    }, []);

    // lista dei matchday
    useEffect(() => {
        const params = new URLSearchParams({ played: "false" });
        if (season !== "") params.append("year", season);

        fetch(`http://127.0.0.1:8000/matches/matchdays?${params}`)
            .then((res) => res.json())
            .then((data) => {
                setMatchdays(data);
                setMatchday("");
            });
    }, [season]);

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


    const groupBy = (items, key) =>
        items.reduce((groups, item) => {
            const value = item[key] ?? "Data da definire";
            (groups[value] ??= []).push(item);
            return groups;
        }, {});

    const formatDate = (iso) =>
        iso === "Data da definire"
            ? iso
            : new Date(iso).toLocaleDateString("it-IT", {
                weekday: "long",
                day: "numeric",
                month: "long",
            });



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
                        {matchdays.map((number) => (
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
                {Object.entries(groupBy(matches, "matchday"))
                    .sort(([a], [b]) => Number(a) - Number(b))
                    .map(([day, dayMatches]) => (
                        <div key={day} className="matchday-group">
                            <h3 className="matchday-title">Giornata {day}</h3>

                            {Object.entries(groupBy(dayMatches, "match_date"))
                                .sort(([a], [b]) => a.localeCompare(b))
                                .map(([date, dateMatches]) => (
                                    <div key={date}>
                                        <h4 className="date-title">{formatDate(date)}</h4>
                                        <div className="fixtures-grid">
                                            {dateMatches.map((m) => (
                                                <div key={m.id} className="fixture-card">
                                                    <span className="fixture-team">{m.home_team}</span>
                                                    <span className="fixture-score">vs</span>
                                                    <span className="fixture-team">{m.away_team}</span>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                ))}
                        </div>
                    ))}
            </div>


        </div>
    );
}

export default App;