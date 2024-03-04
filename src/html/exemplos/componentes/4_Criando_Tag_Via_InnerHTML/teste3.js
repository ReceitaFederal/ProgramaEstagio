export class LinkExemplo extends HTMLElement{
    
    constructor(){
        super();
        
        this.innerHTML = '<a href="../../componentes/cabecalho/cabecalho.html">Link Cabeçalho</a>';                 
    }
}

customElements.define('abelinha-linkexemplo', LinkExemplo);
