import React from "react";
import Character from "../parsing/character";
import Renderable from "./renderable";

export default class StatInfo implements Renderable {
    private _player: Character;

    constructor(player: Character) {
        this._player = player
    }

    render(): JSX.Element {
        if (this._player.infoReceived) {
            let children: Array<JSX.Element> = [];
            this._player.stats.forEach((value, stat) => {
                children.push(<tr key={stat}><td>{stat}</td><td>{value}</td></tr>)
            });
            return <div className="stats"><table className="statTable"><tbody>{children}</tbody></table></div>
        }
        else {
            return <div className="stats">Could not load stats</div>
        }
    }
}