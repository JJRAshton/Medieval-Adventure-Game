import React, { useState, ChangeEvent } from 'react';

interface CharacterClassOption {
    value: string;
}

interface CharacterCustomistationProps {
    characterClassSelection: CharacterClassOption[];
    weaponSelection: Map<string, string[]>;
}

const CharacterCustomistationComponent: React.FC<CharacterCustomistationProps> = ({ characterClassSelection, weaponSelection }) => {
    const [selectedOption, setSelectedOption] = useState<string>('');
    const [selectedWeapon, setSelectedWeapon] = useState<string>('');
    const [characterName, setCharacterName] = useState<string>('');

    const handleNameChange = (event: ChangeEvent<HTMLInputElement>) => {
        setCharacterName(event.target.value);
    };

    const handleSelectedCharacterClassChange = (event: ChangeEvent<HTMLSelectElement>) => {
        setSelectedOption(event.target.value);
        setSelectedWeapon('')

    };

    const handleWeaponSelectionChange = (event: ChangeEvent<HTMLSelectElement>) => {
        setSelectedWeapon(event.target.value);
    };

    return (
        <form>
            <h2>Choose your character</h2>
            <div>
                <label>Enter a character name:</label>
                <input type="text"value={characterName} onChange={handleNameChange}placeholder="Enter character name:"/>
            </div>
            <div>
                <label>Choose your class:</label>
                <select value={selectedOption} onChange={handleSelectedCharacterClassChange}>
                    <option value="">Select a character class</option>
                    {characterClassSelection.map(characterClass => (
                    <option key={characterClass.value} value={characterClass.value}>{characterClass.value}</option>))}
                </select>
            </div>
            <div>
                <label>Choose a weapon:</label>
                <select value={selectedWeapon} onChange={handleWeaponSelectionChange}>
                    <option value="">Select a weapon</option>
                    {weaponSelection[selectedOption]?.map((weaponOption) => (
                    <option key={weaponOption} value={weaponOption}>{weaponOption}</option>))}
                </select>
            </div>
        </form>
    );
};

export { CharacterClassOption, CharacterCustomistationProps }

export default CharacterCustomistationComponent;
