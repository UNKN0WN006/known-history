// minimal content script
(() => {
  const snippet = (document.body && document.body.innerText) ? document.body.innerText.slice(0,3000) : '';
  console.log('LifeLens capture', { url: location.href, title: document.title, snippet_len: snippet.length });
})();