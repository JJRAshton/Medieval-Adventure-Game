import React from "react";
import Attack from "../attack/attack";
import { GameUISelection } from "../gameUISelection";
import Character from "../parsing/character";


type AttackButtonProps = {
    socket: WebSocket;
    selection: GameUISelection | null;
    setSelection;
    character: Character;
}

const ConfirmAttack = (props: AttackButtonProps) => {
    const { socket, selection, setSelection, character } = props;

    const confirmAttack = (): void => {
        if (!(selection instanceof Attack)) {
            return;
        }
        if (selection instanceof Attack && selection.confirmAttack()) {
            if (selection.target === null) {
                // Keep the IDE happy...
                throw new Error("Attack.confirmAttack() is broken")
            }
            socket.send(JSON.stringify({
                event: "attackRequest",
                playerID: character.id,
                enemyID: selection.target.id}));
            setSelection(null);
        }
    }
    return <div className="button" onClick={confirmAttack}>Confirm</div>;
} 

export default ConfirmAttack;