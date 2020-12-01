function initAvatars() {
    document.querySelectorAll("img.avatar").forEach(function(img) {
        img.setAttribute("draggable", "true");
        img.addEventListener("dragstart", addAvatarDragStart);
    });
}

function initTools() {
    initMovementTools();
}

function init() {
    const stage = getStage();
    stage.addEventListener("mouseup", mouseUpOnStage);
    stage.addEventListener("dragover", e => e.preventDefault());
    stage.addEventListener("drop", dropOnStage);
    initAvatars();
    initTools();
}

(init).call(this);