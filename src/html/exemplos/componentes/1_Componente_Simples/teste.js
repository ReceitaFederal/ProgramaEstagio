export class OlaMundo extends HTMLElement{
    
    constructor(){
        super();
        this.innerText = 'Olá mundo!';              
    }
}
customElements.define('abelinha-olamundo', OlaMundo);