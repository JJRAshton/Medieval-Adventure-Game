import React from "react";
import AttackOption from "../attack/attackOption";
import Character from "../parsing/character";

interface AttackOptionInterfaceProps {
    player: Character;
    minDistToTarget: number;
    currentSelectionOrNull: AttackOption | null;
}

const AttackOptionInterface: React.FC<AttackOptionInterfaceProps> = ({ player, minDistToTarget, currentSelectionOrNull }) => {

    if (player && player.infoReceived) {
        let children: Array<JSX.Element> = [];
        player.attacks.forEach((attack) => {
            children.push(attack.renderAttackOptionElement(attack.range >= minDistToTarget, attack === currentSelectionOrNull))
        });
        return <ul className="attack"
            style={{
                listStyleType: "none",
                padding: 0,
                margin: 0,
            }}>{children}</ul>
    }
    else {
        return <div className="attack stats">Could not load attacks</div>
    }
}

export default AttackOptionInterface;

export { AttackOptionInterfaceProps };