import React, { useRef, useEffect, MutableRefObject, useState } from 'react'
import { TILE_WIDTH } from '../constants';

import { onCharacter } from "../gameSceneUtil";

import attackImageSrc from "../../../images/attackImage.png";
import loadInfoDisabldeSrc from "../../../images/loadInfoButtonDisabled.png";
import loadInfoSrc from "../../../images/loadInfoButton.png";
import loadInfoSelectedSrc from "../../../images/loadInfoButtonSelected.png";

import Attack from "../attack/attack";
import GameUISelectionHandler from '../gameUISelection';
import Movement from './movement';
import Character, { checkAttackable } from '../parsing/character';
import MapState from '../MapState';

const ATTACK_IMAGE = new Image();
ATTACK_IMAGE.src = attackImageSrc;

const LOAD_INFO_DISABLED = new Image();
const LOAD_INFO = new Image();
const LOAD_INFO_SELECTED = new Image();
LOAD_INFO_DISABLED.src = loadInfoDisabldeSrc;
LOAD_INFO.src = loadInfoSrc;
LOAD_INFO_SELECTED.src = loadInfoSelectedSrc;

type CanvasProps = {
    mapState: MapState;
    selectionHandler: GameUISelectionHandler;
    characters: Map<string, Character>;
    character: Character;
    socket: WebSocket;
}

