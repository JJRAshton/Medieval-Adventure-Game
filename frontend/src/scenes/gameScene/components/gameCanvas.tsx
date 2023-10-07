import React, { useRef, useEffect, MutableRefObject, useState } from 'react'
import { TILE_WIDTH } from '../constants';

import { onCharacter } from "../gameSceneUtil";

import attackImageSrc from "../../../images/attackImage.png";
import loadInfoDisabldeSrc from "../../../images/loadInfoButtonDisabled.png";
import loadInfoSrc from "../../../images/loadInfoButton.png";
import loadInfoSelectedSrc from "../../../images/loadInfoButtonSelected.png";

import orc from "../../../images/orc.png";
import me from "../../../images/me.png";
import notMe from "../../../images/notMe.png";

import Attack from "../attack/attack";
import { GameUISelection } from '../gameUISelection';
import Movement from './movement';
import Character, { checkAttackable, getCharacterAtLocation, isCharacter } from '../parsing/character';

const ATTACK_IMAGE = new Image();
ATTACK_IMAGE.src = attackImageSrc;

const LOAD_INFO_DISABLED = new Image();
const LOAD_INFO = new Image();
const LOAD_INFO_SELECTED = new Image();
LOAD_INFO_DISABLED.src = loadInfoDisabldeSrc;
LOAD_INFO.src = loadInfoSrc;
LOAD_INFO_SELECTED.src = loadInfoSelectedSrc;

const ORC_IMAGE = new Image();
const ME_IMAGE = new Image();
const NOT_ME_IMAGE = new Image();

ORC_IMAGE.src = orc;
ME_IMAGE.src = me;
NOT_ME_IMAGE.src = notMe;

type CanvasProps = {
    mapSize: any;
    selection: GameUISelection | null;
    setSelection;
    characters: Record<string, Character>;
    character: Character;
    socket: WebSocket;
    onTurn: boolean;
    infoPanelSelection: Character | null;
    setInfoPanelSelection;
}

