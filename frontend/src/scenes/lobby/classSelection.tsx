import React, { useState, ChangeEvent } from 'react';

interface CharacterClassOption {
    value: string;
}

interface CharacterCustomistationProps {
    classOptions: Record<string, string[]>;
    readied: boolean;
    characterName: string,
    setCharacterName,
    playerClass: string,
    setPlayerClass,
    weapon: string,
    setWeapon
}

const CharacterCustomistationComponent: React.FC<CharacterCustomistationProps> = (props: CharacterCustomistationProps) => {
    const { classOptions, readied, characterName, setCharacterName, playerClass, setPlayerClass, weapon, setWeapon } = props

    const handleNameChange = (event: ChangeEvent<HTMLInputElement>) => {
        setCharacterName(event.target.value);
    };

    const handleSelectedCharacterClassChange = (event: ChangeEvent<HTMLSelectElement>) => {
        setPlayerClass(event.target.value);
        setWeapon('')

    };

    const handleWeaponSelectionChange = (event: ChangeEvent<HTMLSelectElement>) => {
        setWeapon(event.target.value);
    };

    return (
        <form>
            <h2>{readied ? "Waiting for other players" : "Customise your character"}</h2>
            <div>
                <label>Enter a character name:</label>
                <input disabled={readied} type="text"value={characterName} onChange={handleNameChange}placeholder="Enter character name:"/>
            </div>
            <div>
                <label>Choose your class:</label>
                <select disabled={readied} value={playerClass} onChange={handleSelectedCharacterClassChange}>
                    <option value="">Select a character class</option>
                    {Object.keys(classOptions).map(characterClass => (
                    <option key={characterClass} value={characterClass}>{characterClass}</option>))}
                </select>
            </div>
            <div>
                <label>Choose a weapon:</label>
                <select disabled={readied} value={weapon} onChange={handleWeaponSelectionChange}>
                    <option value="">Select a weapon</option>
                    {classOptions[playerClass]?.map((weaponOption) => (
                    <option key={weaponOption} value={weaponOption}>{weaponOption}</option>))}
                </select>
            </div>
        </form>
    );
};

export { CharacterClassOption, CharacterCustomistationProps }

export default CharacterCustomistationComponent;
