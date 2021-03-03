import store from "@/store";

export function attachPropToAvatar(state, object) {
    if (object.type === 'prop') {
        // Deattach from old avatar
        state.board.objects.forEach(a => {
            if (a.attachedProps?.includes(object.id)) {
                a.attachedProps = a.attachedProps.filter(id => id !== object.id);
            }
        })
        // Looking for underlaying avatar
        state.board.objects.forEach(a => {
            if (a.type === 'prop') {
                return false;
            }
            if (object.x > a.x + a.w) {
                return false;
            }
            if (object.y > a.y + a.h) {
                return false;
            }
            if (object.x + object.w < a.x) {
                return false;
            }
            if (object.y + object.h < a.y) {
                return false;
            }
            if (!a.attachedProps) {
                a.attachedProps = [];
            }
            a.attachedProps.push(object.id)
            return true;
        });
    }
}

export function toRelative(size) {
    const stageSize = store.getters['stage/stageSize'];
    return size / stageSize.width;
}

export function toAbsolute(size) {
    const stageSize = store.getters['stage/stageSize'];
    return size * stageSize.width;
}

export function serializeObject(object, keepSrc) {
    const { src, type } = object;
    if (!keepSrc) {
        object = {
            ...object,
            src: type === 'drawing' || type === 'stream' || type === 'text' ? null : src
        };
    }
    object.x = toRelative(object.x)
    object.y = toRelative(object.y)
    object.w = toRelative(object.w)
    object.h = toRelative(object.h)
    if (object.type === 'text') {
        object.fontSize = toRelative(object.fontSize.slice(0, -2)) + 'px'
    }
    return object;
}

export function deserializeObject(object, keepSrc) {
    if (!keepSrc) {
        if (object.type === 'drawing' || object.type === 'stream' || object.type === 'text') {
            delete object.src;
        }
    }
    object.x = toAbsolute(object.x)
    object.y = toAbsolute(object.y)
    object.w = toAbsolute(object.w)
    object.h = toAbsolute(object.h)
    if (object.type === 'text') {
        object.fontSize = toAbsolute(object.fontSize.slice(0, -2)) + 'px'
    }
    return object;
}