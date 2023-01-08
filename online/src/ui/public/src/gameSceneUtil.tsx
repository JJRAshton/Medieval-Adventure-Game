import { TILE_WIDTH } from "./constants";

/**
 * Util function to determine whether a click location is on the tile of the player
 * 
 * @param {*} clickX location of click relative to canvas
 * @param {*} clickY location of click relative to canvas
 * @param {*} player Character
 * @returns boolean
 */
export function onCharacter(clickX, clickY, player) {
    return player.x * TILE_WIDTH < clickX
            && clickX < (player.x + 1) * TILE_WIDTH
            && player.y * TILE_WIDTH < clickY
            && clickY < (player.y + 1) * TILE_WIDTH;
}
