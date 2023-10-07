import React from "react";
import AttackOption, { AttackOptionInterfaceEntry } from "../attack/attackOption";
import Character, { checkAttackable } from "../parsing/character";
import Attack from "../attack/attack";

interface AttackOptionInterfaceProps {
    player: Character;
    currentSelectionOrNull: AttackOption | null;
    onTurn: boolean;
    currentAttackOptions: AttackOption[];
    selection;
    setSelection;
    character: Character;
    characters: Record<string, Character>;
}

const AttackOptionInterface: React.FC<AttackOptionInterfaceProps> = ({ player, currentSelectionOrNull, onTurn, currentAttackOptions, selection, setSelection, character, characters }) => {

    if (player && player.infoReceived) {
        let children: Array<JSX.Element> = [];
        currentAttackOptions.forEach((attack) => {
            children.push(<AttackOptionInterfaceEntry
                attackOption={attack}
                selection={selection}
                setSelection={setSelection}
                attackSelected={attack === currentSelectionOrNull}
                onTurn={onTurn}
                character={character}
                characters={characters} />)
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