import React from "react";

import Character from "../parsing/character";

interface HealthBarProps {
    character: Character;
}

const HealthBar: React.FC<HealthBarProps> = ({ character }) => {

    return <div className="healthBar" style={{
            position: "relative",
            width: "100%",
            backgroundColor: "red",
            height: "1.2em",
            border: "medium solid"}}>
            <div style={{
                width: Math.floor(100 * character.health / character.maxHealth)+"%",
                height: "100%",
                background: "green",
                borderRadius: "0px",
                }}/>
            <div style={{
                position: "absolute",
                top: "50%",
                left: "50%",
                transform: "translate(-50%, -50%)",
                fontSize: "1em",
                borderRadius: "0px",
                }}>{character.health}/{character.maxHealth}</div>
        </div>
};

export default HealthBar

export { HealthBarProps }