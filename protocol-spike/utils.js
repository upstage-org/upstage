
const easingNames = [
    'easeInQuad',
    'easeInCubic',
    'easeInQuart',
    'easeInQuint',
    'easeInSine',
    'easeInExpo',
    'easeInCirc',
    'easeInBack',
    'easeOutQuad',
    'easeOutCubic',
    'easeOutQuart',
    'easeOutQuint',
    'easeOutSine',
    'easeOutExpo',
    'easeOutCirc',
    'easeOutBack',
    'easeInBounce',
    'easeInOutQuad',
    'easeInOutCubic',
    'easeInOutQuart',
    'easeInOutQuint',
    'easeInOutSine',
    'easeInOutExpo',
    'easeInOutCirc',
    'easeInOutBack',
    'easeInOutBounce',
    'easeOutBounce',
    'easeOutInQuad',
    'easeOutInCubic',
    'easeOutInQuart',
    'easeOutInQuint',
    'easeOutInSine',
    'easeOutInExpo',
    'easeOutInCirc',
    'easeOutInBack',
    'easeOutInBounce',
  ]

function currentlyHolding() {
    return document.querySelector(".holding.avatar");
}

function isHeld(avatar) {
    return avatar.classList.contains('held');
}

function isAvatar(elem) {
    return elem.classList.contains('avatar');
}

function isCurrentlyHolding(avatar) {
    return currentlyHolding() != undefined;
}

function getStage() {
    return document.querySelector("#stage");
}

function getCurrentEasing() {
    return document.querySelector("#easingSelector").value;
}

function getCurrentMovementDuration() {
    try {
        return parseInt(document.querySelector("#movementDuration").value);
    } catch(error) {
        return 3000;
    }
}

function initMovementTools() {
    const easingSelector = document.querySelector("#easingSelector");
    easingNames.forEach(function(name) {
        const newOpt = document.createElement("option");
        newOpt.value = name;
        newOpt.innerText = name;
        easingSelector.appendChild(newOpt);
    });
}

function randomElementId() {
    return String.fromCharCode(65+Math.floor(Math.random() * 26)) 
    + Math.random().toString(36).substring(2, 15) 
    + Math.random().toString(36).substring(2, 15);
}

function buildAvatar({id = randomElementId(), src = undefined}) {
    if (src == undefined) {
        throw("Can't build avatar: No SRC");
    }
    const newAvatar = document.createElement("div");
    newAvatar.id =  id;
    newAvatar.classList.add("avatar");
    newAvatar.setAttribute("draggable", "true");
    newAvatar.addEventListener("dragstart", onAvatarDragStart);
    const avImage = document.createElement("img");
    avImage.setAttribute("src", src);
    avImage.setAttribute("draggable", "false");
    newAvatar.appendChild(avImage);
    return newAvatar;
}

function getConnectionStatusElem() {
    return document.querySelector("#connectionStatus");
}

function setConnectionStatus({status = "bad"}) {
    const statusElem = getConnectionStatusElem();
    statusElem.classList.forEach(c => statusElem.classList.remove(c));
    if (statusElem == undefined) {
        return;
    }
    switch (status) {
        case "good":
            statusElem.classList.add(status);
            statusElem.innerText = "Online";
            break;
        case "poor":
            statusElem.classList.add(status);
            statusElem.innerText = "Weak";
            break;
        default:
            statusElem.classList.add("bad");
            statusElem.innerText = "Offline";
            break;
    }
}