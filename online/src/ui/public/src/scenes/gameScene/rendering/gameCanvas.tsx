import React, { useRef, useEffect, MutableRefObject } from 'react'
import { TILE_WIDTH } from '../constants';
import Renderable from './renderable';

import { onCharacter } from "../gameSceneUtil";

import attackImageSrc from "../../../images/attackImage.png";

import Attack from "../attack/attack";
import GameUISelectionHandler from '../gameUISelection';
import GameState from '../gameState';
import Movement from './movement';

const ATTACK_IMAGE = new Image();
ATTACK_IMAGE.src = attackImageSrc;

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

export default class CanvasComponent extends Renderable {
    private _selectionHandler: GameUISelectionHandler;
    private _state: GameState;
    private _socket: WebSocket;

    private _mouseX: number;
    private _mouseY: number;
    private canvasOffset: [number, number];

    constructor(selectionHandler: GameUISelectionHandler, socket: WebSocket, gameState: GameState) {
        super();
        this._selectionHandler = selectionHandler;
        this._socket = socket;
        this._state = gameState;
        this._mouseX, this._mouseY = 0, 0;
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

    translateMouseCoords(posX: number, posY: number) {
        return [posX - this.canvasOffset[0], posY - this.canvasOffset[1]];
    }

    // Drawing to the canvas, passed in as a callback
    drawCanvas(ctx: CanvasRenderingContext2D): void {

        //ctx.clearRect(0, 0, this.mapWidth * TILE_WIDTH, this.mapHeight * TILE_WIDTH);
        ctx.fillStyle = 'rgb(109, 153, 87)';
        ctx.fillRect(0, 0, this._state.mapWidth * TILE_WIDTH, this._state.mapHeight * TILE_WIDTH);

        // Draw the move path if its not null
        if (this._selectionHandler.selection instanceof Movement) {
            this._selectionHandler.selection.draw(ctx);
        }

        // Draw the grid
        for (var i = 0; i < this._state.mapWidth; i++) {
            for (var j = 0; j < this._state.mapWidth; j++) {
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
                    }
                    else {
                        ctx.drawImage(ATTACK_IMAGE, character.x * TILE_WIDTH, character.y * TILE_WIDTH, TILE_WIDTH / 2, TILE_WIDTH / 2);
                    }
                }
            }
        }, this);

        // Draw outer boundary
        ctx.strokeRect(1, 1, this._state.mapWidth * TILE_WIDTH - 2, this._state.mapHeight * TILE_WIDTH - 2);
        ctx.beginPath();
    
        ctx.fill()
    }

    // Handling click events in the canvas, passed in as a callback
    handleClick(event: MouseEvent): void {
        let clickX: number, clickY: number;
        [clickX, clickY] = this.translateMouseCoords(event.pageX, event.pageY);
        // Handling movement
        if (this._selectionHandler.selection instanceof Movement) {
            this._socket.send(JSON.stringify(this._selectionHandler.selection.getMoveRequest(this._state.character.id)));
            this._selectionHandler.reset();
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
        canvas.width = TILE_WIDTH * this._state.mapWidth;
        canvas.height = TILE_WIDTH * this._state.mapHeight;
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
        this._selectionHandler.handleMouseMove(this._mouseX, this._mouseY, this._state.mapWidth, this._state.mapHeight);
    }
}