const Canvas = (props: CanvasProps) => {
  
    const { mapSize, selection, setSelection, characters, character, socket, onTurn, infoPanelSelection, setInfoPanelSelection } = props;
    const canvasRef: MutableRefObject<HTMLCanvasElement | null> = useRef(null);

    const [mouseX, setMouseX] = useState<number>(0);
    const [mouseY, setMouseY] = useState<number>(0);

    const handleMouseMove = (event) => {
        const rect = event.target.getBoundingClientRect();
        let [newX, newY] = [event.pageX - rect.left, event.pageY - rect.top];
        setMouseX(newX);
        setMouseY(newY);
        if (selection instanceof Movement) {
            if (0 < mouseX && mouseX < mapSize.mapWidth * TILE_WIDTH && 0 < mouseY && mouseY < mapSize.mapHeight * TILE_WIDTH) {
                selection.check(mouseX, mouseY);
            }
        }
    }

    let handleClick = (event) => {
        const rect = event.target.getBoundingClientRect();
        let [clickX, clickY] = [event.pageX - rect.left, event.pageY - rect.top];
        const [mapX, mapY]: [number, number] = [Math.floor(clickX / TILE_WIDTH), Math.floor(clickY / TILE_WIDTH)];
        const [x_rel, y_rel]: [number, number] = [clickX - mapX * TILE_WIDTH, clickY - mapY * TILE_WIDTH];
        const hover: Character | undefined = getCharacterAtLocation(mapX, mapY, characters);
        // Handling movement
        if (selection instanceof Movement) {
            socket.send(JSON.stringify(selection.getMoveRequest(character.id)));
            setSelection(null);
        }
        else if (isCharacter(hover) && onOpenSelection(x_rel, y_rel)) {
            setInfoPanelSelection(hover)
        }
        else {
            if (onTurn) {
                if (onCharacter(clickX, clickY, character)) {
                    console.log("Setting movement")
                    setSelection(new Movement(character.x, character.y));
                }
                else {
                    Object.values(characters).forEach(player => {
                        if (checkAttackable(character, player) && onCharacter(clickX, clickY, player)) {
                            if (selection instanceof Attack) {
                                selection.setOptions({target: player})
                            }
                            else {
                                setSelection(new Attack({target: player}));
                            }
                        }
                    })
                }
            }
        }
    }

    const onOpenSelection = (x_rel: number, y_rel: number) => {
        return x_rel > TILE_WIDTH * 0.6 && y_rel > TILE_WIDTH * 0.6;
    }

    const drawHealthBar = (character: Character, ctx: CanvasRenderingContext2D) => {
        ctx.fillStyle = "red";
        ctx.fillRect(character.x * TILE_WIDTH + 2, character.y * TILE_WIDTH + 2, TILE_WIDTH - 4, TILE_WIDTH / 8);
        ctx.fillStyle = "green";
        ctx.fillRect(character.x * TILE_WIDTH + 2, character.y * TILE_WIDTH + 2, (TILE_WIDTH - 4) * character.health / character.maxHealth, TILE_WIDTH / 8);
        ctx.fillStyle = "black";
        ctx.strokeRect(character.x * TILE_WIDTH + 2, character.y * TILE_WIDTH + 2, TILE_WIDTH - 4, TILE_WIDTH / 8);
    }

    const drawCanvas = (ctx: CanvasRenderingContext2D | null) => {
        //ctx.clearRect(0, 0, this.mapWidth * TILE_WIDTH, this.mapHeight * TILE_WIDTH);
        if (!ctx) {
            console.log("Canvas context was null");
            return;
        }
        ctx.fillStyle = 'rgb(109, 153, 87)';
        ctx.fillRect(0, 0, mapSize.mapWidth * TILE_WIDTH, mapSize.mapHeight * TILE_WIDTH);
    
        // Draw the move path if its not null
        if (selection instanceof Movement) {
            selection.draw(ctx);
        }
    
        // Draw the grid
        for (var i = 0; i < mapSize.mapWidth; i++) {
            for (var j = 0; j < mapSize.mapWidth; j++) {
                ctx.strokeRect(i * TILE_WIDTH, j * TILE_WIDTH, TILE_WIDTH, TILE_WIDTH);
            }
        }
    
        // Draw the characters
        Object.values(characters).forEach((aCharacter) => {
            let relevantImage: HTMLImageElement;
            if (aCharacter.team === character.team) {
                relevantImage = aCharacter.id === character.id ? ME_IMAGE : NOT_ME_IMAGE;
            }
            else {
                relevantImage = ORC_IMAGE;
            }
            ctx.drawImage(relevantImage, aCharacter.x * TILE_WIDTH, aCharacter.y * TILE_WIDTH, TILE_WIDTH, TILE_WIDTH);
            if (onTurn && checkAttackable(character, aCharacter)) {
                if (selection instanceof Attack 
                        && selection.target
                        && selection.target.id === aCharacter.id) {
                    ctx.drawImage(ATTACK_IMAGE, aCharacter.x * TILE_WIDTH + 2, aCharacter.y * TILE_WIDTH + 2, TILE_WIDTH - 4, TILE_WIDTH - 4);
                }
                else {
                    ctx.drawImage(ATTACK_IMAGE, aCharacter.x * TILE_WIDTH, aCharacter.y * TILE_WIDTH, TILE_WIDTH / 2, TILE_WIDTH / 2);
                }
            }
        });
    
        const [mapX, mapY]: [number, number] = [Math.floor(mouseX / TILE_WIDTH), Math.floor(mouseY / TILE_WIDTH)];
        const [x_rel, y_rel]: [number, number] = [mouseX - mapX * TILE_WIDTH, mouseY - mapY * TILE_WIDTH];
        const hover: Character | undefined = getCharacterAtLocation(mapX, mapY, characters);
        // Draw health bar on hovered character if necessary
        if (hover && isCharacter(hover)) {
            drawHealthBar(hover, ctx);
            let img: HTMLImageElement = onOpenSelection(x_rel, y_rel) ? LOAD_INFO : LOAD_INFO_DISABLED;
            ctx.drawImage(img, (mapX + 0.6) * TILE_WIDTH, (mapY + 0.6) * TILE_WIDTH, TILE_WIDTH * 0.4, TILE_WIDTH * 0.4);
        }
        if (infoPanelSelection !== null && isCharacter(infoPanelSelection)) {
            ctx.drawImage(LOAD_INFO_SELECTED, (infoPanelSelection.x + 0.6) * TILE_WIDTH, (infoPanelSelection.y + 0.6) * TILE_WIDTH, TILE_WIDTH * 0.4, TILE_WIDTH * 0.4);
        }
    
        // Draw outer boundary
        ctx.strokeRect(1, 1, mapSize.mapWidth * TILE_WIDTH - 2, mapSize.mapHeight * TILE_WIDTH - 2);
        ctx.beginPath();
    
        ctx.fill()
    }

    useEffect(() => {
      
        const canvas = canvasRef.current;
        if (canvas === null) {
            throw new Error("Critical error: Canvas ref was null");
        }

        canvas.width = TILE_WIDTH * mapSize.mapWidth;
        canvas.height = TILE_WIDTH * mapSize.mapHeight;

        const context = canvas.getContext('2d');
        let animationFrameId: number;

        const render = () => {
            drawCanvas(context);
            animationFrameId = window.requestAnimationFrame(render);
        }
        render();

        return () => {
            window.cancelAnimationFrame(animationFrameId);
        }
    }, [mouseX, mouseY, onTurn, characters, selection, infoPanelSelection]);
    
    return <canvas ref={canvasRef} onMouseMove={handleMouseMove} onClick={handleClick} width="100" height="400" style={{cursor: "pointer"}} />
}

export default Canvas;