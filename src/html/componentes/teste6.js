export class LinkExemplo extends HTMLElement{
    
    constructor(){
        super();                

        fetch('./cabecalho/cabecalho.html')
          .then( resposta =>
            resposta.text().then( texto =>
              this.innerHTML = texto
        ));
    }
}

customElements.define('abelinha-linkexemplo', LinkExemplo);
