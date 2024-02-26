export class OlaMundo extends HTMLElement{
    
    constructor(){
        super();
        this.innerText = 'Olá mundo!';              
    }
}
console.log ("vai definir o custom element");
customElements.define('abelinha-olamundo', OlaMundo);
console.log ("Definiu o custom element");