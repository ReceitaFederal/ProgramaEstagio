export class LinkExemplo extends HTMLElement{
    
    constructor(){
        super();
        
        for (let i = 0; i < 10; i++){

            let tag_a = document.createElement('a');
            tag_a.href = './cabecalho/cabecalho.html';
            tag_a.innerText = `Link${i}`;            
            this.appendChild(tag_a);

            let tag_br = document.createElement('br');
            this.appendChild(tag_br);
        }                
    }
}

customElements.define('abelinha-linkexemplo', LinkExemplo);
