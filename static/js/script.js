console.log("JS Loaded");
document.addEventListener("visibilitychange", () => {
    if(document.hidden){
        fetch('/log', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({event:'Tab switched'})
        });
    }
});