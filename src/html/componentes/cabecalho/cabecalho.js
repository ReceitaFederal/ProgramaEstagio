export class Cabecalho extends HTMLElement{
    
    constructor(){
        super();
        console.log(`URL do cabeçalho.js: ${import.meta.url}`)
        fetch('./componentes/cabecalho/cabecalho.html').then(resultado => {
            resultado.text().then(texto_pagina => {
            
                let template = document.createElement('template');

                template.innerHTML = texto_pagina;

                this.appendChild(template.content.cloneNode(true));
            });
        });

        

    }
}
customElements.define('br-cabecalho', Cabecalho);