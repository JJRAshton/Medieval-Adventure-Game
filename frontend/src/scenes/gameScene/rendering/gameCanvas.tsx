import React, { useRef, useEffect, MutableRefObject } from 'react'
import { TILE_WIDTH } from '../constants';
import Renderable from './renderable';

import { onCharacter } from "../gameSceneUtil";

import attackImageSrc from "../../../images/attackImage.png";
import loadInfoDisabldeSrc from "../../../images/loadInfoButtonDisabled.png";
import loadInfoSrc from "../../../images/loadInfoButton.png";
import loadInfoSelectedSrc from "../../../images/loadInfoButtonSelected.png";

import Attack from "../attack/attack";
import GameUISelectionHandler from '../gameUISelection';
import GameState from '../gameState';
import Movement from './movement';
import Character from '../parsing/character';

const ATTACK_IMAGE = new Image();
ATTACK_IMAGE.src = attackImageSrc;

const LOAD_INFO_DISABLED = new Image();
const LOAD_INFO = new Image();
const LOAD_INFO_SELECTED = new Image();
LOAD_INFO_DISABLED.src = loadInfoDisabldeSrc;
LOAD_INFO.src = loadInfoSrc;
LOAD_INFO_SELECTED.src = loadInfoSelectedSrc;

type CanvasProps = {
    draw: any;
    resize: any;
    handleClick: any;
    handleKeyPress: any;
    handleMouseMove: any;
    setStyle: any;
    getCanvasOffset: any;
}

let listenersAdded: boolean = false;

const Canvas = (props: CanvasProps) => {
  
  const { draw, resize, handleClick, handleKeyPress, handleMouseMove, setStyle, getCanvasOffset, ...rest } = props;
  const canvasRef: MutableRefObject<HTMLCanvasElement | null> = useRef(null);
  window.addEventListener("keyup", handleKeyPress);

  useEffect(() => {
    
    const canvas = canvasRef.current;
    if (canvas === null) {
        throw new Error("Critical error: Canvas ref was null");
    }

    resize(canvas);
    getCanvasOffset(canvas)

    if (!!!listenersAdded) {
        // Only want to add the event listeners once
        canvas.addEventListener("click", handleClick, false);
        canvas.addEventListener("mousemove", handleMouseMove, false);
        listenersAdded = true;
    }

    const context = canvas.getContext('2d');
    let animationFrameId: number;
    
    const render = () => {
      draw(context);
      animationFrameId = window.requestAnimationFrame(render);
    }
    render();
    
    return () => {
      window.cancelAnimationFrame(animationFrameId);
    }
  });
  
  return <canvas ref={canvasRef} width="100" height="400" style={setStyle()} {...rest}/>
}

export default class CanvasComponent implements Renderable {
    private _selectionHandler: GameUISelectionHandler;
    private _state: GameState;
    private _socket: WebSocket;

    private _mouseX: number;
    private _mouseY: number;
    private canvasOffset: [number, number];

    constructor(selectionHandler: GameUISelectionHandler, socket: WebSocket, gameState: GameState) {
        this._selectionHandler = selectionHandler;
        this._socket = socket;
        this._state = gameState;
        [this._mouseX, this._mouseY] = [0, 0];
    }

    render(): JSX.Element {
        return <Canvas
            // Passing in the various call backs as props
            draw={(ctx: CanvasRenderingContext2D) => {this.drawCanvas(ctx)}}
            resize={(canvas: HTMLCanvasElement) => {this.resize(canvas)}}
            handleClick={this.handleClick.bind(this)}
            handleMouseMove={this.handleMouseMove.bind(this)}
            handleKeyPress={this.handleKeyPress.bind(this)}
            setStyle={this.setStyle}
            getCanvasOffset={this.getCanvasOffset.bind(this)}></Canvas>
    }

    setStyle(): any {
        return {cursor: "pointer"}
    }

    getCanvasOffset(canvas: HTMLCanvasElement) {
        this.canvasOffset = [canvas.offsetLeft + canvas.clientLeft, canvas.offsetTop + canvas.clientTop];
    }

    translateMouseCoords(posX: number, posY: number): [number, number] {
        return [posX - this.canvasOffset[0], posY - this.canvasOffset[1]];
    }

