import React from "react";
import Attack from "../attack/attack";
import AttackOption from "../attack/attackOption";
import GameState from "../gameState";
import GameUISelectionHandler from "../gameUISelection";
import AttackOptionInterface from "./availableAttacks";
import SelectionInfo from "./selectionInfo";
import StatInfo from "./statInfo";
import HealthBar from "./healthBar";

interface InfoPanelProps {
    selectionHandler: GameUISelectionHandler;
    socket: WebSocket;
    gameState: GameState;
}

const InfoPanel: React.FC<InfoPanelProps> = ({ selectionHandler, socket, gameState }) => {

    // Used to display attack options. Has two modes, either returns min dist to any enemy (if
    // no target is selected), or min dist against the current attack target.
    const _getMinDistToTarget = () => {
        if (selectionHandler.selection instanceof Attack) {
            if (selectionHandler.selection.target !== null) {
                const target = selectionHandler.selection.target;
                return Math.max(Math.abs(gameState.character.x - target.x), Math.abs(gameState.character.y - target.y));
            }
        }
        let minDist = 100 // Big number
        gameState.characters.forEach(target => {
            if (gameState.character.checkAttackable(target) && selectionHandler.onTurn) {
                minDist = Math.min(minDist, Math.max(Math.abs(gameState.character.x - target.x), Math.abs(gameState.character.y - target.y)));
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

    return (
         <div className="info">
            <div className="infoComponent" style={{width: "100%"}}><HealthBar character={gameState.character} /></div>
            <div className="infoComponent">
                <StatInfo player={gameState.character} />
            </div>
            <div className="attackList">
                <div>Attacks available</div>
                <AttackOptionInterface player={gameState.character} minDistToTarget={_getMinDistToTarget()} currentSelectionOrNull={_getCurrentSelectionOrNull()} />
            </div>
            <div className="infoCompenent">
                <SelectionInfo selectionHandler={selectionHandler} />
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