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

export function normalizeObject(object) {
    const { src, type } = object;
    return {
        ...object,
        src: type === 'drawing' || type === 'stream' ? null : src
    };
}