    // Drawing to the canvas, passed in as a callback
    drawCanvas(ctx: CanvasRenderingContext2D): void {
        //ctx.clearRect(0, 0, this.mapWidth * TILE_WIDTH, this.mapHeight * TILE_WIDTH);
        ctx.fillStyle = 'rgb(109, 153, 87)';
        ctx.fillRect(0, 0, this._state.mapState.mapWidth * TILE_WIDTH, this._state.mapState.mapHeight * TILE_WIDTH);

        // Draw the move path if its not null
        if (this._selectionHandler.selection instanceof Movement) {
            this._selectionHandler.selection.draw(ctx);
        }

        // Draw the grid
        for (var i = 0; i < this._state.mapState.mapWidth; i++) {
            for (var j = 0; j < this._state.mapState.mapWidth; j++) {
                ctx.strokeRect(i * TILE_WIDTH, j * TILE_WIDTH, TILE_WIDTH, TILE_WIDTH);
            }
        }

        // Draw the characters
        this._state.characters.forEach((character) => {
            if (character.imageLoaded) {
                ctx.drawImage(character.image, character.x * TILE_WIDTH, character.y * TILE_WIDTH, TILE_WIDTH, TILE_WIDTH);
                if (this._selectionHandler.onTurn && this._state.character.checkAttackable(character)) {
                    if (this._selectionHandler.selection instanceof Attack 
                            && this._selectionHandler.selection.target
                            && this._selectionHandler.selection.target.id === character.id) {
                        ctx.drawImage(ATTACK_IMAGE, character.x * TILE_WIDTH + 2, character.y * TILE_WIDTH + 2, TILE_WIDTH - 4, TILE_WIDTH - 4);
                        // this._drawHealthBar(character, ctx)
                    }
                    else {
                        ctx.drawImage(ATTACK_IMAGE, character.x * TILE_WIDTH, character.y * TILE_WIDTH, TILE_WIDTH / 2, TILE_WIDTH / 2);
                    }
                }
            }
        }, this);

        const mapX: number = Math.floor(this._mouseX / TILE_WIDTH);
        const mapY: number = Math.floor(this._mouseY / TILE_WIDTH);
        const x_rel: number = this._mouseX - mapX * TILE_WIDTH;
        const y_rel: number = this._mouseY - mapY * TILE_WIDTH;
        const hover: Character | null = this._state.mapState.get(mapX, mapY);
        // Draw health bar on hovered character if necessary
        if (hover instanceof Character) {
            this._drawHealthBar(hover, ctx);
            let img: HTMLImageElement = this._onOpenSelection(x_rel, y_rel) ? LOAD_INFO : LOAD_INFO_DISABLED;
            ctx.drawImage(img, (mapX + 0.6) * TILE_WIDTH, (mapY + 0.6) * TILE_WIDTH, TILE_WIDTH * 0.4, TILE_WIDTH * 0.4);
        }
        let informationSelection = this._selectionHandler.getInformationPanelSelection() ;
        if (informationSelection instanceof Character) {
            ctx.drawImage(LOAD_INFO_SELECTED, (informationSelection.x + 0.6) * TILE_WIDTH, (informationSelection.y + 0.6) * TILE_WIDTH, TILE_WIDTH * 0.4, TILE_WIDTH * 0.4);
        }

        // Draw outer boundary
        ctx.strokeRect(1, 1, this._state.mapState.mapWidth * TILE_WIDTH - 2, this._state.mapState.mapHeight * TILE_WIDTH - 2);
        ctx.beginPath();
    
        ctx.fill()
    }
    private _onOpenSelection(x_rel: number, y_rel: number): boolean {
        return x_rel > TILE_WIDTH * 0.6 && y_rel > TILE_WIDTH * 0.6;
    }

    private _drawHealthBar(character: Character, ctx: CanvasRenderingContext2D) {
        ctx.fillStyle = "red";
        ctx.fillRect(character.x * TILE_WIDTH + 2, character.y * TILE_WIDTH + 2, TILE_WIDTH - 4, TILE_WIDTH / 8);
        ctx.fillStyle = "green";
        ctx.fillRect(character.x * TILE_WIDTH + 2, character.y * TILE_WIDTH + 2, (TILE_WIDTH - 4) * character.health / character.maxHealth, TILE_WIDTH / 8);
        ctx.fillStyle = "black";
        ctx.strokeRect(character.x * TILE_WIDTH + 2, character.y * TILE_WIDTH + 2, TILE_WIDTH - 4, TILE_WIDTH / 8);
    }

    // Handling click events in the canvas, passed in as a callback
    handleClick(event: MouseEvent): void {
        //let clickX: number, clickY: number;
        let [clickX, clickY] = this.translateMouseCoords(event.pageX, event.pageY);
        const mapX: number = Math.floor(this._mouseX / TILE_WIDTH);
        const mapY: number = Math.floor(this._mouseY / TILE_WIDTH);
        const x_rel: number = this._mouseX - mapX * TILE_WIDTH;
        const y_rel: number = this._mouseY - mapY * TILE_WIDTH;
        const hover: Character | null = this._state.mapState.get(mapX, mapY);
        // Handling movement
        if (this._selectionHandler.selection instanceof Movement) {
            this._socket.send(JSON.stringify(this._selectionHandler.selection.getMoveRequest(this._state.character.id)));
            this._selectionHandler.reset();
        }
        else if (hover instanceof Character && this._onOpenSelection(x_rel, y_rel)) {
            this._selectionHandler.setInformationPanel(hover)
        }
        else {
            if (this._selectionHandler.onTurn) {
                if (onCharacter(clickX, clickY, this._state.character)) {
                    this._selectionHandler.setMovement(new Movement(this._state.character.x, this._state.character.y));
                }
                else {
                    this._state.characters.forEach(player => {
                        // Inefficient way of finding players, they should probably be stored in 2d array
                        if (this._state.character.checkAttackable(player) && onCharacter(clickX, clickY, player)) {
                            this._selectionHandler.setAttackOptions({target: player})
                        }
                    }, this)
                }
            }
        }
    }

    // Resizes the canvas, for some reason this has to be passed as a callback
    resize(canvas: HTMLCanvasElement) {
        canvas.width = TILE_WIDTH * this._state.mapState.mapWidth;
        canvas.height = TILE_WIDTH * this._state.mapState.mapHeight;
    }

    handleKeyPress(event: { keyCode: number; }): void {
        switch (event.keyCode) {
            // Handling wasd and arrow keys, probably wont be used now
            case 38:
            case 87:
                // Up
                console.log("up");
                break;
            case 40:
            case 83:
                // Down
                console.log("down");
                break;
            case 37:
            case 65:
                // Left
                console.log("left");
                break;
            case 39:
            case 68:
                // Right
                console.log("right");
                break;
            default:
                break;
        }
    }

    // Handling mouse movements inside the canvas
    handleMouseMove(event: MouseEvent): void {
        [this._mouseX, this._mouseY] = this.translateMouseCoords(event.pageX, event.pageY);

        this._selectionHandler.handleMouseMove(this._mouseX, this._mouseY, this._state.mapState.mapWidth, this._state.mapState.mapHeight);
    }
}