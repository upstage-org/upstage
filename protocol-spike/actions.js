function placeAvatarOnStage({id = undefined, src = undefined, x = undefined, y = undefined}) {
    if (id == undefined || src == undefined) {
        throw("Can't place avatar on stage: No ID or SRC");
    }
    if (x == undefined || y == undefined) {
        throw("Can't place avatar on stage: No Coordinates");
    }
    const newAv = buildAvatar({id: id, src: src});
    getStage().appendChild(newAv);
    moveTo({target: newAv, x: x, y: y});
}

function moveTo({target = undefined, x = undefined, y = undefined, duration = 0, easing = getCurrentEasing()}) {
    if (target == undefined || x == undefined || y == undefined) {
        console.error(`Move failed: target: ${target} => ${x}, ${y}`);
        return;
    }
    const rect = target.getBoundingClientRect();
    const stage = getStage();
    const transX = x - (rect.width / 2);
    const transY = (y - stage.offsetTop) - (rect.height / 2);
    anime({
        targets: [target],
        translateX: transX,
        translateY: transY,
        duration: duration,
        easing: easing
    });
}