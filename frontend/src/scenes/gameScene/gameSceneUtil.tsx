import { TILE_WIDTH } from "./constants";

/**
 * Util function to determine whether a click location is on the tile of the player
 */
export function onCharacter(clickX: any, clickY: any, player: any): boolean {
    return player.x * TILE_WIDTH < clickX
            && clickX < (player.x + 1) * TILE_WIDTH
            && player.y * TILE_WIDTH < clickY
            && clickY < (player.y + 1) * TILE_WIDTH;
}
