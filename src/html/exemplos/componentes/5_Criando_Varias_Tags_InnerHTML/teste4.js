export class LinkExemplo extends HTMLElement{
    
    constructor(){
        super();

        let string_html = '';
        
        for (let i = 0; i < 10; i++){
            string_html += `<a href="../../componentes/cabecalho/cabecalho.html">Link Cabeçalho-${i}</a><br>`;                 
        }
        console.log (string_html);
        
        this.innerHTML = string_html;
    }
}

customElements.define('abelinha-linkexemplo', LinkExemplo);
