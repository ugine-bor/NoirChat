document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('faviconCanvas');
    const ctx = canvas.getContext('2d');
    const faviconLink = document.getElementById('favicon');
    const size = 16;

    function generateRandomFavicon() {
        ctx.fillStyle = '#000';
        ctx.fillRect(0, 0, size, size);

        const randomNumber = Math.floor(Math.random() * 100);

        ctx.fillStyle = '#fff';
        ctx.font = 'bold 8px sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('I2P', size / 2, size / 2);

        const numPixels = Math.floor(Math.random() * 30) + 10;
        ctx.fillStyle = '#fff';
        for (let i = 0; i < numPixels; i++) {
            const x = Math.floor(Math.random() * size);
            const y = Math.floor(Math.random() * size);
            ctx.fillRect(x, y, 1, 1);
        }

        const dataURL = canvas.toDataURL('image/png');
        faviconLink.href = dataURL;
    }

    generateRandomFavicon();
});
