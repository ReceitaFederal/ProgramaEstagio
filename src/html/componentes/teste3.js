export class LinkExemplo extends HTMLElement{
    
    constructor(){
        super();
        
        this.innerHTML = '<a href="./cabecalho/cabecalho.html">Link Cabeçalho</a>';                 
    }
}

customElements.define('abelinha-linkexemplo', LinkExemplo);