const Canvas = (props: CanvasProps) => {
  
    const { mapState, selectionHandler, characters, character, socket, ...rest } = props;
    const canvasRef: MutableRefObject<HTMLCanvasElement | null> = useRef(null);
  
    const [mouseX, setMouseX] = useState<number>(0);
    const [mouseY, setMouseY] = useState<number>(0);

    const [canvasOffset, setCanvasOffset] = useState<any>([0, 0]);

    const translateMouseCoords = (posX: number, posY: number) => {
        return [posX - canvasOffset[0], posY - canvasOffset[1]];
    }

    const handleMouseMove = (event: MouseEvent) => {
        const [newX, newY] = translateMouseCoords(event.pageX, event.pageY);
        setMouseX(newX);
        setMouseY(newY);
    
        selectionHandler.handleMouseMove(mouseX, mouseY, mapState.mapWidth, mapState.mapHeight);
    }

    const setStyle = () => {
        return {cursor: "pointer"}
    }

    const handleClick = (event: MouseEvent) => {
        let [clickX, clickY] = translateMouseCoords(event.pageX, event.pageY);
        const [mapX, mapY]: [number, number] = [Math.floor(mouseX / TILE_WIDTH), Math.floor(mouseY / TILE_WIDTH)];
        const [x_rel, y_rel]: [number, number] = [mouseX - mapX * TILE_WIDTH, mouseY - mapY * TILE_WIDTH];
        const hover: Character | null = mapState.get(mapX, mapY);
        // Handling movement
        if (selectionHandler.selection instanceof Movement) {
            socket.send(JSON.stringify(selectionHandler.selection.getMoveRequest(character.id)));
            selectionHandler.reset();
        }
        else if (hover instanceof Character && onOpenSelection(x_rel, y_rel)) {
            selectionHandler.setInformationPanel(hover)
        }
        else {
            if (selectionHandler.onTurn) {
                if (onCharacter(clickX, clickY, character)) {
                    selectionHandler.setMovement(new Movement(character.x, character.y));
                }
                else {
                    characters.forEach(player => {
                        // Inefficient way of finding players, they should probably be stored in 2d array
                        if (checkAttackable(character, player) && onCharacter(clickX, clickY, player)) {
                            selectionHandler.setAttackOptions({target: player})
                        }
                    }, this)
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
    
    const drawCanvas = (ctx: CanvasRenderingContext2D | null, mapState: MapState, selectionHandler: GameUISelectionHandler, characters: Map<string, Character>, mouseX: number, mouseY: number) => {
        //ctx.clearRect(0, 0, this.mapWidth * TILE_WIDTH, this.mapHeight * TILE_WIDTH);
        if (!ctx) {
            console.log("Canvas context was null");
            return;
        }
        ctx.fillStyle = 'rgb(109, 153, 87)';
        ctx.fillRect(0, 0, mapState.mapWidth * TILE_WIDTH, mapState.mapHeight * TILE_WIDTH);
    
        // Draw the move path if its not null
        if (selectionHandler.selection instanceof Movement) {
            selectionHandler.selection.draw(ctx);
        }
    
        // Draw the grid
        for (var i = 0; i < mapState.mapWidth; i++) {
            for (var j = 0; j < mapState.mapWidth; j++) {
                ctx.strokeRect(i * TILE_WIDTH, j * TILE_WIDTH, TILE_WIDTH, TILE_WIDTH);
            }
        }
    
        // Draw the characters
        characters.forEach((character) => {
            if (character.imageLoaded) {
                ctx.drawImage(character.image, character.x * TILE_WIDTH, character.y * TILE_WIDTH, TILE_WIDTH, TILE_WIDTH);
                if (selectionHandler.onTurn && checkAttackable(character, character)) {
                    if (selectionHandler.selection instanceof Attack 
                            && selectionHandler.selection.target
                            && selectionHandler.selection.target.id === character.id) {
                        ctx.drawImage(ATTACK_IMAGE, character.x * TILE_WIDTH + 2, character.y * TILE_WIDTH + 2, TILE_WIDTH - 4, TILE_WIDTH - 4);
                        // this._drawHealthBar(character, ctx)
                    }
                    else {
                        ctx.drawImage(ATTACK_IMAGE, character.x * TILE_WIDTH, character.y * TILE_WIDTH, TILE_WIDTH / 2, TILE_WIDTH / 2);
                    }
                }
            }
        }, this);
    
        const [mapX, mapY]: [number, number] = [Math.floor(mouseX / TILE_WIDTH), Math.floor(mouseY / TILE_WIDTH)];
        const [x_rel, y_rel]: [number, number] = [mouseX - mapX * TILE_WIDTH, mouseY - mapY * TILE_WIDTH];
        const hover: Character | null = mapState.get(mapX, mapY);
        // Draw health bar on hovered character if necessary
        if (hover instanceof Character) {
            drawHealthBar(hover, ctx);
            let img: HTMLImageElement = onOpenSelection(x_rel, y_rel) ? LOAD_INFO : LOAD_INFO_DISABLED;
            ctx.drawImage(img, (mapX + 0.6) * TILE_WIDTH, (mapY + 0.6) * TILE_WIDTH, TILE_WIDTH * 0.4, TILE_WIDTH * 0.4);
        }
        let informationSelection = selectionHandler.getInformationPanelSelection() ;
        if (informationSelection instanceof Character) {
            ctx.drawImage(LOAD_INFO_SELECTED, (informationSelection.x + 0.6) * TILE_WIDTH, (informationSelection.y + 0.6) * TILE_WIDTH, TILE_WIDTH * 0.4, TILE_WIDTH * 0.4);
        }
    
        // Draw outer boundary
        ctx.strokeRect(1, 1, mapState.mapWidth * TILE_WIDTH - 2, mapState.mapHeight * TILE_WIDTH - 2);
        ctx.beginPath();
    
        ctx.fill()
    }

    useEffect(() => {
      
        const canvas = canvasRef.current;
        if (canvas === null) {
            throw new Error("Critical error: Canvas ref was null");
        }
    
        canvas.width = TILE_WIDTH * mapState.mapWidth;
        canvas.height = TILE_WIDTH * mapState.mapHeight;
        setCanvasOffset([canvas.offsetLeft + canvas.clientLeft, canvas.offsetTop + canvas.clientTop]);
    
        canvas.addEventListener("click", handleClick, false);
        canvas.addEventListener("mousemove", handleMouseMove, false);

        const context = canvas.getContext('2d');
        let animationFrameId: number;
        
        const render = () => {
            drawCanvas(context, mapState, selectionHandler, characters, mouseX, mouseY);
            animationFrameId = window.requestAnimationFrame(render);
        }
        render();
        
        return () => {
            window.cancelAnimationFrame(animationFrameId);
        }
    }, []);
    
    return <canvas ref={canvasRef} width="100" height="400" style={setStyle()} {...rest}/>
}

export default Canvas;