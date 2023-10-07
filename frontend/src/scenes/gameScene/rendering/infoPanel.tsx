import React, { useState } from "react";
import Attack from "../attack/attack";
import GameUISelectionHandler from "../gameUISelection";
import AttackOptionInterface from "./availableAttacks";
import SelectionInfo from "./selectionInfo";
import StatInfo from "./statInfo";
import HealthBar from "./healthBar";
import Character, { checkAttackable } from "../parsing/character";

interface InfoPanelProps {
    selectionHandler: GameUISelectionHandler;
    socket: WebSocket;
    character: Character;
    characters: Record<string, Character>;
    onTurn: boolean;
    infoPanelSelection: Character | null;
}

const InfoPanel: React.FC<InfoPanelProps> = ({ selectionHandler, socket, character, characters, onTurn, infoPanelSelection }) => {

    // Used to display attack options. Has two modes, either returns min dist to any enemy (if
    // no target is selected), or min dist against the current attack target.
    const _getMinDistToTarget = () => {
        if (selectionHandler.selection instanceof Attack) {
            if (selectionHandler.selection.target !== null) {
                const target = selectionHandler.selection.target;
                return Math.max(Math.abs(character.x - target.x), Math.abs(character.y - target.y));
            }
        }
        let minDist = 100 // Big number
        Object.entries(characters).forEach(([id, target]) => {
            if (checkAttackable(character, target) && onTurn) {
                minDist = Math.min(minDist, Math.max(Math.abs(character.x - target.x), Math.abs(character.y - target.y)));
            }
        })
        return minDist;
    }

    /**
     * Used to display attack options. Returns either the currently selected attack option, or null
     * if there isn't one.
     */
    const _getCurrentSelectionOrNull = () => {
        if (selectionHandler.selection instanceof Attack) {
            if (selectionHandler.selection.attackType) {
                return selectionHandler.selection.attackType;
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
                <AttackOptionInterface player={character} minDistToTarget={_getMinDistToTarget()} currentSelectionOrNull={_getCurrentSelectionOrNull()} onTurn={onTurn} />
            </div>
            <div className="infoCompenent">
                <SelectionInfo infoPanelSelection={infoPanelSelection} />
            </div>
            <div className="infoComponent">
                <div className="button" onClick={() => selectionHandler.confirmAttack()}>Confirm</div>
            </div>
            <div className="infoComponent">
                <div className="button" onClick={()=>socket.send(JSON.stringify({event: "endTurnRequest"}))}>End Turn</div>
            </div>
        </div>
    )
}

export default InfoPanel;