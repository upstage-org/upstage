function mouseUpOnStage(e) {
    const held = currentlyHolding();
    if (held != undefined) {
        const details = { 
            target: held, 
            x: e.clientX, 
            y: e.clientY, 
            easing: getCurrentEasing(), 
            duration: getCurrentMovementDuration() 
        };
        sendMessage({
            type: "moveTo",
            details: details
        });
    }
}

function dropOnStage(e) {
    const imgSrc = e.dataTransfer.getData("text/uri");
    const avId = e.dataTransfer.getData("text/plain");
    if (imgSrc != undefined && imgSrc != "") {
        sendMessage({
            type: "placeAvatarOnStage",
            details: {
                id: randomElementId(),
                src: imgSrc, 
                x: e.clientX, 
                y: e.clientY
            }
        });
    } else if (avId != undefined && avId != "") {
        sendMessage({
            type: "moveTo",
            details: {
                target: avId,
                x: e.clientX, 
                y: e.clientY,
                easing: getCurrentEasing(),
                duration: getCurrentMovementDuration()
            }
        });
    }
}

function addAvatarDragStart(e) {
    e.dataTransfer.clearData();
    e.dataTransfer.type = "copy";
    e.dataTransfer.setData("text/uri", e.target.getAttribute("src"));
}

function onAvatarDragStart(e) {
    e.dataTransfer.clearData();
    e.dataTransfer.type = "move";
    e.dataTransfer.setData("text/plain", e.target.id);
}