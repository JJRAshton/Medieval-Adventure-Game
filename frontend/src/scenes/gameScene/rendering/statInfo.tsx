import React from "react";

import Character from "../parsing/character";

interface StatInfoProps {
    player: Character;
}

const StatInfo: React.FC<StatInfoProps> = ({ player }) => {
    if (player.infoReceived) {
        let children: Array<JSX.Element> = [];
        Object.entries(player.stats).forEach(([stat, value]) => {
            children.push(<tr key={stat}><td>{stat}</td><td>{value}</td></tr>)
        });
        return <div className="stats"><table className="statTable"><tbody>{children}</tbody></table></div>
    }
    else {
        return <div className="stats">Could not load stats</div>
    }
}

export default StatInfo;

export { StatInfoProps }
