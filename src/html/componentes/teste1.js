export class LinkExemplo extends HTMLElement{
    
    constructor(){
        super();
        
        let tag_a = document.createElement('a');
        tag_a.href = './cabecalho/cabecalho.html';
        tag_a.innerText = 'Link para o Google';
        
        this.appendChild(tag_a);
    }
}

customElements.define('abelinha-linkexemplo', LinkExemplo);
