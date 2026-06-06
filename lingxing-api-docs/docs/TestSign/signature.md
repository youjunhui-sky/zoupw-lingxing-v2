<iframe id="signatureFrame" contentEditable="false" style="width: 100%; min-height: 800px; border: none; outline: none; overflow: hidden;" src="docs/TestSign/signature.html"></iframe>

<script>
window.addEventListener('message', function(e) {
    if (e.data && e.data.type === 'iframeResize') {
        var iframe = document.getElementById('signatureFrame');
        if (iframe && e.data.height) {
            iframe.style.height = e.data.height + 'px';
        }
    }
});
</script>
