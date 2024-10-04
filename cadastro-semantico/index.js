const inputFile = document.querySelector('#arquivo');
const imagemPreview = document.querySelector('.imagemPreview');
const imagem_div = document.querySelector('.imagem');

imagemPreview.textContent = 'Escolha uma imagem'; 

inputFile.addEventListener('change', function(e) {
    const inputTarget = e.target;
    const arquivo = inputTarget.files[0];

    if (arquivo) {
        const reader = new FileReader();

        reader.addEventListener('load', function(e) {
            const readerTarget = e.target;
            const img = document.createElement('img');

            img.src = readerTarget.result;
            img.classList.add('imagemPreview');

            img.style.boxShadow = '1px 1px 4px black';

            imagem_div.style.backgroundColor = 'white';
            imagem_div.style.border = 'none';

            imagemPreview.textContent = ''; 

            imagemPreview.appendChild(img);
        });

        reader.readAsDataURL(arquivo)
    }

    else {
        imagemPreview.textContent = 'Escolha uma imagem'; 
    }
})