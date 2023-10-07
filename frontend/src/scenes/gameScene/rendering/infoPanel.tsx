import React, { useState } from "react";
import Attack from "../attack/attack";
import { GameUISelection } from "../gameUISelection";
import AttackOptionInterface from "./availableAttacks";
import SelectionInfo from "./selectionInfo";
import StatInfo from "./statInfo";
import HealthBar from "./healthBar";
import Character, { checkAttackable } from "../parsing/character";
import ConfirmAttack from "./confirmAttack";
import AttackOption from "../attack/attackOption";

interface InfoPanelProps {
    socket: WebSocket;
    character: Character;
    characters: Record<string, Character>;
    onTurn: boolean;
    infoPanelSelection: Character | null;
    selection: GameUISelection | null;
    setSelection;
    currentAttackOptions: AttackOption[];
}

const InfoPanel: React.FC<InfoPanelProps> = ({ socket, character, characters, onTurn, infoPanelSelection, selection, setSelection, currentAttackOptions }) => {

    /**
     * Used to display attack options. Returns either the currently selected attack option, or null
     * if there isn't one.
     */
    const _getCurrentSelectionOrNull = () => {
        if (selection instanceof Attack) {
            if (selection.attackType) {
                return selection.attackType;
            }
        }
        return null;
    }

    if (!character) {
        return <div>Character was undefined</div>
    }

    return (
         <div className="info">
            <div className="infoComponent" style={{width: "100%"}}>
                <HealthBar character={character} />
            </div>
            <div className="infoComponent">
                <StatInfo player={character} />
            </div>
            <div className="attackList">
                <div>Attacks available</div>
                <AttackOptionInterface player={character} currentSelectionOrNull={_getCurrentSelectionOrNull()} onTurn={onTurn} currentAttackOptions={currentAttackOptions} selection={selection} setSelection={setSelection} character={character} characters={characters} />
            </div>
            <div className="infoCompenent">
                <SelectionInfo infoPanelSelection={infoPanelSelection} />
            </div>
            <div className="infoComponent">
                <ConfirmAttack socket={socket} selection={selection} setSelection={setSelection} character={character} />
            </div>
            <div className="infoComponent">
                <div className="button" onClick={()=>socket.send(JSON.stringify({event: "endTurnRequest"}))}>End Turn</div>
            </div>
        </div>
    )
}

export default InfoPanel;