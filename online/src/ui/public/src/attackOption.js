import React from "react";

export default class AttackOption {

    constructor(weapon, name) {
        this.weapon = weapon;
        this.name = name;
        this.range = this.weapon.range;
    }

    renderAttackOptionElement() {
        return <tr key={this.name+"_"+this.weapon.name}><td>{this.name}</td><td><img src={this.weapon.imageSource} width={"32px"} height={"32px"}></img></td></tr>
    }
}